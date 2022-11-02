# -*- coding: utf-8 -*-
import json
import cld3

from googletrans import Translator
translator = Translator()

lang_name: dict = {'en': 'english', 
                   'de': 'german', 
                   'ru': 'russian'}
    
def detect_lang(text) -> str:
    lang: str = cld3.get_language(text).language
    
    if lang not in lang_name.keys():
        lang = 'en'
    
    return lang

def remove_specials(text) -> str:
    text = text.replace(':', ' ')
    text = text.replace('/', ' ')
    # text = text.replace('_', ' ')
    text = text.replace('\n', '')
    text = text.replace('@', '')
    text = text.replace('#', '')
    
    clean_words = []
    for word in text.split():
        if str(word).lower().startswith('http') or str(word).lower().startswith('https') or str(word).lower().startswith('t.co'):
            continue
        clean_words.append(word)
    result = ' '.join(clean_words)
    return result

def preprocess_all(tweet: dict) -> dict:
    tweet['text_processed_en'] = ""
    tweet['text_processed_de'] = ""
    tweet['text_processed_ru'] = ""
    
    result: dict = tweet
    lang = tweet['lang']
    text = tweet['text_' + lang]
    text = remove_specials(text)
    result['text_processed_' + lang] = text
    # print(text)
    if lang == 'en':
        result['text_de'] = translator.translate(text, dest='de', src='en').text
        result['text_ru'] = translator.translate(text, dest='ru', src='en').text
    elif lang == 'de':
        result['text_en'] = translator.translate(text, dest='en', src='de').text
        result['text_ru'] = translator.translate(text, dest='ru', src='de').text
    elif lang == 'ru':
        result['text_en'] = translator.translate(text, dest='en', src='ru').text
        result['text_de'] = translator.translate(text, dest='de', src='ru').text
    
    return result

if __name__ == "__main__":
    input_path = 'data/train.json'
    output_path = 'data/train_preprocessed.json'
    
    collection = []
    with open(input_path) as f:
        collection = json.load(f)
    
    for index, _ in enumerate(collection):
        print("Process index", index)
        collection[index] = preprocess_all(collection[index])
        
    with open(output_path, "w+") as output_file:
        json.dump(collection, output_file, indent=2, sort_keys=True, ensure_ascii=False)
