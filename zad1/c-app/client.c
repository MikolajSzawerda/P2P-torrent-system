#include <arpa/inet.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#include "udp_cl_serv.h"

//TODO hostname resolution
//TODO usage of arguments
//TODO check using docker
int main(int argc, char **argv) {
    int cl_socket;
    if ((cl_socket = socket(AF_INET, SOCK_DGRAM, 0)) < 0) bailout("creating socket")
    struct sockaddr_in servaddr = {
            .sin_family = AF_INET,
            .sin_port = htons(atoi(PORT)),
            .sin_addr.s_addr = inet_addr(ADDR)
    };
    struct payload data_to_send = {
            .length = PAYLOAD_SIZE
    };
    for (int i = 0; i < NLETTERS; i++)
        data_to_send.data[i] = (char) (65 + (i % 26));
    if (sendto(cl_socket, &data_to_send, PAYLOAD_SIZE, 0, (struct sockaddr *) &servaddr, sizeof(servaddr)) < 0) bailout(
            "sending data")

    struct payload_in data_received;
    socklen_t servaddr_len = sizeof(servaddr);
    if (recvfrom(cl_socket, &data_received, BSIZE, 0, (struct sockaddr *) &servaddr, &servaddr_len) < 0) bailout(
            "Receiving")
    printf("%s\n", data_received.data);
    close(cl_socket);
    exit(0);
}
