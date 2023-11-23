#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <unistd.h>
#include <string.h>
#include "udp_cl_serv.h"

#define PROPER_MESSAGE_FLAG 0
#define WRONG_MESSAGE_FLAG 1
#define MISLEADING_MESSAGE_FLAG 2

void generate_proper_message(char *buf, int n) {
    for (int i = 0; i < n; i++)
        buf[i] = (char) (65 + (i % 26));
}

void generate_wrong_message(char *buf, int n) {
    for (int i = 0; i < n; i++)
        buf[i] = (char) (65 + (i % 26));
    buf[0] = 'B';
}

//TODO check using docker
int main(int argc, char **argv) {
    struct addrinfo *bind_info;
    int sock;
    int n_letters = argc > 1 ? atoi(argv[1]) : DEF_NLETTERS;
    if (n_letters > PAYLOAD_SIZE) bailout("Exceeded max letters to send!")
    int message_type = argc > 2 ? atoi(argv[2]) : PROPER_MESSAGE_FLAG;
    struct addrinfo hints = {
            .ai_family = AF_INET,
            .ai_socktype = SOCK_DGRAM,
    };

    if (getaddrinfo(argc > 3 ? argv[3] : DEF_ADDR, argc > 4 ? argv[4] : DEF_PORT,
                    &hints, &bind_info) < 0) bailout("retreving binding info")

    if ((sock = socket(bind_info->ai_family, bind_info->ai_socktype, 0)) < 0) bailout("creating socket")

    struct payload pl = {
            .length = (short) (n_letters + HEADER_SIZE)
    };
    switch (message_type) {
        case WRONG_MESSAGE_FLAG:
            generate_wrong_message(pl.data, n_letters);
            break;
        case MISLEADING_MESSAGE_FLAG:
            generate_proper_message(pl.data, n_letters);
            pl.length = max(pl.length + 1, BSIZE);
            break;
        default:
            generate_proper_message(pl.data, n_letters);
            break;
    }
    if (sendto(sock, &pl, pl.length, 0, bind_info->ai_addr, bind_info->ai_addrlen) <
        0) bailout(
            "sending data")

    memset(&pl, 0, BSIZE);
    if (recvfrom(sock, &pl, BSIZE, 0, bind_info->ai_addr, &bind_info->ai_addrlen) <
        0) bailout(
            "Receiving")
    printf("%s\n", pl.data);
    freeaddrinfo(bind_info);
    close(sock);
    exit(0);
}
