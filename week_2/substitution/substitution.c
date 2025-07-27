#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int is_valid_key(char *key)
{
    if (strlen(key) != 26)
    {
        return 0;
    }

    int seen[26] = {0};

    for (int i = 0; i < 26; i++)
    {
        if (!isalpha(key[i]))
        {
            return 0;
        }

        int index = toupper(key[i]) - 'A';

        if (seen[index])
        {
            return 0;
        }

        seen[index] = 1;
    }

    return 1;
}

int main(int argc, char *argv[])
{
    if (argc != 2 || !is_valid_key(argv[1]))
    {
        printf("Usage: ./substitution KEY (26 unique alphabetic characters)\n");
        return 1;
    }

    char key[26];
    for (int i = 0; i < 26; i++)
    {
        key[i] = toupper(argv[1][i]);
    }

    char plaintext[1000];
    printf("plaintext: ");
    fgets(plaintext, sizeof(plaintext), stdin);

    printf("ciphertext: ");

    for (int i = 0; plaintext[i] != '\0'; i++)
    {
        char c = plaintext[i];

        if (isupper(c))
        {
            int index = c - 'A';
            printf("%c", key[index]);
        }
        else if (islower(c))
        {
            int index = c - 'a';
            printf("%c", tolower(key[index]));
        }
        else
        {
            printf("%c", c);
        }
    }

    printf("\n");
    return 0;
}
