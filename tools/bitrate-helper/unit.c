#define WARDER_BITRATE_UNIT
#include "warder-bitrate.c"
#include <assert.h>
int main(void) {
    unsigned char p[188], stream[188*3+3];
    struct ts_counter c; size_t split; int n;
    memset(p,0x55,sizeof(p)); p[0]=0x47; p[1]=5101>>8; p[2]=5101&255; p[3]=0x10;
    assert(packet_payload(p,5101)==184); assert(!packet_payload(p,5102));
    p[3]=0x30; p[4]=7; assert(packet_payload(p,5101)==176);
    p[4]=184; assert(!packet_payload(p,5101));
    p[3]=0x20; assert(!packet_payload(p,5101));
    p[3]=0x10; p[1]|=0x80; assert(!packet_payload(p,5101)); p[1]&=0x7f;
    for (n=0;n<3;n++) memcpy(stream+n*188,p,188);
    for (split=0;split<=188*3;split++) {
        uint64_t result; memset(&c,0,sizeof(c)); c.pid=5101;
        result=consume_ts(&c,stream,split); result+=consume_ts(&c,stream+split,188*3-split);
        assert(result==184*3); assert(c.used==0);
    }
    memset(&c,0,sizeof(c)); c.pid=5101;
    memmove(stream+3,stream,188*3); stream[0]=0x47; stream[1]=0xff; stream[2]=0;
    assert(consume_ts(&c,stream,sizeof(stream))==184*3);
    assert(rate(125000,1000)==1000); assert(rate(125000,500)==2000); assert(!rate(1,0));
    assert(!number("5101",-1,8190,&n) && n==5101);
    assert(number("0x13ed",-1,8190,&n)); assert(number("99999999999999999999",-1,8190,&n));
    assert(number("5101x",-1,8190,&n)); assert(number("8191",-1,8190,&n));
    puts("PASS: TS payload, adaptation/TEI/PID handling, all 565 read splits, resync, rates and argument validation");
    return 0;
}
