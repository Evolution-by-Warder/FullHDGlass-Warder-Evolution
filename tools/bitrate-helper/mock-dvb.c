/* Test-only userspace DVB device simulator for the actual helper executable. */
#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <fcntl.h>
#include <linux/dvb/dmx.h>
#include <poll.h>
#include <stdarg.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <time.h>
#include <unistd.h>
struct fake { int active,pid,ts; };
static struct fake entries[1024];
int open(const char *path,int flags,...) {
    int (*real_open)(const char*,int,...)=dlsym(RTLD_NEXT,"open");
    mode_t mode=0; int fd;
    if (flags&O_CREAT) { va_list ap; va_start(ap,flags); mode=va_arg(ap,int); va_end(ap); }
    if (strncmp(path,"/dev/dvb/",9)) return real_open(path,flags,mode);
    fd=real_open("/dev/null",O_RDONLY);
    if (fd>=0 && fd<1024) { entries[fd].active=1; entries[fd].pid=0; entries[fd].ts=0; }
    return fd;
}
int close(int fd) {
    int (*real_close)(int)=dlsym(RTLD_NEXT,"close");
    if (fd>=0 && fd<1024) entries[fd].active=0;
    return real_close(fd);
}
int ioctl(int fd,unsigned long request,...) {
    va_list ap; void *arg=NULL;
    if (request!=DMX_STOP) { va_start(ap,request); arg=va_arg(ap,void*); va_end(ap); }
    if (fd>=0 && fd<1024 && entries[fd].active) {
        if (request==DMX_SET_PES_FILTER) {
            struct dmx_pes_filter_params *filter=arg;
            if (filter->pid==5101 && ((!getenv("MOCK_VIDEO_PES") && filter->output==DMX_OUT_TAP && getenv("MOCK_PES_FAIL")) || (filter->output==DMX_OUT_TSDEMUX_TAP && getenv("MOCK_TS_FAIL")))) {
                errno=EOPNOTSUPP; return -1;
            }
            entries[fd].pid=filter->pid; entries[fd].ts=filter->output==DMX_OUT_TSDEMUX_TAP;
        }
        return 0;
    }
    errno=ENOTTY; return -1;
}
int poll(struct pollfd *fds,nfds_t count,int timeout) {
    nfds_t i; int n=0;
    (void)timeout;
    struct timespec wait={0,20000000}; nanosleep(&wait,NULL);
    for (i=0;i<count;i++) { fds[i].revents=0; if (fds[i].fd>=0 && entries[fds[i].fd].active) { fds[i].revents=POLLIN; n++; } }
    return n;
}
ssize_t read(int fd,void *buffer,size_t size) {
    ssize_t (*real_read)(int,void*,size_t)=dlsym(RTLD_NEXT,"read");
    unsigned char *p=buffer; int i;
    if (fd<0 || fd>=1024 || !entries[fd].active) return real_read(fd,buffer,size);
    if (entries[fd].pid==5101 && !entries[fd].ts && !getenv("MOCK_VIDEO_PES")) { errno=EAGAIN; return -1; }
    if (!entries[fd].ts) { if (size>256) size=256; memset(p,0,size); return (ssize_t)size; }
    if (size<1880) { errno=EINVAL; return -1; }
    for (i=0;i<10;i++) { memset(p,0x55,188); p[0]=0x47; p[1]=(unsigned)entries[fd].pid>>8; p[2]=entries[fd].pid&255; p[3]=0x10; p+=188; }
    return 1880;
}
