#!/usr/bin/env python
# coding: utf-8

# In[1]:


from scanner import scanner
input="let Sum(A) = Psum (A,Order A ) where rec Psum (T,N) = N eq 0 -> 0 | Psum(T,N-1)+T N in Print ( Sum (1,2,3,4,5) )"

tokens = scanner(input)


# In[2]:


class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

def token_objects(tokens):
    token_objects_list = []
    for token in tokens:
        token_objects_list.append(Token(token[0], token[1]))
    return token_objects_list

token_objects_list = token_objects(tokens)

for obj in token_objects_list:
    print("The token type: '            ", obj.token_type, "      '  Value: ", obj.value)


# Read

# In[3]:


current_index = 0

def Read(token_type,token_value):
    global current_index
    print(token_type)
    print(token_value)
    print(current_index)
    print(token_objects_list.pop(current_index).value)
    
    if current_index < len(token_objects_list) and token_objects_list[current_index].token_type== token_type and token_objects_list[current_index].value== token_value:
        current_token = token_objects_list.pop(current_index)
        print(current_token)
        
        if current_index < len(token_objects_list):
            current_token = token_objects_list[current_index]
            print(current_token)
        else:
            current_token = None
#     else:
#         raise Exception(f"Expected token '{token_value}', but got '{current_token.token_type}' instead")
    current_index += 1


# In[4]:


Read('IDENTIFIER','let')


# current node

# In[5]:


# def next_token():    


# In[6]:


def current_token():
    if not tokens:
        return None
    global current_token
    if current_token:
        return current_token.token_type
    else:
        current_token = token_objects_list[0]
        return current_token.token_type


# Build tree

# In[7]:


class TreeNode:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, node):
        self.children.insert(0,node)

    def __str__(self):
        result = f"Node: {self.name}\n"
        for child in self.children:
            result += str(child)
        return result


# In[8]:


def Build_tree(node_name, number_of_nodes_to_remove):
    if number_of_nodes_to_remove <= 0:
        raise Exception("Invalid number of nodes to remove")
    if number_of_nodes_to_remove > len(tokens):
        raise Exception("Not enough tokens to remove")
               
    new_node = TreeNode(node_name)
    for i in range(0, number_of_nodes_to_remove):
        new_node.add_child(tokens.pop(0))


# In[9]:


my_node1=TreeNode('Nipuni')
child1 = TreeNode("A")
child2 = TreeNode("B")
my_node1.add_child(child1)
my_node1.add_child(child2)

# my_node2=TreeNode('Lahiru')
child_1 = TreeNode("C")
child_2 = TreeNode("D")
child1.add_child(child_1)
child2.add_child(child_2)


# my_node3=TreeNode('Nipz')
by1 = TreeNode("E")
by2 = TreeNode("F")
child_1.add_child(by1)
child_2.add_child(by2)


# Print Tree

# In[10]:



def pre_order_traversal(node,indent=''):
    """
    Performs a pre-order traversal of the tree rooted at the given node,
    printing the name of each node.
    """
    # Visit the current node
    print(indent+node.name)
    indent+= '.'
    # Traverse the children
    for child in node.children:        
        pre_order_traversal(child,indent)

# pre_order_traversal(my_node1)


# In[11]:


# Example 2
root = TreeNode('<function_form>')
child1 = TreeNode('<ID:Sum>')
child2 = TreeNode('<ID:A>' )
grandchild1 = TreeNode('<where>')
grandchild2 = TreeNode('<ID:gamma>' )
grandchild3 = TreeNode('<ID:Psum>')
grandchild4 = TreeNode('<ID:tau>')
grandchild5 = TreeNode('<ID:A>')
grandchild6 = TreeNode('<ID:gamma>')
grandchild7 = TreeNode('<ID:Order>')
grandchild8 = TreeNode('<ID:A>')

root.children.extend([child1, child2])
child1.children.append(grandchild1)
grandchild1.children.extend([grandchild2, grandchild6])
grandchild2.children.append(grandchild3)
grandchild3.children.append(grandchild5)
grandchild6.children.append(grandchild7)
grandchild6.children.append(grandchild8)

# print(root)


# In[12]:


pre_order_traversal(root)


# # Expressions

# In[13]:


