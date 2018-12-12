from html import unescape
from nltk.corpus import stopwords
import string
import re
import numpy as np

bracket_text = re.compile(r'[\[\(].*[\]\)]')

def stop_words_country():
    stop = stopwords.words('english')
    stop += ['ca', "n't", "'s'", "s", 'wo']
    stop += ['like', 'got', 'yeah', 'get', 'know', 'go', 'oh', 'let', 'make', 'back', 'see', 'cause', 'wanna'] # Round 1
    stop += ['ya']#'na', 'la', 'uh'] # Round 2
    stop += string.punctuation
    stop += ['...']
    return set(stop)

def stop_words():
    stop = stopwords.words('english')
    stop += stopwords.words('spanish')
    # stop += ['intro', 'chorus', 'verse', 'outro', 'bridge'] # these should get filtered out by max_df = 0.95
    stop += ['ca', "n't", "'s'", "s", 'wo']
    stop += ['like', 'got', 'yeah', 'get', 'know', 'go', 'oh', 'let', 'make', 'back', 'see', 'cause', 'wanna'] # Round 1
    stop += ['ya', 'yah', 'yeah', 'ah', 'la', 'ooh', 'uh', 'one', 'wa', 'na'] # Round 2
    stop += ['ay', 'ayy', 'aye', 'da', 'dat', 'oo']
    stop += string.punctuation
    stop += ['...']
    return set(stop)

def my_preprocessor(doc):
    new_doc = unescape(doc).lower()  # remove HTML characters
    new_doc = re.sub(bracket_text, ' ', new_doc)  # remove any words in brackets or parentheses
    return new_doc

# ------------------
# for gensim word embeddings:

# def preproc_and_toke(doc, model):
    # return get_word_list(my_preprocessor(doc))

def get_word_list(doc):
    word_list = [x.lower() for x in wordpunct_tokenize(doc) if x not in stop_words()]
    return word_list

# def get_words_in_model_vocab(doc, model):
def preproc_and_toke(doc, model):
    doc = my_preprocessor(doc)
    word_list = get_word_list(doc)
    # also remove numbers?
    return [word for word in word_list if word in model.vocab]

def get_words_not_in_model_vocab(doc, model):
    doc = my_preprocessor(doc)
    word_list = get_word_list(doc)
    return [word for word in word_list if word not in model.vocab]

def vect_sum(doc, model):
    word_list = get_word_list(doc)
    vect = [model.word_vec(word) for word in word_list if word in model.vocab]
    return np.sum(vect, axis=0)

def vect_mean(doc, model):
    word_list = get_word_list(doc)
    vect = [model.word_vec(word) for word in word_list if word in model.vocab]
    return np.mean(vect, axis=0)
