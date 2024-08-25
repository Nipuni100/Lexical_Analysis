# from LexicalAnalyzer import Tokenizer
from LexicalAnalyzer import Token
from LexicalAnalyzer import Tokenizer
from TreeNodes import TreeNode


class RPALParser:
    def __init__(self):
        # tokenizer for extracting tokens
        self.tokenizer = Tokenizer()

        # keeps the tokens in the input file
        self.tokens = []

        # tracks the current token index
        self.curr_idx = 0

        # current token that has been parsed
        self.curr_token = None

        # stack for AST node building
        self.stack = []

        # AST output of parser
        self.output_AST = ''

    """
    -------------Functions needed for the process of building the tree, identifying the next token and reading the token----------------
    """

    def token_extraction(self, file):
        """
        This function uses the Tokenizer to extract token from the given file.
    
        """
        self.tokens = self.tokenizer.tokenize(file)
        self.curr_token = self.tokens[self.curr_idx]
        return

    def read_token(self, value):
        """
        This function consumes the current token if it matches the required token's value.
        Otherwise, throws Exception saying syntax error occurred.
    
        """
        # # For debugging.
        # for i in self.stack:
        #     print(i.value, end=', ')
        # print()

        # Check for value
        if self.curr_token.value == value:
            self.curr_idx += 1
            # moving to next token
            if self.curr_idx < len(self.tokens):
                self.curr_token = self.tokens[self.curr_idx]
            else:
                self.curr_token = Token("<END>", 'END')
        else:
            # For tracking the parsed token when there is syntax error is encountered.
            for t in self.tokens[:self.curr_idx]:
                print(t.value, end=', ')

            # Raising exception during syntax rules violation
            raise Exception("Syntax Error: %s is expected near %s."
                            % (value, self.tokens[self.curr_idx - 1].value))
        return

    def read_token_by_type(self, type):
        """
        This function consumes the current token if it matches the required token's type.
        Otherwise, throws Exception saying syntax error occurred.
    
        """
        # # For debugging
        # for i in self.stack:
        #     print(i.value, end=', ')

        # Check for type
        if self.curr_token.type == type:
            self.curr_idx += 1  # increment current token index

            match self.curr_token.type:
                case "<IDENTIFIER>":
                    self.stack.append(TreeNode("<%s:%s>" % ("ID", self.tokens[self.curr_idx - 1].value)))
                case "<INTEGER>":
                    self.stack.append(TreeNode("<%s:%s>" % ("INT", self.tokens[self.curr_idx - 1].value)))
                case "<STRING>":
                    self.stack.append(TreeNode("<%s:%s>" % ("STR", self.tokens[self.curr_idx - 1].value)))

            # moving to next token
            if self.curr_idx < len(self.tokens):
                self.curr_token = self.tokens[self.curr_idx]
            else:
                self.curr_token = Token("<END>", 'END')
        else:
            # Raising exception during syntax rules violation
            raise Exception("Syntax Error: %s type is expected near %s." % (type, self.curr_token.value))
        return

    def build_tree(self, value, n):
        """
        This function build pops the nodes from the stack, makes them the child of the parent
        , and pushes the parent back to stack.
    
        """
        parent = TreeNode(value)
        for i in range(n):
            parent.add_child(self.stack.pop())
        self.stack.append(parent)
        return

    '''
    ---------------The functions to check whether the input is according too the RPAL grammar-------------------
    '''

    def Proc_E(self):

        match self.curr_token.value:
            case 'let':
                self.read_token('let')
                self.Proc_D()
                self.read_token('in')
                self.Proc_E()

                # print('E -> ’let’ D ’in’ E')

                self.build_tree('let', 2)  # building 'let' node
            case 'fn':
                self.read_token('fn')

                self.Proc_Vb()
                n = 1

                while self.curr_token.value == "(" or self.curr_token.type == "<IDENTIFIER>":
                    self.Proc_Vb()
                    n += 1
                self.read_token('.')
                self.Proc_E()
                # print('E -> ’fn’ Vb+ ’.’ E')
                self.build_tree('lambda', n + 1)  # building 'lambda' node
            case _:
                self.Proc_Ew()
                # print('E -> Ew')
        return

    def Proc_Ew(self):
        self.Proc_T()

        if self.curr_token.value == 'where':
            self.read_token('where')
            self.Proc_Dr()
            # print('Ew -> T ’where’ Dr')
            self.build_tree('where', 2)  # building 'where' node
            return
        # print('Ew -> T')
        return

    def Proc_T(self):
        self.Proc_Ta()

        if self.curr_token.value == ',':
            self.read_token(',')
            self.Proc_Ta()

            n = 1
            while self.curr_token.value == ',':
                self.read_token(',')
                self.Proc_Ta()
                n += 1
            # print('T -> Ta ( ’,’ Ta )+')
            self.build_tree('tau', n + 1)  # building 'tau' node
            return
        # print('T -> Ta ')
        return

    def Proc_Ta(self):

        self.Proc_Tc()
        # print('Ta -> Tc')

        while self.curr_token.value == 'aug':
            self.read_token('aug')
            self.Proc_Tc()
            # print('Ta -> Ta ’aug’ Tc')
            self.build_tree('aug', 2)
        return

    def Proc_Tc(self):

        self.Proc_B()

        if self.curr_token.value == '->':
            self.read_token('->')
            self.Proc_Tc()
            self.read_token('|')
            self.Proc_Tc()
            # print('Tc -> B ’->’ Tc ’|’ Tc')
            self.build_tree('->', 3)
            return
        # print('Tc -> B')
        return

    def Proc_B(self):

        self.Proc_Bt()
        # print('B -> Bt')

        while self.curr_token.value == 'or':
            self.read_token('or')
            self.Proc_Bt()
            # print('B ->B’or’ Bt')
            self.build_tree('or', 2)
        return

    def Proc_Bt(self):

        self.Proc_Bs()
        # print('Bt -> Bs')
        while self.curr_token.value == '&':
            self.read_token('&')
            self.Proc_Bs()
            # print('Bt -> Bt ’&’ Bs')
            self.build_tree('&', 2)
        return

    def Proc_Bs(self):

        if self.curr_token.value == 'not':
            self.read_token('not')
            self.Proc_Bp()
            # print('Bs -> ’not’ Bp')
            self.build_tree('not', 1)
        else:
            self.Proc_Bp()
            # print('Bs -> Bp')
        return

    def Proc_Bp(self):
        self.Proc_A()

        match self.curr_token.value:
            case 'gr':
                self.read_token('gr')
                self.Proc_A()
                # print('Bp -> A ’gr’ A')
                self.build_tree('gr', 2)
            case '>':
                self.read_token('>')
                self.Proc_A()
                # print('Bp -> A ’>’ A')
                self.build_tree('gr', 2)
            case 'ge':
                self.read_token('ge')
                self.Proc_A()
                # print('Bp -> A ’ge’ A')
                self.build_tree('ge', 2)
            case '>=':
                self.read_token('>=')
                self.Proc_A()
                # print('Bp -> A ’>=’ A')
                self.build_tree('ge', 2)
            case 'ls':
                self.read_token('ls')
                self.Proc_A()
                # print('Bp -> A ’ls’ A')
                self.build_tree('ls', 2)
            case '<':
                self.read_token('<')
                self.Proc_A()
                # print('Bp -> A ’<’ A')
                self.build_tree('ls', 2)
            case 'le':
                self.read_token('le')
                self.Proc_A()
                # print('Bp -> A ’le’ A')
                self.build_tree('le', 2)
            case '<=':
                self.read_token('<=')
                self.Proc_A()
                # print('Bp -> A ’<=’ A')
                self.build_tree('le', 2)
            case 'eq':
                self.read_token('eq')
                self.Proc_A()
                # print('Bp -> A ’eq’ A')
                self.build_tree('eq', 2)
            case 'ne':
                self.read_token('ne')
                self.Proc_A()
                # print('Bp -> A ’ne’ A')
                self.build_tree('ne', 2)
            case _:
                # print('Bp -> A')
                pass
        return

    # Checked & Fixed
    def Proc_A(self):

        if self.curr_token.value == '+':
            self.read_token('+')
            self.Proc_At()
            # print('A ->’+’ At')

        elif self.curr_token.value == '-':
            self.read_token('-')
            self.Proc_At()
            # print('A ->’-’ At')
            self.build_tree('neg', 1)

        else:
            self.Proc_At()
            # print('A -> At')

        while self.curr_token.value == '+' or self.curr_token.value == '-':
            if self.curr_token.value == '+':
                self.read_token('+')
                self.Proc_At()
                # print('A ->A’+’ At')
                self.build_tree('+', 2)
            elif self.curr_token.value == '-':
                self.read_token('-')
                self.Proc_At()
                # print('A ->A’-’ At')
                self.build_tree('-', 2)
        return

    def Proc_At(self):

        self.Proc_Af()
        # print('At -> Af')

        while self.curr_token.value == '*' or self.curr_token.value == '/':
            if self.curr_token.value == '*':
                self.read_token('*')
                self.Proc_Af()
                # print('At -> At ’*’ Af')
                self.build_tree('*', 2)
            elif self.curr_token.value == '/':
                self.read_token('/')
                self.Proc_Af()
                # print('At -> At ’/’ Af')
                self.build_tree('/', 2)
        return

    def Proc_Af(self):

        self.Proc_Ap()

        if self.curr_token.value == '**':
            self.read_token('**')
            self.Proc_Af()
            # print('Af -> Ap ’**’ Af')
            self.build_tree('**', 2)
            return
        # print('Af -> Ap')
        return

    # Checked & Fixed
    def Proc_Ap(self):

        self.Proc_R()
        # print('Ap -> R')

        while self.curr_token.value == '@':
            self.read_token('@')
            self.read_token_by_type('<IDENTIFIER>')
            self.Proc_R()
            # print('Ap -> Ap ’@’ ’<IDENTIFIER>’ R')
            self.build_tree('@', 3)  # Checked & Fixed
        return

    # Checked and Fixed
    def Proc_R(self):

        self.Proc_Rn()
        # print('R -> Rn')

        while (self.curr_token.type in ["<IDENTIFIER>", "<INTEGER>", "<STRING>"] or
               self.curr_token.value in ['true', 'false', 'nil', '(', 'dummy']):
            self.Proc_Rn()
            # print('R ->R Rn')
            self.build_tree('gamma', 2)
        return

    # Checked & Fixed
    def Proc_Rn(self):

        if self.curr_token.type in ["<IDENTIFIER>", "<INTEGER>", "<STRING>"]:

            match self.curr_token.type:
                case "<IDENTIFIER>":
                    self.read_token_by_type("<IDENTIFIER>")
                    # print('Rn -> ’<IDENTIFIER>’')
                case "<INTEGER>":
                    self.read_token_by_type("<INTEGER>")
                    # print('Rn -> ’<INTEGER>’')
                case "<STRING>":
                    self.read_token_by_type("<STRING>")
                    # print('Rn -> ’<STRING>’')

        elif self.curr_token.value in ['true', 'false', 'nil', '(', 'dummy']:

            match self.curr_token.value:
                case 'true':
                    self.read_token('true')
                    # print('Rn -> ’true’')
                    self.build_tree('true', 0)
                case 'false':
                    self.read_token('false')
                    # print('Rn -> ’false’')
                    self.build_tree('false', 0)
                case 'nil':
                    self.read_token('nil')
                    # print('Rn -> ’nil’')
                    self.build_tree('nil', 0)
                case 'dummy':
                    self.read_token('dummy')
                    # print('Rn -> ’dummy’')
                    self.build_tree('dummy', 0)
                case '(':
                    self.read_token('(')
                    self.Proc_E()
                    self.read_token(')')
                    # print('Rn -> ’( E )’')
        return

    def Proc_D(self):

        self.Proc_Da()

        if self.curr_token.value == 'within':
            self.read_token('within')
            self.Proc_D()
            # print('D -> Da ’within’ D')
            self.build_tree('within', 2)
            return
        # print('D -> Da')
        return

    def Proc_Da(self):

        self.Proc_Dr()

        if self.curr_token.value == 'and':
            self.read_token('and')
            self.Proc_Dr()
            n = 1
            while self.curr_token == 'and':
                self.read_token('and')
                self.Proc_Dr()
                n += 1
            # print('Da -> Dr ( ’and’ Dr )+')
            self.build_tree('and', n + 1)
        # print('Da -> Dr')
        return

    def Proc_Dr(self):
        if self.curr_token.value == 'rec':

            self.read_token('rec')
            self.Proc_Db()
            # print('Dr -> ’rec’ Db')
            self.build_tree('rec', 1)
        else:
            self.Proc_Db()
            # print('Dr -> Db')
        return

    # Checked & Fixed
    def Proc_Db(self):

        if self.curr_token.value == '(':
            self.read_token('(')
            self.Proc_D()
            self.read_token(')')
            # print('Db -> ’(’ D ’)’ ')
        elif self.curr_token.type == '<IDENTIFIER>':
            '''
            We happened to check two consecutive tokens as 
                Db -> Vl ’=’ E => ’=’
                   -> ’<IDENTIFIER>’ Vb+ ’=’ E
                both have the same first set <IDENTIFIER>
            '''
            # up-coming token is looked ahead to resolve the issued mentioned above.
            look_ahead_token = self.tokens[self.curr_idx + 1]

            if look_ahead_token.type == '<IDENTIFIER>' or look_ahead_token.value == '(':
                # 'Db -> ’<IDENTIFIER>’ Vb+ ’=’ E' is chosen
                self.read_token_by_type('<IDENTIFIER>')

                if self.curr_token.value == '(' or self.curr_token.type == '<IDENTIFIER>':
                    self.Proc_Vb()
                    n = 1

                    while self.curr_token.value == '(' or self.curr_token.type == '<IDENTIFIER>':
                        self.Proc_Vb()
                        n += 1

                    self.read_token('=')

                    self.Proc_E()
                    # print('Db -> ’<IDENTIFIER>’ Vb+ ’=’ E')
                    self.build_tree('function_form', n + 2)  # Checked & Fixed
            else:
                self.Proc_Vl()
                self.read_token('=')
                self.Proc_E()

                # print('Db -> Vl ’=’ E')
                self.build_tree('=', 2)
        return

    def Proc_Vb(self):

        if self.curr_token.value == '(':
            self.read_token('(')
            if self.curr_token.value == ')':
                self.read_token(')')
                # print('Vb -> ’(’ ’)’')
                self.build_tree('()', 0)
            else:
                self.Proc_Vl()
                self.read_token(')')
                # print('Vb -> ’(’ Vl ’)’')
        else:
            self.read_token_by_type('<IDENTIFIER>')
            # print('Vb -> ’<IDENTIFIER>’')
        return

    def Proc_Vl(self):

        self.read_token_by_type('<IDENTIFIER>')

        n = 0
        while self.curr_token.value == ',':
            self.read_token(',')
            self.read_token_by_type('<IDENTIFIER>')
            n += 1

        if n > 0:
            # print('Vl -> ’<IDENTIFIER>’ list ’,’')
            self.build_tree(',', n + 1)
        return

    
    """
    -------------Functions needed for the process of parsing and building the AST----------------
    """

    def parse_file(self, in_file):
        """
        This function first extracts the tokens,  parses by invoking respective functions.
       
        """
        self.token_extraction(in_file)
        self.Proc_E()
        self.build_AST(self.stack[0])
        return

    def build_AST(self, node, level=0):
        """
        This function prints the built AST tree.
    
        """
        # level is for indicating the tree levels of each node
        self.output_AST += '.' * level + node.value + "\n"
        if len(node.children) == 0:
            return

        # when building AST children of each node is reversed.
        # So we make them reveresed again to get the correct version
        node.children.reverse()

        level += 1

        for child in node.children:
            self.build_AST(child, level)

# For debugging

# tokenizer= Tokenizer()
# tokens = tokenizer.tokenize('input.txt')

# for token in tokens:
#    print(f"Token type :  {token.type:<15} Value : {token.value}")



# parser = RPALParser()
# parser.parse_file('input.txt')
# print(parser.output_AST)

