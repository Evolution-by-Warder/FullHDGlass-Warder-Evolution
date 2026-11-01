/* FullHDGlass bitrate helper. Original implementation, 2026 Warder.
 * Counts bytes delivered by Linux DVB filters; no decoder or tuning changes.
 * stdout: video min/max/average/current, then audio, in decimal kbit/s.
 */
#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <fcntl.h>
#include <inttypes.h>
#include <linux/dvb/dmx.h>
#include <poll.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <time.h>
#include <unistd.h>

#define PACKET 188
#define READ_SIZE (PACKET * 128)
struct ts_counter { unsigned char pending[PACKET]; size_t used; unsigned pid; uint64_t invalid; };
struct meter {
    int fd, pid, ts, zero_samples;
    uint64_t total, interval, started, minimum, maximum;
    struct ts_counter parser;
};
static volatile sig_atomic_t running = 1;
static void stop_signal(int sig) { (void)sig; running = 0; }
static uint64_t now_ms(void) {
    struct timespec t;
    if (clock_gettime(CLOCK_MONOTONIC, &t)) return 0;
    return (uint64_t)t.tv_sec * 1000 + (uint64_t)t.tv_nsec / 1000000;
}
/* Do not count TS headers, adaptation fields, wrong PIDs or damaged packets.
 * Retain partial packets across reads rather than assuming read boundaries.
 */
