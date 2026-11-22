#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
    char nameBuffer[100];

    if (argc < 2) {
        printf("Usage: %s yourname\n", argv[0]);
        printf("Please enter your name for registration purposes.");
        exit(1);
    }
    else {
            printf("nameBuffer address: %p\n", (void *)nameBuffer);
            strcpy(nameBuffer, argv[1]);
    }

    printf("Thank you %s, have a nice day!\n", nameBuffer);
}
