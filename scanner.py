import re

# Token patterns
patterns = [
    ('IDENTIFIER', r'[a-zA-Z][a-zA-Z0-9_]*'),
    ('INTEGER', r'\d+'),
    ('OPERATOR', r'[+\-<>&.@/:=~|$!#%^_\[\]{}"\?]+'),
    ('STRING', r"''''(\\t|\\n|\\\|\\''''|\(|\)|;|,| |[a-zA-Z0-9+\-<>&.@/:=~|$!#%^_\[\]{}\"?\t\n])*''''"),
    ('DELETE', r'( |\t|\n)+'),
    ('PUNCTUATION', r'[();,]'),
    # ('COMMENT', r'//(\'\'\'\'|\(\)|;|,|\\| |\t|\n|[a-zA-Z0-9+\-<>&.@/:=~|$!#%^_\[\]{}\"?\(\)\[\];,])*\n'),
    ('COMMENT', r'//.*')]

def scanner(input_text):
    tokens = []
    while input_text:
        match = None
        for token_type, pattern in patterns:
            regex = re.compile(pattern)
            match = regex.match(input_text)
            if match:
                value = match.group(0)
                if token_type != 'DELETE' and token_type != 'COMMENT':
                    tokens.append((token_type, value))
                input_text = input_text[len(value):]
                break
        if not match:
            raise ValueError("Invalid input at: " + input_text)
    return tokens

# Take input from the user
# user_input = input("Enter your code: ")
input="""
''''This is a sample input string''''
foo = 123;
bar = 456;
"""
# input="let Sum(A) = Psum (A,Order A ) where rec Psum (T,N) = N eq 0 -> 0 | Psum(T,N-1)+T N in Print ( Sum (1,2,3,4,5) )"
tokens = scanner(input)
# print(tokens)
for token in tokens:

    print("The token type: '",token[0],"'" ,"   Value: ", token[1])
    # print("/n")
