
import numpy
import re
import json
import requests
import random

def tokenize(sentences):
    words = []
    for sentence in sentences:
        w = word_extraction(sentence)
        words.extend(w)

    words = sorted(list(set(words)))
    return words

def word_extraction(sentence):
    ignore = ['a', "the", "is"]
    words = re.sub("[^\w]", " ",  sentence).split()
    cleaned_text = [w.lower() for w in words if w not in ignore]
    return cleaned_text

def generate_bow(allsentences):
    if len(allsentences) < 1:
        allsentences = ['Empty article']
    vocab = tokenize(allsentences)
    vectors = []
    for sentence in allsentences:
        words = word_extraction(sentence)
        bag_vector = numpy.zeros(len(vocab))
        for w in words:
            for i,word in enumerate(vocab):
                if word == w:
                    bag_vector[i] += 1

        vectors.append(bag_vector)
    return vectors

def get_sentences(url):

    res = requests.get(url)
    if res.status_code != 200:
        return ['Failed to fetch the article']
    return res.text.split('\n')

def function_handler(event, context):
    url = event['article']
    sentences = get_sentences(url)
    vectors = generate_bow(sentences)
    response = {'statusCode':200, 'body': str(vectors)}
    return response
