#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#define MAX_INPUT_SIZE 1024
#define MAX_TOKENS_SIZE 100

// Token type enumeration
typedef enum {
    IDENTIFIER,
    INTEGER,
    OPERATOR,
    STRING,
    DELETE,
    PUNCTUATION,
    COMMENT,
    INVALID
} TokenType;

// Token structure
typedef struct {
    TokenType type;
    char *value;
} Token;

// Tokenize the input text
Token *tokenize(const char *input_text) {
    Token *tokens = NULL;
    int num_tokens = 0;
    int i = 0;
    while (input_text[i] != '\0') {
        TokenType type = get_token_type(input_text[i]);
        if (type == DELETE) {
            // Skip whitespaces
            while (input_text[i] == ' ' || input_text[i] == '\t' || input_text[i] == '\n') {
                i++;
            }
            continue;
        }
        if (type == COMMENT && input_text[i+1] == '*') {
            // Skip comments
            while (input_text[i] != '*' || input_text[i+1] != '/') {
                i++;
            }
            i += 2;
            continue;
        }
        if (type == INTEGER) {
            // Read the integer value
            int start = i;
            while (is_digit(input_text[i])) {
                i++;
            }
            // Create a new token
            Token *new_token = (Token *) malloc(sizeof(Token));
            new_token->type = INTEGER;
            new_token->value = (char *) malloc(i - start + 1);
            strncpy(new_token->value, input_text + start, i - start);
            new_token->value[i - start] = '\0';
            // Add the new token to the list
            tokens = (Token *) realloc(tokens, sizeof(Token) * (num_tokens + 1));
            tokens[num_tokens] = *new_token;
            num_tokens++;
            continue;
        }
        if (type == IDENTIFIER || type == OPERATOR || type == PUNCTUATION) {
            // Read the token value
            int start = i;
            while (get_token_type(input_text[i]) == type) {
                i++;
            }
            // Create a new token
            Token *new_token = (Token *) malloc(sizeof(Token));
            new_token->type = type;
            new_token->value = (char *) malloc(i - start + 1);
            strncpy(new_token->value, input_text + start, i - start);
            new_token->value[i - start] = '\0';
            // Add the new token to the list
            tokens = (Token *) realloc(tokens, sizeof(Token) * (num_tokens + 1));
            tokens[num_tokens] = *new_token;
            num_tokens++;
            continue;
        }
        if (type == STRING) {
            // Read the string value
            int start = i + 2;
            int end = start;
            while (input_text[end] != '\0' && (input_text[end] != '\'' || input_text[end-1] == '\\')) {
                end++;
            }
            if (input_text[end] != '\'') {
                printf("Error: Unmatched string literal\n");
                exit(1);
            }
            // Create a new token
            Token *new_token = (Token *) malloc(sizeof(Token));
            new_token->type = STRING;
            new_token->value = (char *) malloc(end - start + 1);
            strncpy(new_token->value, input_text + start, end - start);
            new_token->value[end - start] = '\0';
            // Add the new token to the list
            tokens = (Token *) realloc(tokens, sizeof(Token) * (num_tokens + 1));
            tokens[num_tokens] = *new_token;
            num_tokens++;
            i = end + 1;
            continue;
        }
        if (type == INVALID) {
            printf("Error: Invalid input at %d: %c\n", i, input_text[i]);
            exit(1);
        }
    }
    return tokens;
}

// Free the memory used by the tokens
void free_tokens(Token *tokens, int num_tokens) {
    for (int i = 0; i < num_tokens; i++) {
        free(tokens[i].value);
    }
    free(tokens);
}

// Check if a character is a letter
bool is_letter(char c) {
    return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z');
}

// Check if a character is a digit
bool is_digit(char c) {
    return c >= '0' && c <= '9';
}

// Check if a character is an operator
bool is_operator(char c) {
    return (c == '+') || (c == '-') || (c == '<') || (c == '>') || (c == '&') ||
           (c == '.') || (c == '@') || (c == '/') || (c == ':') || (c == '=') ||
           (c == '~') || (c == '|') || (c == '$') || (c == '!') || (c == '#') ||
           (c == '%') || (c == '^') || (c == '_') || (c == '[') || (c == ']') ||
           (c == '{') || (c == '}') || (c == '\"') || (c == '?') || (c == '(') ||
           (c == ')') || (c == ';') || (c == ',') || (c == '\\') || (c == '`') ||
           (c == '~') || (c == '\'');
}

// Get the token type based on a character
TokenType get_token_type(char c) {
    if (is_letter(c)) {
        return IDENTIFIER;
    }
    if (is_digit(c)) {
        return INTEGER;
    }
    if (is_operator(c)) {
        return OPERATOR;
    }
    if (c == ' ' || c == '\t' || c == '\n') {
        return DELETE;
    }
    if (c == ';' || c == ',' || c == '(') {
        return PUNCTUATION;
    }
    if (c == '/' && *(input + 1) == '*') {
        return COMMENT;
    }
    return INVALID;
}

int main() {
    // Take input from the user
    printf("Enter your code: ");
    char input[MAX_INPUT_SIZE];
    fgets(input, sizeof(input), stdin);
    input[strcspn(input, "\n")] = '\0';

    // Tokenize the input
    Token *tokens = tokenize(input);

    // Print the tokens
    for (int i = 0; i < 33; i++) {
        printf("The token type: '%s'   Value: %s\n",
            token_type_str[tokens[i].type], tokens[i].value);
    }

    // Free the memory used by the tokens
    free_tokens(tokens, 33);

    return 0;
}