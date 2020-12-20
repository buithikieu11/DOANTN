#from src.utils import markdown_to_text
import numpy as np
from tqdm import tqdm
import pymongo
import os, sys
from matplotlib import pyplot as plt    
from pymongo import MongoClient
import itertools
import gensim
from gensim.utils import simple_preprocess
import joblib
import settings
client = MongoClient('localhost', 27017)
db = client['rsblog']
col = db['viblo_posts']
posts = col.find()
client = MongoClient('localhost', 27017)
db = client['rsblog']
col = db['viblo_posts']
posts = col.find()
def make_sentences():
    for post in col.find():
        yield post['pp_content']
def make_texts_corpus(sentences):
    for sentence in sentences:
        yield simple_preprocess(sentence, deacc=True)
def main():    
    texts = make_sentences()
    print(texts)
    texts = make_texts_corpus(texts)
    print(texts)
    lda_model = gensim.models.LdaModel.load(
    settings.PATH_LDA_MODEL
    )
     # load dictionary
    id2word = gensim.corpora.Dictionary.load(
        settings.PATH_DICTIONARY
    )
    # corpus = [id2word.doc2bow(text) for text in texts]
    # print(corpus)
   
    coherence_model_lda =  gensim.models.coherencemodel.CoherenceModel(model=lda_model, texts=texts, dictionary=id2word, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    print('\nCoherence Score: ', coherence_lda)
if __name__ == "__main__":
    main()