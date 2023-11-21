
#ifndef C_APP_UDP_CL_SERV_H
#define C_APP_UDP_CL_SERV_H

#define DEF_PORT "8081"
#define DEF_ADDR "localhost"
#define BSIZE 1024
#define DEF_NLETTERS 26
#define HEADER_SIZE (sizeof(short))
#define PAYLOAD_SIZE (BSIZE - HEADER_SIZE)

#define bailout(s) {perror(s); exit(1); }

struct payload {
    short length;
    char data[PAYLOAD_SIZE];
};


short min(short a, short b) {
    return a < b ? a : b;
}

short max(short a, short b) {
    return a >= b ? a : b;
}


#endif