def Proc_Rn():
    if token_objects_list[0].token_type=='<IDENTIFIER>':
        Read('<IDENTIFIER>', "any")         
    elif token_objects_list[0].token_type=='<STRING>':
        Read('<STRING>', "any")
    elif token_objects_list[0].token_type=='<INTEGER>':
        Read('<INTEGER>' , "any")
    elif token_objects_list[0].value=='true':
        Read('<IDENTIFIER>', 'true')
        Build_tree('true',1)
    elif token_objects_list[0].value=='false':
        Read('<IDENTIFIER>','false')
        Build_tree('false',1)
    elif token_objects_list[0].value=='nil':
        Read('<IDENTIFIER>','nil')
        Build_tree('nil',1)
    elif token_objects_list[0].value=='(':
        Read('<PUNCTUATION>','(')
        Proc_E()
        Read('<PUNCTUATION>',')')
    else:
        Read('<IDENTIFIER>',"dummy")
        Build_tree('dummy',1)


# In[14]:


Proc_Rn()


# In[15]:


def Proc_E():
    if token_objects_list[0].value=='let':
        Read('<IDENTIFIER>','let')
        Proc_D()
        Read('<IDENTIFIER>','in')
        Proc_E()
        Build_tree('let',2)
    elif token_objects_list[0].value=='fn':
        Read('<IDENTIFIER>','fn')
        n=1
        Proc_Vb()
        while token_objects_list[0].value=='fn':
            Proc_Vb()
            n+=1
        Read('<OPERATOR>','.')
        Proc_E()
        Build_tree('lamdha',n+1)
    else:
        Proc_Ew()
        Read('<PUNCTUATION>',';')      


# In[16]:


def Proc_Ew():
    Proc_T()
    if token_objects_list[0].value=='where':
        Read('<IDENTIFIER>','where')
        Proc_Dr()
        Build_tree('where',2)


# # Tuple Expressions

# In[17]:


def Proc_T():
    Proc_Ta()
    n=1
    if token_objects_list[0].value==',':
        while token_objects_list[0].value==',':
            Read('<PUNCTUATION>',',')
            Proc_Ta()
            n+=1
        Build_tree('tau',n+1)


# In[18]:


def Proc_Ta():
    Proc_Tc()
    while token_objects_list[0].value=='aug':
        Read('<PUNCTUATION>','aug')
        Proc_Tc()
        Build_tree('aug',2)
        
def Proc_Tc():
    Proc_B()
    if token_objects_list[0].value=='->':
        Read('<OPERATOR>','->')
        Proc_Tc()
        Read('<OPERATOR>','|')
        Proc_Tc()   


# # Boolean Expressions

# In[19]:


def Proc_B():
    Proc_Bt()
    while token_objects_list[0].value=='or':
        Read('<IDENTIFIER>','or')
        Proc_Bt()
        Build_tree('or',2)


# In[20]:


def Proc_Bt():
    Proc_Bs()
    while token_objects_list[0].value=='&':
        Read('<OPERATOR>','&')
        Proc_Bs()
        Build_tree('&',2)


# In[21]:


def Proc_Bs():
    if token_objects_list[0].value=='not':
        Proc_Bp()
        Build_tree('not',1)
    else:
        Proc_Bp()   


# In[22]:


def Proc_Bp():
    Proc_A()
    if token_objects_list[0].value=='eq':
        Read('<IDENTIFIER>','eq')
        Proc_A()
        Build_tree('eq',2)
    elif token_objects_list[0].value=='ne':
        Read('<IDENTIFIER>','ne')
        Proc_A()
        Build_tree('ne',2)
    elif token_objects_list[0].value=='gr' or '>':
        if token_objects_list[0].value=='gr':
            Read('<IDENTIFIER>','gr')
            Proc_A()
        else:
            Read('<OPERATOR>','>')
            Proc_A()
        Build_tree('gr',2)
    elif token_objects_list[0].value=='ge' or '>=':
        if token_objects_list[0].value=='ge':
            Read('<IDENTIFIER>','ge')
            Proc_A()
        else:
            Read('<OPERATOR>','>=')
            Proc_A()
        Build_tree('ge',2)  
    elif token_objects_list[0].value=='ls' or '<':
        if token_objects_list[0].value=='ls':
            Read('<IDENTIFIER>','ls')
            Proc_A()
        else:
            Read('<OPERATOR>','<')
            Proc_A()
        Build_tree('ls',2)
    elif token_objects_list[0].value=='le' or '<=':
        if token_objects_list[0].value=='le':
            Read('<IDENTIFIER>','le')
            Proc_A()
        else:
            Read('<OPERATOR>','<=')
            Proc_A()
        Build_tree('le',2)


