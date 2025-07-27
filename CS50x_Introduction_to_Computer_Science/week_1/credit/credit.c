#include <cs50.h>
#include <stdio.h>

int main()
{
    long card;

    // Prompt user for a valid credit card number
    do
    {
        card = get_long("Number: ");
    }
    while (card < 0);

    // Determine the length of the card number
    int length = 0;
    long tempCard = card;

    while (tempCard > 0)
    {
        length++;
        tempCard /= 10;
    }

    // Card number should be 13, 15, or 16 digits long
    if (length != 13 && length != 15 && length != 16)
    {
        printf("INVALID\n");
        return 0;
    }

    int sum1 = 0, sum2 = 0, total = 0;
    tempCard = card;

    // Luhn's Algorithm: Validate the card number
    while (tempCard > 0)
    {
        // Add the last digit directly to sum1
        sum1 += tempCard % 10;
        tempCard /= 10;

        // Take the next digit, multiply by 2, and sum its digits
        if (tempCard > 0)
        {
            int doubled = (tempCard % 10) * 2;
            sum2 += (doubled / 10) + (doubled % 10);
            tempCard /= 10;
        }
    }

    total = sum1 + sum2;

    // If the total sum is not a multiple of 10, it's an invalid card
    if (total % 10 != 0)
    {
        printf("INVALID\n");
        return 0;
    }

    // Extract the starting digits of the card
    long start = card;
    while (start >= 100)
    {
        start /= 10;
    }

    // Determine the card type based on length and starting digits
    if ((length == 13 || length == 16) && (start / 10 == 4))
    {
        printf("VISA\n");
    }
    else if (length == 15 && (start == 34 || start == 37))
    {
        printf("AMEX\n");
    }
    else if (length == 16 && (start >= 51 && start <= 55))
    {
        printf("MASTERCARD\n");
    }
    else
    {
        printf("INVALID\n");
    }

    return 0;
}
