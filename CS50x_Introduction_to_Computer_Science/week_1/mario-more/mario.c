#include <cs50.h>
#include <stdio.h>

int main()
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    for (int i = 0; i < height; i++)
    {
        printf("%*s", height - i - 1, "");
        for (int j = 0; j <= i; j++)
            printf("#");
        printf("  ");
        for (int j = 0; j <= i; j++)
            printf("#");
        printf("\n");
    }
    return 0;
}
