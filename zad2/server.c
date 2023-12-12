#include <stdio.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#include "config.h"



void read_from_buffer(int connfd)
{
    char buff[BUFF_SIZE];

    bzero(buff, BUFF_SIZE);
    read(connfd, buff, sizeof(buff));
    printf("From client: %.*s\n", 20, buff);
    bzero(buff, BUFF_SIZE);

}


int main()
{
    int sockfd, connfd, len;
    struct sockaddr_in serv_addr, cli_addr;

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1) {
        exit(-1);
    }

    bzero(&serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    serv_addr.sin_port = htons(PORT);

    if ((bind(sockfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr))) != 0) {
        exit(-1);
    }

    if ((listen(sockfd, BACKLOG)) != 0) {
        exit(-1);
    }

    len = sizeof(cli_addr);
    connfd = accept(sockfd, (struct sockaddr*)&cli_addr, &len);
    if (connfd < 0) {
        exit(-1);
    }

    read_from_buffer(connfd);

    close(sockfd);
}
