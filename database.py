class AVLNode:
    def __init__(self, student_id, name, age, grade):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.grade = grade
        self.height = 1  # Height of this node
        self.left = None  # Left child
        self.right = None  # Right child


class AVLTree:
    def __init__(self):
        self.root = None

    # Utility function to get the height of a node
    def get_height(self, node):
        return node.height if node else 0

    # Utility function to calculate balance factor
    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    # Right rotation
    def rotate_right(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    # Left rotation
    def rotate_left(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    # Insert a new record into the AVL tree
    def insert(self, node, student_id, name, age, grade):
        if not node:
            return AVLNode(student_id, name, age, grade)

        # Perform standard BST insertion
        if student_id < node.student_id:
            node.left = self.insert(node.left, student_id, name, age, grade)
        elif student_id > node.student_id:
            node.right = self.insert(node.right, student_id, name, age, grade)
        else:
            return node  # Duplicates are not allowed

        # Update height of the current node
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        # Check balance and perform rotations if needed
        balance = self.get_balance(node)

        # Left Left Case
        if balance > 1 and student_id < node.left.student_id:
            return self.rotate_right(node)

        # Right Right Case
        if balance < -1 and student_id > node.right.student_id:
            return self.rotate_left(node)

        # Left Right Case
        if balance > 1 and student_id > node.left.student_id:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        # Right Left Case
        if balance < -1 and student_id < node.right.student_id:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    # Delete a record from the AVL tree
    def delete(self, node, student_id):
        if not node:
            return node

        # Perform standard BST deletion
        if student_id < node.student_id:
            node.left = self.delete(node.left, student_id)
        elif student_id > node.student_id:
            node.right = self.delete(node.right, student_id)
        else:
            # Node with one or no child
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            # Node with two children: Get the inorder successor
            temp = self.get_min_value_node(node.right)
            node.student_id = temp.student_id
            node.name = temp.name
            node.age = temp.age
            node.grade = temp.grade
            node.right = self.delete(node.right, temp.student_id)

        # Update height and check balance
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)

        # Balance the tree
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.rotate_right(node)

        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.rotate_left(node)

        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    # Utility to find the node with the smallest key
    def get_min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    # Search for a student record by ID
    def search(self, node, student_id):
        if not node or node.student_id == student_id:
            return node

        if student_id < node.student_id:
            return self.search(node.left, student_id)
        return self.search(node.right, student_id)

    # In-order traversal (sorted order)
    def in_order(self, node):
        if node:
            self.in_order(node.left)
            print(f"ID: {node.student_id}, Name: {node.name}, Age: {node.age}, Grade: {node.grade}")
            self.in_order(node.right)


# Example Usage
if __name__ == "__main__":
    tree = AVLTree()

    # Insert records
    tree.root = tree.insert(tree.root, 101, "Alice", 20, "A")
    tree.root = tree.insert(tree.root, 102, "Bob", 22, "B")
    tree.root = tree.insert(tree.root, 103, "Charlie", 21, "A-")

    # Display all records
    print("In-order traversal:")
    tree.in_order(tree.root)

    # Search for a record
    print("\nSearching for ID 102:")
    result = tree.search(tree.root, 102)
    if result:
        print(f"Found: {result.student_id}, {result.name}, {result.age}, {result.grade}")
    else:
        print("Record not found.")

    # Delete a record
    print("\nDeleting ID 102...")
    tree.root = tree.delete(tree.root, 102)

    # Display all records after deletion
    print("\nIn-order traversal after deletion:")
    tree.in_order(tree.root)
