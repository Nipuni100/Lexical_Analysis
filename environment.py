class Environment:
    def __init__(self, name):
        self.name = name
        self.binding = dict()
        self.parent = None
        self.children = []

    def add_child(self, env):
        """
        This function is for adding child environment to the current environment
        :param env:
        :return:
        """
        self.children.append(env)
        env.parent = self

    def lookup(self, var):
        """
        This function for look up a value in the current and parent environment
        :param var:
        :return:
        """
        try:
            return self.binding[var]
        except KeyError:
            if self.parent is None:
                exit(f'{var} is not defined.')

            return self.parent.lookup(var)

    def add_binding(self, var, value):
        """
        This function is for adding binding into the environment
        :param var:
        :param value:
        :return:
        """
        self.binding[var] = value


# for debugging

# e1 = Environment(1)
# e1.add_binding("a", 5)
# e1.add_binding("b", 7)

# e2 = Environment(2)
# e2.add_binding("c", 4)

# e3 = Environment(3)

# e1.add_child(e2)
# e2.add_child(e3)

# print(e3.lookup("d"))

# print(e3.lookup('a'))