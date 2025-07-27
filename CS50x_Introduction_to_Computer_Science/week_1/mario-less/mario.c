#include <cs50.h>
#include <stdio.h>

void print_pyramid(int h)
{
    for (int i = 1; i <= h; i++)
    {
        for (int j = 0; j < h - i; j++)
            printf(" ");
        for (int j = 0; j < i; j++)
            printf("#");
        printf("\n");
    }
}

int main(void)
{
    int h;

    // Get a positive height from the user
    do
    {
        h = get_int("Height: ");
    }
    while (h <= 0);

    // Print the pyramid without extra text
    print_pyramid(h);
}
