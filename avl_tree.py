import matplotlib.pyplot as plt
import networkx as nx


class AVLNode:
    def __init__(self, key):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None

    def __str__(self, level=0, prefix="Root: "):
        ret = "\t" * level + prefix + str(self.key) + "\n"
        if self.left:
            ret += self.left.__str__(level + 1, "L--- ")
        if self.right:
            ret += self.right.__str__(level + 1, "R--- ")
        return ret


class AVLTree:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def left_rotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def right_rotate(self, y):
        x = y.left
        T3 = x.right

        x.right = y
        y.left = T3

        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))

        return x

    def min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def max_value(self):
        return self._max_value(self.root)

    def _max_value(self, root):
        current = root
        while current.right:
            current = current.right
        return current.key

    def min_value(self):
        return self._min_value(self.root)

    def _min_value(self, root):
        current = root
        while current.left:
            current = current.left
        return current.key

    def sum(self):
        return self._sum(self.root)

    def _sum(self, root):
        if not root:
            return 0
        return root.key + self._sum(root.left) + self._sum(root.right)

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, root, key):
        if not root:
            return AVLNode(key)

        if key < root.key:
            root.left = self._insert(root.left, key)
        elif key > root.key:
            root.right = self._insert(root.right, key)
        else:
            return root

        root.height = 1 + max(self.get_height(root.left),
                              self.get_height(root.right))

        balance = self.get_balance(root)

        if balance > 1:
            if key < root.left.key:
                return self.right_rotate(root)
            else:
                root.left = self.left_rotate(root.left)
                return self.right_rotate(root)

        if balance < -1:
            if key > root.right.key:
                return self.left_rotate(root)
            else:
                root.right = self.right_rotate(root.right)
                return self.left_rotate(root)

        return root

    def delete_node(self, key):
        self.root = self._delete_node(self.root, key)

    def _delete_node(self, root, key):
        if not root:
            return root

        if key < root.key:
            root.left = self._delete_node(root.left, key)
        elif key > root.key:
            root.right = self._delete_node(root.right, key)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp

            temp = self.min_value_node(root.right)
            root.key = temp.key
            root.right = self._delete_node(root.right, temp.key)

        if root is None:
            return root

        root.height = 1 + max(self.get_height(root.left),
                              self.get_height(root.right))

        balance = self.get_balance(root)

        if balance > 1:
            if self.get_balance(root.left) >= 0:
                return self.right_rotate(root)
            else:
                root.left = self.left_rotate(root.left)
                return self.right_rotate(root)

        if balance < -1:
            if self.get_balance(root.right) <= 0:
                return self.left_rotate(root)
            else:
                root.right = self.right_rotate(root.right)
                return self.left_rotate(root)

        return root

    def plot_tree(self):
        if not self.root:
            print("Empty tree")
            return
        G = nx.DiGraph()
        G.add_node(self.root.key)
        pos = self._compute_position(G, self.root)
        nx.draw(G, pos=pos, with_labels=True, arrows=True, node_size=700,
                node_color="lightblue", font_size=8, font_color="black")
        plt.show()

    def _compute_position(self, G, node, pos=None, layer=1, layer_height=2, layer_offset=0.5):
        if pos is None:
            pos = {node.key: (0, 0)}

        if node.left:
            pos[node.left.key] = (
                pos[node.key][0] - layer_height / (2 ** layer), pos[node.key][1] - layer_offset)
            G.add_edge(node.key, node.left.key)
            self._compute_position(
                G, node.left, pos, layer + 1, layer_height, layer_offset)

        if node.right:
            pos[node.right.key] = (
                pos[node.key][0] + layer_height / (2 ** layer), pos[node.key][1] - layer_offset)
            G.add_edge(node.key, node.right.key)
            self._compute_position(
                G, node.right, pos, layer + 1, layer_height, layer_offset)

        return pos

    def __str__(self):
        return str(self.root)


if __name__ == "__main__":
    avl_tree = AVLTree()

    # Insert
    keys = [10, 20, 30, 25, 28, 27, -1]
    for key in keys:
        avl_tree.insert(key)
        print("Inserted:", key)
        print(f"AVL-Tree:\n{avl_tree}")
        print("Max value:", avl_tree.max_value())
        print("Min value:", avl_tree.min_value())
        print("Sum:", avl_tree.sum())
        print("-------------------")
        avl_tree.plot_tree()

    # Delete
    keys_to_delete = [10, 27]
    for key in keys_to_delete:
        avl_tree.delete_node(key)
        print("Deleted:", key)
        print(f"AVL-Tree:\n{avl_tree}")
        print("Max value:", avl_tree.max_value())
        print("Min value:", avl_tree.min_value())
        print("Sum:", avl_tree.sum())
        print("-------------------")
        avl_tree.plot_tree()
