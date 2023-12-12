
#ifndef LAB_REPO_LISTS_H
#define LAB_REPO_LISTS_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "config.h"

typedef union {
    int16_t int16Value;
    int32_t int32Value;
    char fixedSizeString[FIXED_SIZE_STRING_LENGTH];
    char *variableSizeString;
} Data;


typedef struct Node {
    int dataType;  // 0: int16, 1: int32, 2: fixed-size string, 3: variable-size string
    Data data;
    struct Node *next;
} Node;

Node *createNodeInt16(int16_t value) {
    Node *newNode = (Node *)malloc(sizeof(Node));
    newNode->dataType = 0;  // int16
    newNode->data.int16Value = value;
    newNode->next = NULL;
    return newNode;
}

Node *createNodeInt32(int32_t value) {
    Node *newNode = (Node *)malloc(sizeof(Node));
    newNode->dataType = 1;  // int32
    newNode->data.int32Value = value;
    newNode->next = NULL;
    return newNode;
}

Node *createNodeFixedSizeString(const char *value) {
    Node *newNode = (Node *)malloc(sizeof(Node));
    newNode->dataType = 2;  // fixed-size string
    strncpy(newNode->data.fixedSizeString, value, sizeof(newNode->data.fixedSizeString));
    newNode->data.fixedSizeString[sizeof(newNode->data.fixedSizeString) - 1] = '\0'; // Ensure null-termination
    newNode->next = NULL;
    return newNode;
}

Node *createNodeVariableSizeString(const char *value) {
    Node *newNode = (Node *)malloc(sizeof(Node));
    newNode->dataType = 3;  // variable-size string
    newNode->data.variableSizeString = strdup(value);
    newNode->next = NULL;
    return newNode;
}

void printList(Node *head) {
    Node *current = head;
    while (current != NULL) {
        switch (current->dataType) {
            case 0:
                printf("%d (int16)", current->data.int16Value);
                break;
            case 1:
                printf("%d (int32)", current->data.int32Value);
                break;
            case 2:
                printf("%.20s (fixed)", current->data.fixedSizeString);
                break;
            case 3:
                printf("%.20s (var-size)", current->data.variableSizeString);
                break;
        }
        printf("\n");
        current = current->next;
    }
    printf("NULL\n");
}


void freeList(Node *head) {
    Node *current = head;
    while (current != NULL) {
        Node *next = current->next;
        if (current->dataType == 3) {
            free(current->data.variableSizeString);
        }
        free(current);
        current = next;
    }
}

#endif //LAB_REPO_LISTS_H
