class TreeNode:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def find_child(self, name):
        for child in self.children:
            if child.name == name:
                return child
        return None

    def print_tree(self, indent=0):
        print(' ' * indent + self.name)
        for child in self.children:
            child.print_tree(indent + 2)

def build_tree(directories):
    root = TreeNode('root')
    for path in directories:
        parts = path.split('/')  # Игнорируем корневой элемент
        current_node = root
        for part in parts:
            child = current_node.find_child(part)
            if not child:
                child = TreeNode(part)
                current_node.add_child(child)
            current_node = child
    return root

def print_directories(node, indent=-2):
    if node !=root_node:
        print(' ' * indent + node.name)
    for child in sorted(node.children, key=lambda x: x.name):
        print_directories(child, indent + 2)

# Считываем количество директорий
n = int(input())

# Считываем директории
directories = [input() for _ in range(n)]

# Создаем дерево из списка директорий
root_node = build_tree(directories)

# Выводим директории с учетом вложенности
print_directories(root_node,)

