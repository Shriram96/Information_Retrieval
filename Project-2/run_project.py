'''
@author: Sougata Saha
Institute: University at Buffalo
'''

from tqdm import tqdm
from preprocessor import Preprocessor
from indexer import Indexer
from linkedlist import LinkedList
import argparse
import json
import time
import random
import flask
import hashlib

app = flask.Flask(__name__)


class ProjectRunner:
    def __init__(self):
        self.preprocessor = Preprocessor()
        self.indexer = Indexer()

    def _merge(self, postings_1, postings_2, skip = False):
        """ Implement the merge algorithm to merge 2 postings list at a time.
            Use appropriate parameters & return types.
            While merging 2 postings list, preserve the maximum tf-idf value of a document.
            To be implemented."""
        node_1 = postings_1.start_node
        node_2 = postings_2.start_node
        num_comparisons = 0
        merged_list = LinkedList()
        if not skip:
            while node_1 is not None and node_2 is not None:
                num_comparisons += 1
                if node_1.value == node_2.value:
                    decider_tf = max(node_1.tf, node_2.tf)
                    decider_tfidf = max(node_1.tfidf, node_2.tfidf)
                    merged_list.insert_at_end(node_1.value, decider_tf, decider_tfidf)
                    node_1 = node_1.next
                    node_2 = node_2.next
                elif node_1.value < node_2.value:
                    node_1 = node_1.next
                else:
                    node_2 = node_2.next
        else:
            while node_1 is not None and node_2 is not None:
                num_comparisons += 1
                if node_1.value == node_2.value:
                    decider_tf = max(node_1.tf, node_2.tf)
                    decider_tfidf = max(node_1.tfidf, node_2.tfidf)
                    merged_list.insert_at_end(node_1.value, decider_tf, decider_tfidf)
                    node_1 = node_1.next
                    node_2 = node_2.next
                elif node_1.next_skip is not None and node_1.next_skip.value <= node_2.value:
                    node_1 = node_1.next_skip
                elif node_2.next_skip is not None and node_2.next_skip.value <= node_1.value:
                    node_2 = node_2.next_skip
                elif node_1.value < node_2.value:
                    node_1 = node_1.next
                else:
                    node_2 = node_2.next
            merged_list.add_skip_connections()
        return num_comparisons, merged_list

    def _daat_and(self, query_terms, skip=False):
        """ Implement the DAAT AND algorithm, which merges the postings list of N query terms.
            Use appropriate parameters & return types.
            To be implemented."""
        merged_list = None
        num_comparisons = 0
        if len(query_terms) == 1:
            term_postings = self._get_postings(query_terms[0])
            merged_list = term_postings
        elif len(query_terms) >= 2:
            term_to_postings = dict()
            for term in query_terms:
                term_postings = self._get_postings(term)
                term_to_postings[term] = term_postings.length

            input_term_arr = []
            for term, _ in sorted(term_to_postings.items(), key = lambda term_len: term_len[1]):
                input_term_arr.append(term)
            
            input_term_len = len(input_term_arr)
            for i in range(input_term_len - 1):
                temp_comparisons = 0
                postings_1 = merged_list
                if postings_1 is None:
                    postings_1 = self._get_postings(input_term_arr[i])
                    
                postings_2 = self._get_postings(input_term_arr[i + 1])
                temp_comparisons, merged_list = self._merge(postings_1, postings_2, skip)
                num_comparisons += temp_comparisons

        if merged_list is None:
            merged_list = LinkedList()
        return num_comparisons, merged_list

    def _get_postings(self, term):
        """ Function to get the postings list of a term from the index.
            Use appropriate parameters & return types.
            To be implemented."""
        postings_list = LinkedList()

        if term in self.indexer.get_index():
            postings_list = self.indexer.get_index().get(term)

        return postings_list

    def _output_formatter(self, op):
        """ This formats the result in the required format.
            Do NOT change."""
        if op is None or len(op) == 0:
            return [], 0
        op_no_score = [int(i) for i in op]
        results_cnt = len(op_no_score)
        return op_no_score, results_cnt

    def run_indexer(self, corpus):
        """ This function reads & indexes the corpus. After creating the inverted index,
            it sorts the index by the terms, add skip pointers, and calculates the tf-idf scores.
            Already implemented, but you can modify the orchestration, as you seem fit."""
        with open(corpus, 'r') as fp:
            for line in tqdm(fp.readlines()):
                doc_id, document = self.preprocessor.get_doc_id(line)
                tokenized_document = self.preprocessor.tokenizer(document)
                self.indexer.generate_inverted_index(doc_id, tokenized_document)
        self.indexer.sort_terms()
        self.indexer.add_skip_connections()
        self.indexer.calculate_tf_idf()

    def sanity_checker(self, command):
        """ DO NOT MODIFY THIS. THIS IS USED BY THE GRADER. """

        index = self.indexer.get_index()
        kw = random.choice(list(index.keys()))
        return {"index_type": str(type(index)),
                "indexer_type": str(type(self.indexer)),
                "post_mem": str(index[kw]),
                "post_type": str(type(index[kw])),
                "node_mem": str(index[kw].start_node),
                "node_type": str(type(index[kw].start_node)),
                "node_value": str(index[kw].start_node.value),
                "command_result": eval(command) if "." in command else ""}

    def run_queries(self, query_list, random_command):
        """ DO NOT CHANGE THE output_dict definition"""
        output_dict = {'postingsList': {},
                       'postingsListSkip': {},
                       'daatAnd': {},
                       'daatAndSkip': {},
                       'daatAndTfIdf': {},
                       'daatAndSkipTfIdf': {},
                       'sanity': self.sanity_checker(random_command)}

        for query in tqdm(query_list):
            """ Run each query against the index. You should do the following for each query:
                1. Pre-process & tokenize the query.
                2. For each query token, get the postings list & postings list with skip pointers.
                3. Get the DAAT AND query results & number of comparisons with & without skip pointers.
                4. Get the DAAT AND query results & number of comparisons with & without skip pointers, 
                    along with sorting by tf-idf scores."""

            input_term_arr = self.preprocessor.tokenizer(query)  # Tokenized query. To be implemented.

            for term in input_term_arr:
                all_postings = self._get_postings(term)
                postings = all_postings.traverse_list()
                skip_postings = all_postings.traverse_skips()
                """ Implement logic to populate initialize the above variables.
                    The below code formats your result to the required format.
                    To be implemented."""

                output_dict['postingsList'][term] = postings
                output_dict['postingsListSkip'][term] = skip_postings

            and_op_no_skip, and_op_skip, and_op_no_skip_sorted, and_op_skip_sorted = None, None, None, None
            and_comparisons_no_skip, and_comparisons_skip, \
                and_comparisons_no_skip_sorted, and_comparisons_skip_sorted = None, None, None, None

            and_comparisons_no_skip, and_op_no_skip = self._daat_and(input_term_arr)
            node_list = []
            node = and_op_no_skip.start_node
            while node is not None:
                node_list.append([node.value, node.tfidf])
                node = node.next
            and_op_no_skip_sorted = []
            for [value, _] in sorted(node_list, key = lambda x: x[1], reverse = True):
                and_op_no_skip_sorted.append(value)
            and_comparisons_no_skip_sorted = and_comparisons_no_skip
            and_op_no_skip = and_op_no_skip.traverse_list()

            and_comparisons_skip, and_op_skip = self._daat_and(input_term_arr, True)
            node_list = []
            node = and_op_skip.start_node
            while node is not None:
                node_list.append([node.value, node.tfidf])
                node = node.next
            and_op_skip_sorted = []
            for [value, _] in sorted(node_list, key = lambda x: x[1], reverse = True):
                and_op_skip_sorted.append(value)
            and_comparisons_skip_sorted = and_comparisons_skip
            and_op_skip = and_op_skip.traverse_list()

            """ Implement logic to populate initialize the above variables.
                The below code formats your result to the required format.
                To be implemented."""
            and_op_no_score_no_skip, and_results_cnt_no_skip = self._output_formatter(and_op_no_skip)
            and_op_no_score_skip, and_results_cnt_skip = self._output_formatter(and_op_skip)
            and_op_no_score_no_skip_sorted, and_results_cnt_no_skip_sorted = self._output_formatter(and_op_no_skip_sorted)
            and_op_no_score_skip_sorted, and_results_cnt_skip_sorted = self._output_formatter(and_op_skip_sorted)

            output_dict['daatAnd'][query.strip()] = {}
            output_dict['daatAnd'][query.strip()]['results'] = and_op_no_score_no_skip
            output_dict['daatAnd'][query.strip()]['num_docs'] = and_results_cnt_no_skip
            output_dict['daatAnd'][query.strip()]['num_comparisons'] = and_comparisons_no_skip

            output_dict['daatAndSkip'][query.strip()] = {}
            output_dict['daatAndSkip'][query.strip()]['results'] = and_op_no_score_skip
            output_dict['daatAndSkip'][query.strip()]['num_docs'] = and_results_cnt_skip
            output_dict['daatAndSkip'][query.strip()]['num_comparisons'] = and_comparisons_skip

            output_dict['daatAndTfIdf'][query.strip()] = {}
            output_dict['daatAndTfIdf'][query.strip()]['results'] = and_op_no_score_no_skip_sorted
            output_dict['daatAndTfIdf'][query.strip()]['num_docs'] = and_results_cnt_no_skip_sorted
            output_dict['daatAndTfIdf'][query.strip()]['num_comparisons'] = and_comparisons_no_skip_sorted

            output_dict['daatAndSkipTfIdf'][query.strip()] = {}
            output_dict['daatAndSkipTfIdf'][query.strip()]['results'] = and_op_no_score_skip_sorted
            output_dict['daatAndSkipTfIdf'][query.strip()]['num_docs'] = and_results_cnt_skip_sorted
            output_dict['daatAndSkipTfIdf'][query.strip()]['num_comparisons'] = and_comparisons_skip_sorted

        return output_dict


