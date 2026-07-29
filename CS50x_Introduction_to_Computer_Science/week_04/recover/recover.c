#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define BLOCK_SIZE 512

int main(int argc, char *argv[])
{
    // Check usage
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // Open the input file
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    uint8_t buffer[BLOCK_SIZE];
    FILE *img = NULL;
    char filename[8];
    int img_count = 0;

    // Read blocks until end of file
    while (fread(buffer, sizeof(uint8_t), BLOCK_SIZE, card) == BLOCK_SIZE)
    {
        // Check for JPEG signature
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // If already writing a JPEG, close it
            if (img != NULL)
            {
                fclose(img);
            }
            // Create new JPEG file
            sprintf(filename, "%03i.jpg", img_count);
            img = fopen(filename, "w");
            img_count++;
        }

        // If a JPEG file is open, write the block
        if (img != NULL)
        {
            fwrite(buffer, sizeof(uint8_t), BLOCK_SIZE, img);
        }
    }

    // Close last JPEG if open
    if (img != NULL)
    {
        fclose(img);
    }
    fclose(card);
    return 0;
}
