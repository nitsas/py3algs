"""
A simple binary search tree implementation.

Operations:
- __len__
- __contains__
- root
- insert
- find

Author:
  Chris Nitsas
  (nitsas)
  (nitsas.chris)

Language:
  Python 3(.4)

Date:
  May, 2016
"""


__all__ = ['BinarySearchTree', 'BinarySearchTreeUsingNodes', 'Node']


class Node:
    """
    A node in the binary tree (implementation using nodes).
    
    A node has a `value` and points to `left` and `right` child nodes.
    """
    
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value


class BinarySearchTreeUsingNodes:
    """
    A simple binary tree implemented using a Node class.
    
    There is the root node, and each node points to a left and right child
    node or None when some child does not exist. So, a node is a leaf when
    both the left and the right child is None.
    """
    
    def __init__(self):
        self._root = None
        self._len = 0
    
    def __len__(self):
        return self._len
    
    def __contains__(self, value):
        return bool(self.find(value))
    
    def root(self):
        return self._root
    
    def insert(self, value):
        """
        Insert the given value in the tree.
        
        Iterative implementation to avoid hitting the maximum recursion depth.
        """
        
        if self._root is None:
            self._root = Node(value)
        else:
            parent = None
            node = self._root
            while node is not None:
                if value <= node.value:
                    parent, node = node, node.left
                else:
                    parent, node = node, node.right
            if value <= parent.value:
                parent.left = Node(value)
            else:
                parent.right = Node(value)
        self._len += 1
    
    def find(self, value):
        """
        Find a node with the given value (the shallowest one), if one exists.
        
        Iterative implementation to avoid hitting the maximum recursion depth.
        """
        
        node = self._root
        while node is not None:
            if value == node.value:
                return node
            elif value < node.value:
                node = node.left
            else:
                node = node.right
        return None


BinarySearchTree = BinarySearchTreeUsingNodes


# NOTE: I should also try to implement one using a list, for better locality
#   of reference.
