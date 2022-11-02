# -*- coding: utf-8 -*-


import json
from Preprocessor import detect_lang, preprocess_all, remove_specials
import urllib.request

f = open("data/test-queries.txt", "r")
queries = []
for x in f:
  queries.append(x)

ir_models = ['BM25', 'VSM']

for model in ir_models:
  sample_trec_input_file = open('data/sample_trec_input_'+model.lower()+'.txt', 'w+')
  for query in queries:
      a = query.split(' ')
      query_number = a[0]
      query_text = ' '.join(a[1:])
      
      lang = detect_lang(query_text)
      text_key = 'text_' + lang
      preprocess_text = preprocess_all({text_key: query_text, 'lang': lang})
      parsed_query = urllib.parse.quote(remove_specials(query_text))
      final_query: dict = {
          'en': urllib.parse.quote(preprocess_text['text_en']),
          'de': urllib.parse.quote(preprocess_text['text_de']),
          'ru': urllib.parse.quote(preprocess_text['text_ru'])
      }
      final_query[lang] = urllib.parse.quote(query_text.replace(':', ''))
            
      inurl = 'http://localhost:8983/solr/' + model + '/select?q=' + \
              'text_en%3A(' + final_query['en'] + ')' + \
              '%20OR%20text_ru%3A(' + final_query['de'] + ')' + \
              '%20OR%20text_de%3A(' + final_query['ru'] + ')' + \
              '%20OR%20text_processed_en%3A(' + parsed_query + ')' + \
              '%20OR%20text_processed_ru%3A(' + parsed_query + ')' + \
              '%20OR%20text_processed_de%3A(' + parsed_query + ')' + \
              '&fl=id%2Cscore&rows=20&wt=json&indent=true'

      data = urllib.request.urlopen(inurl)
      responses = json.load(data)['response']['docs']

      outfile = open(model + '/' + str(int(query_number)) + '.txt', 'w+')

      rank = 0
      for row in responses:
          outfile.write(query_number + ' ' + 'Q0' + ' ' + str(row['id']) + ' ' + str(rank) + ' ' + str(
              row['score']) + ' ' + model.lower() + '\n')
          sample_trec_input_file.write(query_number + ' ' + 'Q0' + ' ' + str(row['id']) + ' ' + str(rank) + ' ' + str(
              row['score']) + ' ' + model.lower() + '\n')
          rank += 1
      outfile.close()
  sample_trec_input_file.close()