'''
@author: Sougata Saha
Institute: University at Buffalo
'''

from linkedlist import LinkedList
from collections import OrderedDict, Counter


class Indexer:
    def __init__(self):
        """ Add more attributes if needed"""
        self.inverted_index = OrderedDict({})
        self.doc_ids = set()

    def get_index(self):
        """ Function to get the index.
            Already implemented."""
        return self.inverted_index

    def generate_inverted_index(self, doc_id, tokenized_document):
        """ This function adds each tokenized document to the index. This in turn uses the function add_to_index
            Already implemented."""

        self.doc_ids.add(doc_id)
        doc_length = len(tokenized_document)
        term_count = Counter(tokenized_document)

        for term, count in term_count.items():
            self.add_to_index(term, doc_id, (count / doc_length))

    def add_to_index(self, term_, doc_id_, term_frequency):
        """ This function adds each term & document id to the index.
            If a term is not present in the index, then add the term to the index & initialize a new postings list (linked list).
            If a term is present, then add the document to the appropriate position in the posstings list of the term.
            To be implemented."""
        postings_list = LinkedList()
        if term_ in self.inverted_index:
            postings_list = self.inverted_index.get(term_)
        
        postings_list.insert_at_end(doc_id_, term_frequency, None)
        self.inverted_index[term_] = postings_list
        return

    def sort_terms(self):
        """ Sorting the index by terms.
            Already implemented."""
        sorted_index = OrderedDict({})
        for k in sorted(self.inverted_index.keys()):
            sorted_index[k] = self.inverted_index[k]
        self.inverted_index = sorted_index

    def add_skip_connections(self):
        """ For each postings list in the index, add skip pointers.
            To be implemented."""
        for term in self.inverted_index:
            posting_list = self.inverted_index.get(term)
            posting_list.add_skip_connections()
        return

    def calculate_tf_idf(self):
        """ Calculate tf-idf score for each document in the postings lists of the index.
            To be implemented."""
        for term in self.inverted_index:
            posting_list = self.inverted_index.get(term)
            posting_list.idf = len(self.doc_ids) / (posting_list.length)
            node = posting_list.start_node
            while node is not None:
                node.tfidf = posting_list.idf * node.tf
                node = node.next
        return