#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
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

void return_message(struct payload *buffer) {
    short recv_payload_len = max(min(PAYLOAD_SIZE, buffer->length - HEADER_SIZE), 0);
    int is_valid = check_msg(buffer->data, recv_payload_len);
    memset(buffer->data, 0, recv_payload_len);
    if (is_valid < 0) {
        buffer->length = sizeof(ERROR_MSG);
        strcpy(buffer->data, ERROR_MSG);
    } else {
        buffer->length = sizeof(INFO_MSG);
        strcpy(buffer->data, INFO_MSG);
    }
}


int main(int argc, char **argv) {
    struct addrinfo *server_binding;
    struct payload recv;
    struct sockaddr_in cl_info;
    socklen_t info_len = sizeof(cl_info);
    struct addrinfo server_conf = {
            .ai_family = AF_INET,
            .ai_socktype = SOCK_DGRAM,
    };


    if (getaddrinfo(0, argc > 1 ? argv[1] : DEF_PORT, &server_conf, &server_binding) < 0) bailout(
            "retreving binding info")
    int binded_sock;

    if ((binded_sock = socket(server_binding->ai_family, server_binding->ai_socktype, 0)) < 0) bailout("opening socket")

    if (bind(binded_sock, server_binding->ai_addr, server_binding->ai_addrlen) < 0) bailout("binding stream socket");

    freeaddrinfo(server_binding);

    while (1) {

        memset(&recv, 0, sizeof(BSIZE));
        if (recvfrom(binded_sock, &recv, BSIZE, 0, (struct sockaddr *) &cl_info,
                     &info_len) < 0) bailout("reading stream message")
        return_message(&recv);
        if (sendto(binded_sock, &recv, recv.length + 1, 0, (struct sockaddr *) &cl_info, sizeof(cl_info)) <
            0) bailout(
                "sending to client")
    }

    exit(0);
}
