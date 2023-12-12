#include <stdio.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#include "config.h"
#include "lists.h"


void read_from_buffer(int connfd)
{
    char buff[BUFF_SIZE];

    bzero(buff, BUFF_SIZE);
    read(connfd, buff, sizeof(buff));


    Node *head = NULL;
    Node *current = NULL;
    int i = 0;
    int nodes_count = 0;
    while (nodes_count < NODES_COUNT) {
        if (head == NULL) {
            head = (Node *)malloc(sizeof(Node));
            current = head;
        } else {
            current->next = (Node *)malloc(sizeof(Node));
            current = current->next;
        }
        current->dataType = buff[i];
        i += sizeof(int32_t);
        switch (current->dataType) {
            case 0:
                memcpy(&current->data.int16Value, buff + i, sizeof(int16_t));
                i += sizeof(int16_t);
                break;
            case 1:
                memcpy(&current->data.int32Value, buff + i, sizeof(int32_t));
                i += sizeof(int32_t);
                break;
            case 2:
                memcpy(current->data.fixedSizeString, buff + i, sizeof(current->data.fixedSizeString));
                i += sizeof(current->data.fixedSizeString);
                break;
            case 3:
                current->data.variableSizeString = strdup(buff + i);
                i += strlen(buff + i) + 1;
                break;
        }
        current->next = NULL;
        nodes_count++;
    }
    printList(head);
    freeList(head);

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
