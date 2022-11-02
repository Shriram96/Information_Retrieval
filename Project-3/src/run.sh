#!/bin/sh
rm -rf ../data/sample_trec_input_bm25.txt ../data/sample_trec_input_vsm.txt ../data/sample_trec_output_bm25.txt ../data/sample_trec_output_vsm.txt ../data/all_map_bm25.log ../data/all_map_vsm.log

python3 ./Preprocessor.py
python3 ./BM25_Indexer.py
python3 ./VSM_Indexer.py
python3 ./json_to_trec.py

./trec_eval -q -c -M 1000 ../data/qrel.txt ../data/sample_trec_input_bm25.txt > ../data/sample_trec_output_bm25.txt
cat ../data/sample_trec_output_bm25.txt | grep "map" > ../data/all_map_bm25.log

./trec_eval -q -c -M 1000 ../data/qrel.txt ../data/sample_trec_input_vsm.txt > ../data/sample_trec_output_vsm.txt
cat ../data/sample_trec_output_vsm.txt | grep "map" > ../data/all_map_vsm.log