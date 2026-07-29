#include <cs50.h>
#include <stdio.h>

int main()
{
    string name;
    name = get_string("What's your name? ");

    printf("hello, %s\n", name);
    return 0;
}
