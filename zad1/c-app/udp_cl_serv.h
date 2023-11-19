
#ifndef C_APP_UDP_CL_SERV_H
#define C_APP_UDP_CL_SERV_H
#define PORT "8081"
#define ADDR "127.0.0.1"
#define BSIZE 1024
#define NLETTERS 26
#define PAYLOAD_SIZE (NLETTERS + sizeof(short))
#define PAYLOAD_IN_SIZE (BSIZE - sizeof(short))

#define bailout(s) {perror(s); exit(1); }

struct payload {
    short length;
    char data[NLETTERS];
};

struct payload_in {
    short length;
    char data[PAYLOAD_IN_SIZE];
};

short min(short a, short b) {
    return a < b ? a : b;
}

short max(short a, short b) {
    return a >= b ? a : b;
}

#endif
