class Token:
    """
    This is for each token in the program file.
    """
    def __init__(self, type, value):
        # each token has it's type and a vlaue
        self.type = type
        self.value = value

class Tokenizer:
    """
    Tokens can be extracted and labelled from a file using this class.
    """
    def __init__(self):
        # set of states in the FA
        self.states = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22}

        # set of accepting states of FA
        self.final_states = {1, 2, 3, 4, 5, 8, 14, 15, 16, 17, 18, 19}

        # initial state
        self.curr_state = 0

        # mapping state with respective transition functions
        self.transition_table = {0: 'trans_at_0', 1: 'trans_at_1', 2: 'trans_at_2', 3: 'trans_at_3',
                                 4: 'trans_at_4', 5: 'trans_at_5', 6: 'trans_at_6', 7: 'trans_at_7',
                                 8: 'trans_at_8', 9: 'trans_at_9', 10: 'trans_at_10',
                                 11: 'trans_at_11',
                                 12: 'trans_at_12', 13: 'trans_at_13', 14: 'trans_at_14',
                                 15: 'trans_at_15',
                                 16: 'trans_at_16', 17: 'trans_at_17', 18: 'trans_at_18',
                                 19: 'trans_at_19',
                                 20: 'trans_at_20', 21: 'trans_at_21', 22: 'trans_at_22'
                                 }

        # initial token is an empty string
        self.curr_token = ''

        # keeps the picked tokens
        self.picked_tokens = []

        # position of the character being read in the current line. Used for finding position of lexical violation
        self.char_pos = 0

        # the current line being read
        self.line_number = 0

        # associating states with respective labels
        self.state_labels = {1: "<IDENTIFIER>", 2: "<INTEGER>", 3: "<OPERATOR>", 4: "<OPERATOR>", 5: "<OPERATOR>",
                             8: "<DELETE>", 14: "<STRING>", 15: "<DELETE>", 16: ")", 17: "(", 18: ";", 19: ","}

        # special keywords
        self.keywords = ['let', 'in', 'fn', 'where', 'aug', 'or', 'not', 'gr', 'ge', 'ls', 'le', 'eq', 'ne', 'true',
                         'false', 'nil', 'dummy', 'within', 'and', 'rec']

        # operator symbol
        self.operator_symbols = ['+', '-', '*', '<', '>', '&', '.', '@', '/', ':', '=', '~', '|', '$', '!', '#', '%',
                                 '^', '_', '[', ']',
                                 '{', '}', '"', "`", '?']

        # digit
        self.digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        # letter
        self.letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                        'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                        't', 'u', 'v', 'w', 'x', 'y', 'z']

        self.white_space = chr(32)
        self.horizontal_tab = chr(9)
        self.end_of_line = chr(10)

    '''this reset() function resets the finite automaton to the initial state, 
    and collect the tokens if those tokens are acceptable'''
    def reset(self):
        """
        This function add completed tokens into the picked_tokens list and notify lexical violations if there are any
        """
        if self.curr_state in self.final_states:
            self.picked_tokens.append(Token(self.state_labels[self.curr_state], self.curr_token))
            self.curr_state = 0
            self.curr_token = ''

        else:
            print(self.curr_token, self.curr_state)
            raise Exception("Lexical Rules Violated in line:%d at position:%d." % (self.line_number, self.char_pos))

    '''
    -------------------------Beginning of Transition Functions---------------------------
    '''

    def trans_at_0(self, c):
        ope_sym_4 = self.operator_symbols.copy()
        ope_sym_4.remove('/')
        if c in self.letters:
            self.curr_state = 1
            self.curr_token += c
            self.char_pos += 1
        elif c in self.digits:
            self.curr_state = 2
            self.curr_token += c
            self.char_pos += 1
        elif c == '/':
            self.curr_state = 3
            self.curr_token += c
            self.char_pos += 1
        elif c in ope_sym_4:
            self.curr_state = 4
            self.curr_token += c
            self.char_pos += 1
        elif c == "'":
            self.curr_state = 10
            self.curr_token += c
            self.char_pos += 1
        elif c in [self.white_space, self.horizontal_tab]:
            self.curr_state = 15
            self.curr_token += c
            self.char_pos += 1
        elif c == ")":
            self.curr_state = 16
            self.curr_token += c
            self.char_pos += 1
        elif c == "(":
            self.curr_state = 17
            self.curr_token += c
            self.char_pos += 1
        elif c == ";":
            self.curr_state = 18
            self.curr_token += c
            self.char_pos += 1
        elif c == ",":
            self.curr_state = 19
            self.curr_token += c
            self.char_pos += 1
        elif c == "\\":
            self.curr_state = 21
            self.curr_token += c
            self.char_pos += 1

        else:
            # set the state to 0, and collect the scanned token so far and prepare FA for scanning next token
            self.reset()

    def trans_at_1(self, c):
        if (c in self.letters) or (c in self.digits) or (c == "_"):
            self.curr_state = 1
            self.curr_token += c
            self.char_pos += 1
        else:
            self.reset()

    def trans_at_2(self, c):
        if c in self.digits:
            self.curr_state = 2
            self.curr_token += c
            self.char_pos += 1
        else:
            self.reset()

    def trans_at_3(self, c):
        op_sym_set_3 = self.operator_symbols.copy()
        op_sym_set_3.remove('/')  # getting set of symbols triggers a specific transition at state 3

        if c in op_sym_set_3:
            self.curr_state = 4
            self.curr_token += c
            self.char_pos += 1
        elif c == '/':
            self.curr_state = 5
            self.curr_token += c
            self.char_pos += 1
        else:
            self.reset()

    def trans_at_4(self, c):
        if c in self.operator_symbols:
            self.curr_state = 4
            self.curr_token += c
            self.char_pos += 1
        else:
            self.reset()

    def trans_at_5(self, c):
        if c in self.operator_symbols:
            self.curr_state = 5
            self.curr_token += c
            self.char_pos += 1
        elif c == "\\":
            self.curr_state = 20
            self.curr_token += c
            self.char_pos += 1
        elif c == "'":
            self.curr_state = 7
            self.curr_token += c
            self.char_pos += 1

        # chr(92) = \
        elif (c in self.letters) or (c in self.digits) or (
                c in [self.horizontal_tab, self.white_space, '(', ')', ';', ',', chr(92)]):
            self.curr_state = 7
            self.curr_token += c
            self.char_pos += 1
        else:
            self.reset()

    # def trans_at_6(self, c):
    #     if c == "'":
    #         self.curr_state = 7
    #         self.curr_token += c
    #         self.char_pos += 1
    #     else:
    #         self.reset()

    def trans_at_7(self, c):

        if (c in self.letters) or (c in self.digits) or (c in self.operator_symbols) or (
                c in [self.horizontal_tab, self.white_space, '(', ')', ';', ',', "'"]):
            self.curr_state = 7
            self.curr_token += c
            self.char_pos += 1
        elif c == '\\':
            self.curr_state = 20
            self.curr_token += c
            self.char_pos += 1
        else:
            self.reset()

    def trans_at_8(self, c):
        self.reset()

    # def trans_at_9(self, c):
    #     if c == "'":
    #         self.curr_state = 10
    #         self.curr_token += c
    #         self.char_pos += 1
    #     else:
    #         self.reset()

    def trans_at_10(self, c):
        if (c in self.letters) or (c in self.digits) or (c in self.operator_symbols) or (
                c in [self.white_space, '(', ')', ';', ',']):
            self.curr_state = 10
            self.curr_token += c
            self.char_pos += 1
        elif c == "/":
            self.curr_state = 11
            self.curr_token += c
            self.char_pos += 1

        elif c == "'":
            self.curr_state = 14
            self.curr_token += c
            self.char_pos += 1
        else:
            self.reset()

    def trans_at_11(self, c):
        if c == 't' or c == 'n' or c == '/':
            self.curr_state = 10
            self.curr_token += c
            self.char_pos += 1
        elif c == "'":
            self.curr_state = 12
            self.curr_token += c
            self.char_pos += 1
        else:
            self.reset()

    def trans_at_12(self, c):
        if c == "'":
            self.curr_state = 10
            self.curr_token += c
            self.char_pos += 1
        else:
            self.reset()


    def trans_at_14(self, c):
        self.reset()

    def trans_at_15(self, c):
        if c in [self.white_space, self.horizontal_tab]:
            self.curr_state = 15
            self.curr_token += c
            self.char_pos += 1
        elif c == "\\":
            self.curr_state = 22
            self.curr_token += c
            self.char_pos += 1
        else:
            self.reset()

    def trans_at_16(self, c):
        self.reset()

    def trans_at_17(self, c):
        self.reset()

    def trans_at_18(self, c):
        self.reset()

    def trans_at_19(self, c):
        self.reset()

    def trans_at_20(self, c):
        if c == "n":
            self.curr_state = 8
            self.curr_token += c
            self.char_pos += 1
        elif (c in self.letters) or (c in self.digits) or (c in self.operator_symbols) or (
                c in [self.horizontal_tab, self.white_space, '(', ')', ';', ',']):
            self.curr_state = 7
            self.curr_token += c
            self.char_pos += 1
        elif c == '\\':
            self.curr_state = 20
            self.curr_token += c
            self.char_pos += 1
        else:
            self.reset()

    def trans_at_21(self, c):
        if c == "n" or "t":
            self.curr_state = 15
            self.curr_token += c
            self.char_pos += 1
        else:
            self.reset()

    def trans_at_22(self, c):
        if c == "n" or "t":
            self.curr_state = 15
            self.curr_token += c
            self.char_pos += 1
        else:
            self.reset()

    '''
    ----------------------------------------------------------------------------------
    '''

    def scanner(self):
        """
        This is the scanner which removes the unnecessary white spaces, tab space and EOLs.
        
        """
        screened_tokens = []

        for token in self.picked_tokens:
            # Separating keywords from the <IDENTIFIER> tokens.
            if token.value in self.keywords:
                token.type = '<KEYWORD>'

            # Removing tokens from <DELETE> type: white space, tabs, EOL, and comments.
            if token.type == '<DELETE>':
                continue

            screened_tokens.append(token)
        self.picked_tokens = screened_tokens

    def tokenize(self, file):
        """
        This function tokenizes the input file and output list of tokens which is filtered.
        """
        try:
            # open the file to tokenize it
            with open(file, 'r') as file:

                # this loop is for reading and tokenizing each line
                for line in file:

                    characters = list(repr(line)[1:-1])  # raw string representation to capture the EOL character as it is
                    self.line_number += 1
                    self.char_pos = 0

                    while self.char_pos < len(characters):

                        f = self.transition_table[self.curr_state]
                        i = characters[self.char_pos]
                        # print(f, i)
                        match f:
                            case 'trans_at_0':
                                self.trans_at_0(i)
                            case 'trans_at_1':
                                self.trans_at_1(i)
                            case 'trans_at_2':
                                self.trans_at_2(i)
                            case 'trans_at_3':
                                self.trans_at_3(i)
                            case 'trans_at_4':
                                self.trans_at_4(i)
                            case 'trans_at_5':
                                self.trans_at_5(i)
                            # case 'trans_at_6':
                            #     self.trans_at_6(i)
                            case 'trans_at_7':
                                self.trans_at_7(i)
                            case 'trans_at_8':
                                self.trans_at_8(i)
                            # case 'trans_at_9':
                            #     self.trans_at_9(i)
                            case 'trans_at_10':
                                self.trans_at_10(i)
                            case 'trans_at_11':
                                self.trans_at_11(i)
                            case 'trans_at_12':
                                self.trans_at_12(i)
                            # case 'trans_at_13':
                            #     self.trans_at_13(i)
                            case 'trans_at_14':
                                self.trans_at_14(i)
                            case 'trans_at_15':
                                self.trans_at_15(i)
                            case 'trans_at_16':
                                self.trans_at_16(i)
                            case 'trans_at_17':
                                self.trans_at_17(i)
                            case 'trans_at_18':
                                self.trans_at_18(i)
                            case 'trans_at_19':
                                self.trans_at_19(i)
                            case 'trans_at_20':
                                self.trans_at_20(i)
                            case 'trans_at_21':
                                self.trans_at_21(i)
                            case 'trans_at_22':
                                self.trans_at_22(i)

                    # this reset invocation is for accepting states like 1,2,4,5,15 (accepting states and have
                    # transitions) when token belong to those states is collected till the end of the line,
                    # we have to break the token before moving to the next line.
                    self.reset()

            # by calling scanner function , we remove unwanted spaces, EOLs and tabs
            self.scanner()
            return self.picked_tokens
        except FileNotFoundError:
            print("File not found!")
            exit()

# # For debugging purpose
# tokenizer = Tokenizer()
# tokens = tokenizer.tokenize('input.txt')


# for token in tokens:
#     print(f"Token type :  {token.type:<15}Value : {token.value}")