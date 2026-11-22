#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

char *IMPORTANT = "/bin/sh <&1 >&1";

// For testing only.  TODO: DELETE THIS FUNCTION
void vulnerable() {
    printf("Congrats on running the vulnerable function!\n");
    system(IMPORTANT);
    exit(0);
}

int main(int argc, char **argv) {
    if (argc != 1) {
        printf("Usage: overflow\n");
        exit(1);
    }

    char nameBuffer[20];

    printf("Please enter your name for registration purposes: ");
    gets(nameBuffer);
    printf("\nThank you %s, have a nice day!\n", nameBuffer);
}
