from parser import RPALParser
from Standardizer import Standardizer
from cse_machine import CSE_machine
import sys

# reading inputs from command line
arguments = sys.argv

# instantiating parser, standardizer and CSE machine
parser = RPALParser()
standardizer = Standardizer()
cse = CSE_machine()


if len(arguments) <= 3:
    if len(arguments) == 2:

        print("Starting the CSE Machine...\n")
        # assigning the name for input file
        input_file = arguments[1]

        print("Output of the above program is: ")
        parser.parse_file(input_file)
        standardizer.standardize(parser.stack)
        cse.execute(standardizer.std_tree[0])
        # print(cse.control_structure)  # for debugging

    elif len(arguments) == 3:

        print("Starting the CSE Machine...\n")
        # assigning the name for input file
        input_file = arguments[2]

        if arguments[1] == '-ast':

            print("The corresponding AST: \n")
            parser.parse_file(input_file)
            print(parser.output_AST)

        elif arguments[1] == "-st":

            print("The corresponding ST: \n")
            parser.parse_file(input_file)
            standardizer.standardize(parser.stack)
            print(standardizer.output_ST)
        else:
            print('Invalid Command: try <file_name> [<-ast>/<-st>] <RPAL source file>')
#     else:
#         print('Invalid Command: try <file_name> [<-ast>/<-st>] <RPAL source file>')
# # else:
#     print('Invalid Command: try <file_name> [<-ast>/<-st>] <RPAL source file>')