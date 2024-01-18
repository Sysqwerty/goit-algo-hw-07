import matplotlib.pyplot as plt
import networkx as nx


class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

    def __str__(self, level=0, prefix="Root: "):
        ret = "\t" * level + prefix + str(self.val) + "\n"
        if self.left:
            ret += self.left.__str__(level + 1, "L--- ")
        if self.right:
            ret += self.right.__str__(level + 1, "R--- ")
        return ret


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, root, key):
        if root is None:
            return Node(key)
        else:
            if key < root.val:
                root.left = self._insert(root.left, key)
            else:
                root.right = self._insert(root.right, key)
        return root

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, root, key):
        if root is None or root.val == key:
            return root
        if key < root.val:
            return self._search(root.left, key)
        return self._search(root.right, key)

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
        return current.val

    def min_value(self):
        return self._min_value(self.root)

    def _min_value(self, root):
        current = root
        while current.left:
            current = current.left
        return current.val

    def sum(self):
        return self._sum(self.root)

    def _sum(self, root):
        if not root:
            return 0
        return root.val + self._sum(root.left) + self._sum(root.right)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, root, key):
        if not root:
            return root

        if key < root.val:
            root.left = self._delete(root.left, key)
        elif key > root.val:
            root.right = self._delete(root.right, key)
        else:
            if not root.left:
                temp = root.right
                root = None
                return temp
            elif not root.right:
                temp = root.left
                root = None
                return temp
            root.val = self.min_value_node(root.right).val
            root.right = self._delete(root.right, root.val)
        return root

    def plot_tree(self):
        if not self.root:
            print("Empty tree")
            return
        G = nx.DiGraph()
        G.add_node(self.root.val)
        pos = self._compute_position(G, self.root)
        nx.draw(G, pos=pos, with_labels=True, arrows=True, node_size=700,
                node_color="lightblue", font_size=8, font_color="black")
        plt.show()

    def _compute_position(self, G, node, pos=None, layer=1, layer_height=2, layer_offset=0.5):
        if pos is None:
            pos = {node.val: (0, 0)}

        if node.left:
            pos[node.left.val] = (
                pos[node.val][0] - layer_height / (2 ** layer), pos[node.val][1] - layer_offset)
            G.add_edge(node.val, node.left.val)
            self._compute_position(
                G, node.left, pos, layer + 1, layer_height, layer_offset)

        if node.right:
            pos[node.right.val] = (
                pos[node.val][0] + layer_height / (2 ** layer), pos[node.val][1] - layer_offset)
            G.add_edge(node.val, node.right.val)
            self._compute_position(
                G, node.right, pos, layer + 1, layer_height, layer_offset)

        return pos

    def __str__(self):
        return str(self.root)


if __name__ == "__main__":
    bst = BinarySearchTree()

    # Insert
    keys = [5, 3, 2, 4, 7, 6, 8]
    for key in keys:
        bst.insert(key)
        print("Inserted:", key)
        print(f"Binary Search Tree:\n{bst}")
        print("Max value:", bst.max_value())
        print("Min value:", bst.min_value())
        print("Sum:", bst.sum())
        print("-------------------")
        bst.plot_tree()

    # Delete
    keys_to_delete = [7, 5]
    for key in keys_to_delete:
        bst.delete(key)
        print("Deleted:", key)
        print(f"Binary Search Tree:\n{bst}")
        print("Max value:", bst.max_value())
        print("Min value:", bst.min_value())
        print("Sum:", bst.sum())
        print("-------------------")
        bst.plot_tree()