static size_t packet_payload(const unsigned char *p, unsigned pid) {
    unsigned control;
    size_t start = 4;
    if (p[0] != 0x47 || (p[1] & 0x80) || (unsigned)(((p[1]&31)<<8)|p[2]) != pid) return 0;
    control = (p[3] >> 4) & 3;
    if (!(control & 1)) return 0;
    if (control & 2) start += 1 + p[4];
    return start <= PACKET ? PACKET - start : 0;
}
static uint64_t consume_ts(struct ts_counter *c, const unsigned char *data, size_t size) {
    uint64_t bytes = 0;
    while (size) {
        size_t take;
        if (!c->used && *data != 0x47) { data++; size--; c->invalid++; continue; }
        take = (c->used < 4 ? 4 : PACKET) - c->used;
        if (take > size) take = size;
        memcpy(c->pending + c->used, data, take);
        c->used += take; data += take; size -= take;
        if (c->used >= 4 && (c->pending[0]!=0x47 || (unsigned)(((c->pending[1]&31)<<8)|c->pending[2])!=c->pid || !(c->pending[3]&0x30))) {
            memmove(c->pending,c->pending+1,--c->used); c->invalid++;
        }
        if (c->used == PACKET) {
            bytes += packet_payload(c->pending, c->pid);
            c->used = 0;
        }
    }
    return bytes;
}
static int open_filter(struct meter *m, int adapter, int demux, int ts) {
    char path[96];
    struct dmx_pes_filter_params filter;
    snprintf(path, sizeof(path), "/dev/dvb/adapter%d/demux%d", adapter, demux);
    m->fd = open(path, O_RDONLY | O_NONBLOCK | O_CLOEXEC);
    if (m->fd < 0) { fprintf(stderr,"WarderBitrate: open %s pid=%d: %s\n",path,m->pid,strerror(errno)); return -1; }
    if (ioctl(m->fd, DMX_SET_BUFFER_SIZE, 2*1024*1024) < 0)
        fprintf(stderr,"WarderBitrate: buffer pid=%d: %s\n",m->pid,strerror(errno));
    memset(&filter,0,sizeof(filter));
    filter.pid = (uint16_t)m->pid;
    filter.input = DMX_IN_FRONTEND;
    filter.output = ts ? DMX_OUT_TSDEMUX_TAP : DMX_OUT_TAP;
    filter.pes_type = DMX_PES_OTHER;
    filter.flags = DMX_IMMEDIATE_START;
    if (ioctl(m->fd, DMX_SET_PES_FILTER, &filter) < 0) {
        fprintf(stderr,"WarderBitrate: filter pid=%d mode=%s: %s\n",m->pid,ts?"ts":"pes",strerror(errno));
        close(m->fd); m->fd=-1; return -1;
    }
    m->ts = ts;
    memset(&m->parser,0,sizeof(m->parser)); m->parser.pid=(unsigned)m->pid;
    fprintf(stderr,"WarderBitrate: filter pid=%d mode=%s adapter=%d demux=%d\n",m->pid,ts?"ts":"pes",adapter,demux);
    return 0;
}
static void close_filter(struct meter *m) {
    if (m->fd >= 0) { (void)ioctl(m->fd, DMX_STOP); close(m->fd); m->fd=-1; }
}
static int receive(struct meter *m) {
    unsigned char data[READ_SIZE];
    int loops;
    for (loops=0; loops<8; loops++) {
        ssize_t size=read(m->fd,data,sizeof(data));
        uint64_t bytes;
        if (size < 0) {
            if (errno==EINTR) continue;
            if (errno==EAGAIN || errno==EWOULDBLOCK) return 0;
            fprintf(stderr,"WarderBitrate: read pid=%d mode=%s: %s\n",m->pid,m->ts?"ts":"pes",strerror(errno));
            return -1;
        }
        if (!size) { fprintf(stderr,"WarderBitrate: end of stream pid=%d\n",m->pid); return -1; }
        bytes=m->ts ? consume_ts(&m->parser,data,(size_t)size) : (uint64_t)size;
        m->total+=bytes; m->interval+=bytes;
    }
    return 0;
}
static uint64_t rate(uint64_t bytes, uint64_t milliseconds) {
    return milliseconds ? bytes*8/milliseconds : 0;
}
static void print_sample(struct meter *m, uint64_t elapsed, uint64_t duration) {
    uint64_t current=rate(m->interval,duration), average=rate(m->total,elapsed);
    if (m->minimum==UINT64_MAX || current<m->minimum) m->minimum=current;
    if (current>m->maximum) m->maximum=current;
    printf("%"PRIu64" %"PRIu64" %"PRIu64" %"PRIu64"\n",m->minimum,m->maximum,average,current);
    m->zero_samples=current ? 0 : m->zero_samples+1;
    m->interval=0;
}
static int number(const char *s, int lower, int upper, int *out) {
    char *end; long n;
    errno=0; n=strtol(s,&end,10);
    if (errno || !*s || *end || n<lower || n>upper) return -1;
    *out=(int)n; return 0;
}
#ifndef WARDER_BITRATE_UNIT
int main(int argc, char **argv) {
    struct meter meters[2];
    int adapter,demux,i,status=0;
    uint64_t last,now;
    memset(meters,0,sizeof(meters));
    for (i=0;i<2;i++) { meters[i].fd=-1; meters[i].minimum=UINT64_MAX; }
    if (argc!=5 || number(argv[1],0,255,&adapter) || number(argv[2],0,255,&demux)
        || number(argv[3],-1,8190,&meters[0].pid) || number(argv[4],-1,8190,&meters[1].pid)
        || (meters[0].pid<=0 && meters[1].pid<=0)) {
        fprintf(stderr,"usage: %s <adapter> <demux> <video-pid> <audio-pid>\n",argv[0]); return 2;
    }
    signal(SIGTERM,stop_signal); signal(SIGINT,stop_signal);
    for (i=0;i<2;i++) if (meters[i].pid>0 && open_filter(&meters[i],adapter,demux,0)) {
        if (i!=0 || open_filter(&meters[i],adapter,demux,1)) { status=2; goto done; }
    }
    last=now_ms();
    if (!last) { status=2; goto done; }
    for (i=0;i<2;i++) meters[i].started=last;
    while (running) {
        struct pollfd fds[2]; int ready;
        for (i=0;i<2;i++) { fds[i].fd=meters[i].fd; fds[i].events=POLLIN; fds[i].revents=0; }
        ready=poll(fds,2,100);
        if (ready<0) { if (errno==EINTR) continue; status=2; break; }
        for (i=0;i<2;i++) if (fds[i].fd>=0 && fds[i].revents) {
            if ((fds[i].revents & (POLLERR|POLLHUP|POLLNVAL)) || receive(&meters[i])) { status=2; goto done; }
        }
        now=now_ms();
        if (!now) { status=2; break; }
        if (now-last < 1000) continue;
        for (i=0;i<2;i++) print_sample(&meters[i],now-meters[i].started,now-last);
        if (fflush(stdout)) { status=2; break; }
        last=now;
        /* Some receiver drivers accept the PES filter but never return video.
         * Change only our video filter to TS, leaving playback and audio alone.
         */
        if (meters[0].fd>=0 && !meters[0].ts && meters[0].zero_samples>=3) {
            fprintf(stderr,"WarderBitrate: video PID %d returned no PES bytes; switching to TS payload measurement\n",meters[0].pid);
            close_filter(&meters[0]);
            if (open_filter(&meters[0],adapter,demux,1)) { status=2; break; }
            meters[0].total=meters[0].interval=0; meters[0].started=now;
            meters[0].minimum=UINT64_MAX; meters[0].maximum=0; meters[0].zero_samples=0;
        }
    }
done:
    for (i=0;i<2;i++) close_filter(&meters[i]);
    return status;
}
#endif