@app.route("/execute_query", methods=['POST'])
def execute_query():
    """ This function handles the POST request to your endpoint.
        Do NOT change it."""
    start_time = time.time()

    queries = flask.request.json["queries"]
    print("Queries:", queries)
    random_command = flask.request.json["random_command"]
    print("Random Command:", random_command)

    """ Running the queries against the pre-loaded index. """
    output_dict = runner.run_queries(queries, random_command)

    """ Dumping the results to a JSON file. """
    with open(output_location, 'w') as fp:
        json.dump(output_dict, fp)

    response = {
        "Response": output_dict,
        "time_taken": str(time.time() - start_time),
        "username_hash": username_hash
    }
    return flask.jsonify(response)


if __name__ == "__main__":
    """ Driver code for the project, which defines the global variables.
        Do NOT change it."""

    output_location = "project2_output.json"
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--corpus", type=str, help="Corpus File name, with path.")
    parser.add_argument("--output_location", type=str, help="Output file name.", default=output_location)
    parser.add_argument("--username", type=str,
                        help="Your UB username. It's the part of your UB email id before the @buffalo.edu. "
                             "DO NOT pass incorrect value here")

    argv = parser.parse_args()

    corpus = argv.corpus
    output_location = argv.output_location
    username_hash = hashlib.md5(argv.username.encode()).hexdigest()

    """ Initialize the project runner"""
    runner = ProjectRunner()

    """ Index the documents from beforehand. When the API endpoint is hit, queries are run against 
        this pre-loaded in memory index. """
    runner.run_indexer(corpus)

    app.run(host="0.0.0.0", port=9999)
