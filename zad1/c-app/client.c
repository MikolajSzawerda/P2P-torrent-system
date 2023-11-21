#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <unistd.h>
#include <string.h>
#include "udp_cl_serv.h"

//TODO check using docker
int main(int argc, char **argv) {
    struct addrinfo *bind_info;
    int sock;
    int n_letters = argc > 1 ? atoi(argv[1]) : DEF_NLETTERS;
    struct addrinfo hints = {
            .ai_family = AF_INET,
            .ai_socktype = SOCK_DGRAM,
    };

    if (getaddrinfo(argc > 2 ? argv[2] : DEF_ADDR, argc > 3 ? argv[3] : DEF_PORT,
                    &hints, &bind_info) < 0) bailout("retreving binding info")

    if ((sock = socket(bind_info->ai_family, bind_info->ai_socktype, 0)) < 0) bailout("creating socket")

    struct payload pl = {
            .length = (short) (n_letters + HEADER_SIZE)
    };
    for (int i = 0; i < n_letters; i++)
        pl.data[i] = (char) (65 + (i % 26));
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
