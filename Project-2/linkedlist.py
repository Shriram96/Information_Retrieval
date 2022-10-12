'''
@author: Sougata Saha
Institute: University at Buffalo
'''

import math


class Node:

    def __init__(self, value=None, tf=None, tfidf=None, next=None, next_skip=None):
        """ Class to define the structure of each node in a linked list (postings list).
            Value: document id, Next: Pointer to the next node
            Add more parameters if needed.
            Hint: You may want to define skip pointers & appropriate score calculation here"""
        self.value = value
        self.next = next
        self.tf = tf
        self.tfidf = tfidf
        self.next_skip = next_skip


class LinkedList:
    """ Class to define a linked list (postings list). Each element in the linked list is of the type 'Node'
        Each term in the inverted index has an associated linked list object.
        Feel free to add additional functions to this class."""
    def __init__(self):
        self.start_node = None
        self.end_node = None
        self.length, self.n_skips, self.idf = 0, 0, 0.0
        self.skip_length = None

    def traverse_list(self):
        traversal = []
        if self.start_node is not None:
            """ Write logic to traverse the linked list.
                To be implemented."""
            node = self.start_node
            while node is not None:
                traversal.append(node.value)
                node = node.next
        return traversal

    def traverse_skips(self):
        traversal = []
        if self.start_node is not None and self.length > 2:
            """ Write logic to traverse the linked list using skip pointers.
                To be implemented."""
            node = self.start_node
            while node is not None:
                traversal.append(node.value)
                node = node.next_skip
        return traversal

    def add_skip_connections(self):
        self.n_skips = math.floor(math.sqrt(self.length))
        self.skip_length = math.floor(round(math.sqrt(self.length), 0))
        if self.n_skips ** 2 == self.length:
            self.n_skips = self.n_skips - 1
        """ Write logic to add skip pointers to the linked list. 
            This function does not return anything.
            To be implemented."""
        if self.length > 2:
            current_node = self.start_node
            for i in range(self.n_skips):
                node = current_node
                for j in range(self.skip_length):
                    current_node = current_node.next
                node.next_skip = current_node
        return

    def insert_at_end(self, _value, _tf, _tfidf):
        """ Write logic to add new elements to the linked list.
            Insert the element at an appropriate position, such that elements to the left are lower than the inserted
            element, and elements to the right are greater than the inserted element.
            To be implemented. """
        value = _value
        tf = _tf
        tfidf = _tfidf
        new_node = Node(value=value, tf=tf, tfidf=tfidf)
        self.length += 1
        n = self.start_node

        if self.start_node is None:
            self.start_node = new_node
            self.end_node = new_node
        elif self.start_node.value >= value:
            self.start_node = new_node
            self.start_node.next = n
        elif self.end_node.value <= value:
            self.end_node.next = new_node
            self.end_node = new_node
        else:
            while n.next is not None and n.value < value and value < self.end_node.value:
                n = n.next

            m = self.start_node
            while m.next != n and m.next is not None:
                m = m.next
            m.next = new_node
            new_node.next = n
        return

