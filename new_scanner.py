class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

class LexicalAnalyzer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def get_char(self):
        if self.pos < len(self.text):
            return self.text[self.pos]
        return None

    def consume_char(self):
        char = self.get_char()
        if char:
            self.pos += 1
        return char

    def skip_spaces(self):
        while self.get_char() in [' ', '\t', '\n']:
            self.consume_char()

    def get_identifier(self):
        identifier = ''
        while self.get_char() and (self.get_char().isalnum() or self.get_char() == '_'):
            identifier += self.consume_char()
        return identifier

    def get_integer(self):
        integer = ''
        while self.get_char() and self.get_char().isdigit():
            integer += self.consume_char()
        return integer

    def get_operator(self):
        operator = ''
        while self.get_char() and self.get_char() in ['+', '-', '*', '<', '>', '&', '.', '@', '/', ':', '=', '˜', '|', '$', '!', '#', '%', 'ˆ', '_', '[', ']', '{', '}', '"', '‘', '?']:
            operator += self.consume_char()
        return operator

    def get_string(self):
        string = ''
        self.consume_char()  # Consume opening single quote
        while True:
            char = self.consume_char()
            if char == "'":
                break
            elif char == '\\':
                escape_char = self.consume_char()
                if escape_char == 't':
                    string += '\t'
                elif escape_char == 'n':
                    string += '\n'
                elif escape_char == '\\':
                    string += '\\'
                elif escape_char == "'":
                    string += "'"
                elif escape_char == '(':
                    string += '('
                elif escape_char == ')':
                    string += ')'
                elif escape_char == ';':
                    string += ';'
                elif escape_char == ',':
                    string += ','
                else:
                    string += escape_char
            else:
                string += char
        return string

    def next_token(self):
        self.skip_spaces()
        char = self.get_char()
        if char is None:
            return Token("EOF", None)
        elif char.isalpha():
            return Token("IDENTIFIER", self.get_identifier())
        elif char.isdigit():
            return Token("INTEGER", self.get_integer())
        elif char in ['+', '-', '*', '<', '>', '&', '.', '@', '/', ':', '=', '˜', '|', '$', '!', '#', '%', 'ˆ', '_', '[', ']', '{', '}', '"', '‘', '?']:
            return Token("OPERATOR", self.get_operator())
        elif char == "'":
            return Token("STRING", self.get_string())
        elif char == '(':
            self.consume_char()
            return Token("Punctuation", "(")
        elif char == ')':
            self.consume_char()
            return Token("Punctuation", ")")
        elif char == ';':
            self.consume_char()
            return Token("Punctuation", ";")
        elif char == ',':
            self.consume_char()
            return Token("Punctuation", ",")
        else:
            # Handle unexpected characters
            self.consume_char()
            return Token("ERROR", char)

    def tokenize(self):
        tokens = []
        while True:
            token = self.next_token()
            if token.token_type == "EOF":
                break
            tokens.append(token)
        return tokens

# Example usage
#text = "let Sum(A) = Psum (A,Order A ) where rec Psum (T,N) = N eq 0 -> 0 | Psum(T,N-1)+T N in Print ( Sum (1,2,3,4,5) )"
with open("input.txt","r") as file:
    text = file.read()

lexer = LexicalAnalyzer(text)
tokens = lexer.tokenize()

for token in tokens:
    print(f"Token type :  {token.token_type:<15}Value : {token.value}")
