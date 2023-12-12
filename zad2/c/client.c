#include <arpa/inet.h>
#include <stdlib.h>
#include <strings.h>
#include <sys/socket.h>
#include <unistd.h>

#include "config.h"
#include "lists.h"


int writeListToBuffer(Node *head, char *buff) {
    Node *current = head;
    int i = 0;
    while (current != NULL) {
        buff[i] = current->dataType;
        i+= sizeof(int32_t);
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
    head->next = createNodeInt32(456);
    head->next->next = createNodeFixedSizeString("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\0" );
    head->next->next->next = createNodeVariableSizeString("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\0");
    // write the linked list to the buffer
    writeListToBuffer(head, buff);
    // send the buffer to the server
    write(sockfd, buff, sizeof(buff));
    // free the memory allocated
    freeList(head);

}

int main()
{
    int sockfd;
    struct sockaddr_in servaddr;

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1) {
        exit(-1);
    }

    bzero(&servaddr, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = inet_addr("127.0.0.1");
    servaddr.sin_port = htons(PORT);


    if (connect(sockfd, (struct sockaddr*)&servaddr, sizeof(servaddr))!= 0) {
        exit(-1);
    }

    write_buffer_to_server(sockfd);

    close(sockfd);
}
