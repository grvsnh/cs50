#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Function to check if the input string is a valid positive integer
int is_valid_key(char *s)
{
    for (int i = 0; s[i] != '\0'; i++)
    {
        if (!isdigit(s[i]))
        {
            return 0;
        }
    }
    return 1;
}

int main(int argc, char *argv[])
{
    // Check if the user provided exactly one command-line argument and if it's a valid key
    if (argc != 2 || !is_valid_key(argv[1]))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // Convert the key string to an integer
    int key = atoi(argv[1]);

    // Get plaintext input from the user
    char plaintext[1000];
    printf("plaintext: ");
    fgets(plaintext, sizeof(plaintext), stdin);

    printf("ciphertext: ");

    // Loop through each character in the plaintext
    for (int i = 0; plaintext[i] != '\0'; i++)
    {
        char c = plaintext[i];

        // If it's an uppercase letter, rotate it within A-Z
        if (isupper(c))
        {
            printf("%c", ((c - 'A' + key) % 26) + 'A');
        }
        // If it's a lowercase letter, rotate it within a-z
        else if (islower(c))
        {
            printf("%c", ((c - 'a' + key) % 26) + 'a');
        }
        // If it's any other character, print as-is
        else
        {
            printf("%c", c);
        }
    }

    // Print newline at the end
    printf("\n");
    return 0;
}
