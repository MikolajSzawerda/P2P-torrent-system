#include <arpa/inet.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#include <ctype.h> // For toupper
#include "udp_cl_serv.h"

#define INFO_MSG "You have sent proper message"
#define ERROR_MSG "Your message does not obey contract!"


int check_msg(const char *data, int n) {
    for (int i = 0; i < n; i++) {
        if (data[i] != (char) (65 + (i % 26)))
            return -1;
    }
    return 0;
}

int main(int argc, char **argv) {
    struct addrinfo server_conf = {
            .ai_family = AF_INET,
            .ai_socktype = SOCK_DGRAM,
            .ai_flags = AI_PASSIVE
    };

    struct addrinfo *server_binding;

    if (getaddrinfo(0, PORT, &server_conf, &server_binding) < 0) bailout("retreving binding info")
    int binded_sock;

    if ((binded_sock = socket(server_binding->ai_family, server_binding->ai_socktype, 0)) < 0) bailout("opening socket")

    if (bind(binded_sock, server_binding->ai_addr, server_binding->ai_addrlen) < 0) bailout("binding stream socket");

    freeaddrinfo(server_binding);

    struct payload_in data_received;

    while (1) {
        struct sockaddr_in client_conf;
        socklen_t servaddr_len = sizeof(client_conf);

        size_t n_received;
        memset(data_received.data, 0, sizeof(PAYLOAD_IN_SIZE));
        if ((n_received = recvfrom(binded_sock, &data_received, BSIZE, 0, (struct sockaddr *) &client_conf,
                                   &servaddr_len)) ==
            -1) bailout(
                "reading stream message")
        printf("n letters: %d \npayload: %s\n", data_received.length - sizeof(short), data_received.data);
        short received_payload_size = max(min(PAYLOAD_IN_SIZE, data_received.length - sizeof(short)), 0);
        int is_valid = check_msg(data_received.data, received_payload_size);
        memset(data_received.data, 0, PAYLOAD_IN_SIZE);
        if (is_valid < 0) {
            data_received.length = sizeof(ERROR_MSG);
            strcpy(data_received.data, ERROR_MSG);
        } else {
            data_received.length = sizeof(INFO_MSG);
            strcpy(data_received.data, INFO_MSG);
        }
        if (sendto(binded_sock, &data_received, BSIZE, 0, (struct sockaddr *) &client_conf, sizeof(client_conf)) <
            0) bailout(
                "sending to client")
    }

    exit(0);
}
