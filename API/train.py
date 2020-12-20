#from src.utils import markdown_to_text
from tqdm import tqdm
import pymongo
import os, sys 
from pymongo import MongoClient
import itertools
import gensim
from gensim.utils import simple_preprocess
import joblib
client = MongoClient('localhost', 27017)
db = client['rsblog']
col = db['viblo_posts']
posts = col.find()
#convert markdown to html
import markdown2
#convert html_to_text
# lấy ra đường dẫn đến thư mục modules ở trong projetc hiện hành
lib_path = os.path.abspath(os.path.join('src'))
# thêm thư mục cần load vào trong hệ thống
sys.path.append(lib_path)
from utils import html_to_text
for i, post in tqdm(enumerate(col.find()), total=col.count()):
    try:
        col.update_one({"_id": post["_id"]}, {"$set": {"idrs": i}})
        pp_content = html_to_text(markdown2.markdown(post['content']))
        col.update_one({"_id": post["_id"]}, {"$set": {"pp_content": pp_content}})
    except Exception as e:
        print(e)
        continue
def make_sentences():
    for post in col.find():
        yield post['pp_content']
 
def make_texts_corpus(sentences):
    for sentence in sentences:
        yield simple_preprocess(sentence, deacc=True)

#         yield [word for word in sentence.split()]
class StreamCorpus(object):
    def __init__(self, sentences, dictionary, clip_docs=None):
        """
        Parse the first `clip_docs` documents
        Yield each document in turn, as a list of tokens.
        """
        self.sentences = sentences
        self.dictionary = dictionary
        self.clip_docs = clip_docs

    def __iter__(self):
        for tokens in itertools.islice(make_texts_corpus(self.sentences),
                                       self.clip_docs):
            yield self.dictionary.doc2bow(tokens)

    def __len__(self):
        return self.clip_docs
import sys
sys.path
sentences = make_sentences()
sentences = make_texts_corpus(sentences)
id2word = gensim.corpora.Dictionary(sentences)
id2word.filter_extremes(no_below=10, no_above=0.25)
id2word.compactify()
id2word.save('models/id2word.dictionary')

len(id2word)
for i in range(10):
    print(id2word[i])
sentences = make_sentences()
corpus = StreamCorpus(sentences, id2word)
gensim.corpora.MmCorpus.serialize('models/corpus.mm', corpus)
corpus = gensim.corpora.MmCorpus('models/corpus.mm')
tfidf_model = gensim.models.TfidfModel(corpus, id2word=id2word)
lda_model = gensim.models.ldamodel.LdaModel(tfidf_model[corpus],id2word=id2word, num_topics=64, passes=10,
            chunksize=100, random_state=42, alpha=1e-2, eta=0.5e-2,
            minimum_probability=0.0, per_word_topics=False)
lda_model.save('models/LDA.model')
lda_model.print_topics(10)
import numpy as np
doc_topic_dist = np.array(
    [[tup[1] for tup in lst] for lst in lda_model[corpus]]
)
import joblib
joblib.dump(doc_topic_dist, 'models/doc_topic_dist.dat')

