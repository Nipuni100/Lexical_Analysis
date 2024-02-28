#include <stdio.h>
#include <ctype.h>


//Check whether it is a string.
int isValidString(const char *str) {
    // Check if the string is not empty
    if (*str == '\0') {
        return 0; // Invalid if empty
    }

    // Check if the first character is a letter
    if (!isalpha(*str)) {
        return 0; // Invalid if not a letter
    }

    int firstCharProcessed = 0;

    // Iterate through the rest of the string
   while (*str != '\0' && *str != ' ' && *str != '\t' && *str != '\n') {
    // Check if the character is a letter, digit, or underscore
    if (firstCharProcessed && !isalnum(*str) && *str != '_') {
        return 0; // Invalid if not a letter, digit, or underscore after the first character
    }

    // If the character is an underscore, mark that the first character is processed
    if (*str == '_') {
        firstCharProcessed = 1;
    }

    str++; // Move to the next character
}


    return 1; // String is valid
}

int isInteger(const char *str) {
    // Iterate through the string
    while (*str != '\0' && *str != ' ' && *str != '\t' && *str != '\n') {
        // Check if the character is not a digit
        if (!isdigit(*str)) {
            return 0; // Invalid if not a digit
        }

        str++; // Move to the next character
    }

    return 1; // String is valid (contains only digits)
}

int isOperator(const char *str) {
    // Iterate through the string
    while (*str != '\0' && *str != ' ' && *str != '\t' && *str != '\n') {
        // Check if the character is a valid operator symbol
        switch (*str) {
            case '+':
            case '-':
            case '*':
            case '<':
            case '>':
            case '&':
            case '.':
            case '@':
            case '/':
            case ':':
            case '=':
            case '~':
            case '|':
            case '$':
            case '!':
            case '#':
            case '%':
            case '^':
            case '_':
            case '[':
            case ']':
            case '{':
            case '}':
            case '"':
            case '‘':
            case '?':
                break; // Valid operator symbol
            default:
                return 0; // Invalid if not a valid operator symbol
        }

        str++; // Move to the next character
    }

    return 1; // String is valid (contains only valid operator symbols)
}

int isString(const char *str) {
    // Check if the string starts with "''''"
    if (str[0] != '\'' || str[1] != '\'' || str[2] != '\'' || str[3] != '\'') {
        return 0; // Invalid if it doesn't start with "''''"
    }

    // Skip the starting "''''"
    str += 4;

    // Iterate through the rest of the string
    while (*str != '\0') {
        // Check for valid escape sequences
        if (*str == '\\' && (str[1] == 't' || str[1] == 'n' || str[1] == '\\' || str[1] == '\'')) {
            str += 2; // Skip the escape sequence
        }
        // Check for valid characters inside the string
        else if (!(isalnum(*str) || ispunct(*str) || isspace(*str))) {
            return 0; // Invalid character inside the string
        }

        // Check if the string ends with "''''"
        if (str[0] == '\'' && str[1] == '\'' && str[2] == '\'' && str[3] == '\'') {
            return 1; // Valid 'String'
        }

        str++; // Move to the next character
    }

    return 0; // No ending "''''"
}

int isPunctuation(const char *str) {
    // Check if the string is one of the specified punctuations
    switch (*str) {
        case '(':
        case ')':
        case ';':
        case ',':
            // Check if the next character is a null terminator
            if (*(str + 1) == '\0' || *(str + 1) == '\n' || *(str + 1) == ' ' || *(str + 1) == '\t') {
                return 1; // Valid single punctuation
            } else {
                return 0; // More than one symbol is invalid
            }
        default:
            return 0; // Not a valid punctuation
    }
}


int isComment(const char *str) {
    // Check if the string starts with "//"
    if (str[0] != '/' || str[1] != '/') {
        return 0; // Invalid if it doesn't start with "//"
    }

    // Skip the starting "//"
    str += 2;

    // Iterate through the rest of the string
    while (*str != '\0' && *str != '\n') {
        // Check for valid characters inside the comment
        if (!(isalnum(*str) || ispunct(*str) || isspace(*str) || *str == '\t')) {
            return 0; // Invalid character inside the comment
        }

        str++; // Move to the next character
    }

    // Check if the comment ends with Eol
    if (*str == '\n') {
        return 1; // Valid comment
    }

    return 0; // No ending Eol
}



int main(){

    // char input[100]; // Assuming a maximum input length of 100 characters

    // // Taking input from the user
    // printf("Enter a string: ");
    // scanf("%s", input);

    // // Checking if the input string is valid
    // if (isValidString(input)) {
    //     printf("The input string is valid.\n");
    // } else {
    //     printf("The input string is invalid.\n");
    // }

    // return 0;

    // if (isInteger(input)) {
    //     printf("The input string is an integer.\n");
    // } else {
    //     printf("The input string is not an integer.\n");
    // }

    // return 0;

    // if (isOperator(input)) {
    //     printf("The input string contains only valid operator symbols.\n");
    // } else {
    //     printf("The input string contains invalid characters or is not a valid operator.\n");
    // }

    // return 0;

    // if (isOperator(input)) {
    //     printf("The input string contains only valid operator symbols.\n");
    // } else {
    //     printf("The input string contains invalid characters or is not a valid operator.\n");
    // }

    char input[100]; // Assuming a maximum input length of 1000 characters

    // Taking input from the user
    printf("Enter a string: ");
    fgets(input, sizeof(input), stdin);

    // Checking if the input string is a valid 'String'
    if (isPunctuation(input)) {
        printf("The input is a valid punctuation.\n");
    } else {
        printf("The input is not a valid punctuation.\n");
    }

    return 0;
}
