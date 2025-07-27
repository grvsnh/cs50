#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{
    int cents = -1;
    char input[100];

    // Prompt until valid numeric input greater than 0
    while (cents <= 0)
    {
        printf("Change owed: ");

        // Read input as string
        if (!fgets(input, sizeof(input), stdin))
        {
            continue;
        }

        // Remove trailing newline
        input[strcspn(input, "\n")] = 0;

        // Try to parse to int
        if (sscanf(input, "%d", &cents) != 1 || cents <= 0)
        {
            cents = -1; // Reset for loop
        }
    }

    int coins = 0;
    int coin_values[] = {25, 10, 5, 1};

    for (int i = 0; i < 4; i++)
    {
        coins += cents / coin_values[i];
        cents %= coin_values[i];
    }

    printf("%d\n", coins);
    return 0;
}