# # Arithmetic Expressions

# In[23]:


def Proc_A():
    if token_objects_list[0].value=='+':
            Read('<OPERATOR>','+')
            Proc_At()
    elif token_objects_list[0].value=='-':
            Read('<OPERATOR>','-')
            Proc_At()
            Build_tree('neg',1)
    else:
        Proc_A()
        if token_objects_list[0].value=='+':
            Proc_At()
            Build_tree('+',2)
        else:
            Proc_At()
            Build_tree('-',2)


# In[24]:


def Proc_At():
       Proc_Af()
       n=1
       while token_objects_list[0].value=='*':
           Read('<OPERATOR>','*')
           Proc_Af()
           n+=1
           Build_tree('*',n)
       m=1
       while token_objects_list[0].value=='/':
           Read('<OPERATOR>','/')
           Proc_Af()
           m+=1
           Build_tree('/',m)


# In[25]:


def Proc_Af():
       Proc_Ap()
       n=1
       while token_objects_list[0].value=='**':
           Read('<OPERATOR>','**')
           Proc_Ap()
           n+=1
           Build_tree('**',n)            


# In[26]:


(/, This, is, needs, a, clarification)
def Proc_Ap():
    Proc_R()
    n=1
    while current_token()=='@':
        Read('@')
        Read('IDENTIFIER')
        Build_tree('<IDENTIFIER>',0)
        Proc_R()
        n+=1
        Build_tree('@',n)


# # Rators and Rands

# In[27]:


def Proc_Ap():
       Proc_R()
       n=1
       while token_objects_list[0].value=='@':
           Read('<IDENTIFIER>','@')
           Read('<IDENTIFIER>')
           Build_tree('<IDENTIFIER>',0)
           Proc_R()
           n+=1
           Build_tree('@',n)   


# # Definitions
# 

# In[28]:


def Proc_D():
    Proc_Da()
    if token_objects_list[0].value=='within':
        Read('<IDENTIFIER>','within')
        Proc_D()
        Build_tree('within',2)
        
def Proc_T():
    Proc_Dr()
    n=1
    if token_objects_list[0].value=='and':
        while token_objects_list[0].value=='and':
            Read('<IDENTIFIER>','and')
            Proc_Dr()
            n+=1
        Build_tree('and',n+1)

def Proc_Dr():
    if token_objects_list[0].value=='rec':
        Proc_Db()
        Build_tree('rec',1)
    else:
        Proc_Db()
    


# In[29]:


def Proc_Db():
    if token_objects_list[0].value=='(':
        Read('<PUNCTUATION>','(')
        Proc_D()
        Read('<PUNCTUATION>',')')
    elif token_objects_list[0].value=='<IDENTIFIER>':
        Read('<IDENTIFIER>')
        Build_tree('<IDENTIFIER>',0)
        n=1
        Proc_Vb()
        while token_objects_list[0].value=='<IDENTIFIER>':
            Proc_Vb()
            n+=1
        Read('<OPERATOR>','=')
        Proc_E()
        Build_tree('fcn_form',n+1)
    else:
        Proc_Vl()
        Read('<OPERATOR>','=')
        Proc_E()        


# In[30]:


def Proc_Vb():
    if token_objects_list[0].value=='<IDENTIFIER>':
        Read('<IDENTIFIER>')
        Build_tree('<IDENTIFIER>',0)
    else:
#     elif token_objects_list[0].value=='(':
        Read('<PUNCTUATION>','(')
        if token_objects_list[0].value==')':
            Read('<PUNCTUATION>',')')
            Build_tree('()',1)
        else:
            Proc_Vl()
            Read(')')

def Proc_Vl():
    n=1
    Read('<IDENTIFIER>', "any")
    while token_objects_list[0].value==',':
            Read('<PUNCTUATION>',',')
            Read('<IDENTIFIER>', "any")
            n+=1
    if (n>1) :
        Build_tree(',',1)
    

main function
# In[31]:


def main():
    # Initialize the list of token objects
    token_objects_list = token_objects(tokens)
    # Initialize the current index
    current_index = 0

    # Call Proc_E()
    Proc_E()

    # Print the remaining tokens
    print("Remaining tokens:")
    for token in token_objects_list:
        print(token.token_type)

    # Print the AST
    print("\nAST:")
    print(ast_root)

if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




