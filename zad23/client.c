#include <arpa/inet.h>
#include <stdlib.h>
#include <strings.h>
#include <sys/socket.h>
#include <unistd.h>
#include <time.h>

#include "config.h"
#include "lists.h"



int writeListToBuffer(Node *head, char *buff) {
    Node *current = head;
    int i = 0;
    while (current != NULL) {
        buff[i++] = current->dataType;
        switch (current->dataType) {
            case 0:
                memcpy(buff + i, &current->data.int16Value, sizeof(int16_t));
                i += sizeof(int16_t);
                break;
            case 1:
                memcpy(buff + i, &current->data.int32Value, sizeof(int32_t));
                i += sizeof(int32_t);
                break;
            case 2:
                memcpy(buff + i, current->data.fixedSizeString, sizeof(current->data.fixedSizeString));
                i += sizeof(current->data.fixedSizeString);
                break;
            case 3:
                memcpy(buff + i, current->data.variableSizeString, strlen(current->data.variableSizeString) + 1);
                i += strlen(current->data.variableSizeString) + 1;
                break;
        }
        current = current->next;
    }
    return i;
}


void write_buffer_to_server(int sockfd)
{
    char buff[BUFF_SIZE];

    bzero(buff, sizeof(buff));
    // create 4 different nodes ~~ NODES_COUNT
    Node *head = createNodeInt16(123);
    Node* n = head;
    for(int i=0;i<NODES_COUNT-1;i++){
        n->next = createNodeInt32(789);
        n = n->next;
    }
    // write the linked list to the buffer
    writeListToBuffer(head, buff);
    // send the buffer to the server
    send(sockfd, buff, sizeof(buff), 0);
    // free the memory allocated
    freeList(head);

}

int main(int argc, char **argv)
{
    int sockfd;
    struct sockaddr_in servaddr;

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1) {
        exit(-1);
    }

    int bufferSize = argc > 1 ? atoi(argv[1]) : 100;
    if (setsockopt(sockfd, SOL_SOCKET, SO_SNDBUFFORCE, &bufferSize, sizeof(bufferSize)) < 0) {
        perror("Error setting socket options");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    bzero(&servaddr, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = inet_addr("127.0.0.1");
    servaddr.sin_port = htons(PORT);


    if (connect(sockfd, (struct sockaddr*)&servaddr, sizeof(servaddr))!= 0) {
        exit(-1);
    }
    while(1){
        struct timespec start, end;
        clock_gettime(CLOCK_MONOTONIC, &start);
        write_buffer_to_server(sockfd);
        clock_gettime(CLOCK_MONOTONIC, &end);
        long elapsed= (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec);
        if(elapsed > 0){
            printf("%ld\n", elapsed);
        }
    }

    close(sockfd);
}
