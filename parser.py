class Tree:
    def __init__(self, tag, parent=None):
        self.tag = tag
        self.parent = parent
        self.child = None
        self.next = None

    def add_a_child(self, tag):
        if self.child:
            this = self.child
            while this.next:
                this = this.next
            this.next = Tree(tag, self)
        else:
            self.child = Tree(tag, self)

    def __str__(self, lvl=1):
        graph = '\033[34m' + '|  ' * (lvl - 1) + '|--\033[0m' + str(self.tag) + '\n'
        if self.child:
            graph += self.child.__str__(lvl + 1)
        if self.next:
            graph += self.next.__str__(lvl)
        return graph


def error(a):
    print('Sequence error', a.coords)
    exit(0)


def scroll_tree(tree):
    while tree.parent and not tree.next:
        tree = tree.parent
    return tree.next or tree


def parse(S, T, b, u):
    stack = ['$', S]
    a = next(u)
    tree = Tree(S)
    while len(stack) > 1:
        X = stack.pop()
        if X in T:
            if X == a.domain:
                a = next(u)
                tree = scroll_tree(tree)
            else:
                error(a)
        else:
            Y = b(X, a.domain)
            if Y:
                if Y != 'err':
                    queue = Y.split(' ')
                    for i in range(0, len(queue)):
                        tree.add_a_child(queue[i])
                        stack.append(queue[len(queue) - i - 1])
                    tree = tree.child
                else:
                    error(a)
            else:
                tree = scroll_tree(tree)
    return tree
