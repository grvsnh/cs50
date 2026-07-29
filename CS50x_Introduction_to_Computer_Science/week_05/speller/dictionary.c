#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Hash word to obtain index
    int index = hash(word);

    // Traverse linked list at the hashed bucket
    for (node *tmp = table[index]; tmp != NULL; tmp = tmp->next)
    {
        // Case-insensitive comparison of dictionary word and input word
        if (strcasecmp(tmp->word, word) == 0)
        {
            return true;
        }
    }

    // Word not found in dictionary
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned int hash_value = 0;

    // Compute hash value using bit-shifting and XOR of uppercase letters
    for (int i = 0; word[i] != '\0'; i++)
    {
        hash_value = (hash_value << 2) ^ toupper(word[i]);
    }

    // Ensure hash value fits in table size
    return hash_value % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open dictionary file for reading
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        fprintf(stderr, "Could not open dictionary.\n");
        return false;
    }

    // Initialize hash table buckets to NULL
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }

    char word[LENGTH + 1];

    // Read each word from dictionary file
    while (fscanf(file, "%s", word) != EOF)
    {
        // Allocate memory for a new node
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            fclose(file);
            fprintf(stderr, "Out of memory.\n");
            return false;
        }

        // Copy word into node
        strcpy(new_node->word, word);

        // Hash word to obtain index for insertion
        int index = hash(word);

        // Insert node at beginning of linked list in hash table bucket
        new_node->next = table[index];
        table[index] = new_node;
    }

    // Close dictionary file
    fclose(file);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    int count = 0;

    // Traverse each bucket in the hash table
    for (int i = 0; i < N; i++)
    {
        // Traverse linked list at this bucket and count nodes
        for (node *tmp = table[i]; tmp != NULL; tmp = tmp->next)
        {
            count++;
        }
    }

    return count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // Traverse each bucket in the hash table
    for (int i = 0; i < N; i++)
    {
        // Free nodes within the linked list at this bucket
        while (table[i] != NULL)
        {
            node *tmp = table[i]->next;
            free(table[i]);
            table[i] = tmp;
        }
    }

    return true;
}
