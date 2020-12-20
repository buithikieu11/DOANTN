import os
import logging
import random
from flask import Flask, jsonify
from flask import request
import json 
from bson import json_util 
import numpy as np
import pymongo
import settings
import markdown2
import os, sys
from flask_cors import CORS
import datetime, time
import requests
import joblib
from operator import itemgetter
from time import sleep
# lấy ra đường dẫn đến thư mục modules ở trong projetc hiện hành
lib_path = os.path.abspath(os.path.join('src'))
# thêm thư mục cần load vào trong hệ thống
sys.path.append(lib_path)
from distances import get_most_similar_documents
from lda_models import make_texts_corpus
from utils import html_to_text

client = pymongo.MongoClient(settings.MONGODB_SETTINGS["host"])
db = client[settings.MONGODB_SETTINGS["db"]]
mongo_col = db[settings.MONGODB_SETTINGS["collection"]]

app = Flask(__name__)
CORS(app)
app.secret_key = os.environ.get("SECRET_KEY", "framgia123")

# app.config.from_object('web.config.DevelopmentConfig')
logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO
)


def load_model():
    import gensim  # noqa
    # load LDA model
    lda_model = gensim.models.LdaModel.load(
        settings.PATH_LDA_MODEL
    )
    # load corpus
    corpus = gensim.corpora.MmCorpus(
        settings.PATH_CORPUS
    )
    # load dictionary
    id2word = gensim.corpora.Dictionary.load(
        settings.PATH_DICTIONARY
    )
    # load documents topic distribution matrix
    doc_topic_dist = joblib.load(
        settings.PATH_DOC_TOPIC_DIST
    )
    # doc_topic_dist = np.array([np.array(dist) for dist in doc_topic_dist])

    return lda_model, corpus, id2word, doc_topic_dist


lda_model, corpus, id2word, doc_topic_dist = load_model()
@app.route('/api/post', methods=["POST"])
def test():
   point = []
   list_url = []
   list_max_point = []
   post_id = 0
   recent_time = 0
   temp = 0
   data = request.get_json()
   clicked = data["clicked"]
   mouse_scrolled = data["mouseScrolled"]
   click_arr = clicked['clickedDetails']
   i = 0
   j = 0
   k = 0
   index = -1
   while(i<len(click_arr) and len(click_arr)>0) :
       if(click_arr[i]['at_time']>recent_time): 
            recent_time = click_arr[k]['at_time']
            temp = i
       slug = click_arr[i]['url'].split("-")[-1]
       find_post = mongo_col.find_one({"slug":slug})
       if (find_post ==  None) :
        print("ok")
        fmt_url = "https://viblo.asia/api/posts/{}"
        req = requests.get(fmt_url.format(slug))
        post = req.json()['post']
        data = post['data']
        mongo_col.insert_one({
                "idrs":mongo_col.count(),
                'id': data['id'] ,
                'title': data['title'],
                'slug': data['slug'],
                'url': data['canonical_url'],
                'content': data['contents'],
                'reading_time': data['reading_time']
            })
        viblo_time = data['reading_time']    
        tam = joblib.load(
         settings.PATH_DOC_TOPIC_DIST
         )
        content = html_to_text(markdown2.markdown(data["contents"]))
        text_corpus = make_texts_corpus([content])
        bow = id2word.doc2bow(next(text_corpus))
        doc_distribution = np.array([doc_top[1] for doc_top in lda_model.get_document_topics(bow=bow)]) 
        doc_topic_dis = np.vstack([tam,doc_distribution])
        joblib.dump(doc_topic_dis, 'models/doc_topic_dist.dat')
       else: viblo_time = find_post['reading_time']  
       point.append(0)
       reading_time = mouse_scrolled[i]['reading_time']/60 #convert to minius
       point[i] = point[i]+click_arr[i]['count']+mouse_scrolled[i]['percentage_scrolled']
       if(reading_time>=viblo_time): point[i]+=100
       else: point[i]+=(reading_time/viblo_time)*100
       i+=1
   recent_time = 0
   while j <len(point): 
        if(recent_time<click_arr[j]['at_time'] and point[j]>=150):
            recent_time = click_arr[j]['at_time']
            index = j
        j+=1
   if(index==-1):
       print(temp) 
       slug = click_arr[temp]['url'].split("-")[-1]
       find_post = mongo_col.find_one({"slug":slug})
       content = html_to_text(markdown2.markdown(find_post["content"]))
       text_corpus = make_texts_corpus([content])
       bow = id2word.doc2bow(next(text_corpus))
       doc_distribution = np.array([doc_top[1] for doc_top in lda_model.get_document_topics(bow=bow)])
       doc_topic_dist = joblib.load(
       settings.PATH_DOC_TOPIC_DIST)  
       most_sim_ids = list(get_most_similar_documents(doc_distribution, doc_topic_dist))[1:]
       most_sim_ids = [int(id_) for id_ in most_sim_ids]
       print(most_sim_ids)
       posts = list(mongo_col.find({"idrs": {"$in": most_sim_ids}}))
       temp = 0
       return json.dumps(posts, default=json_util.default)   
   else:
       #Neu cac bai post co cung diem so thi chon bai vua moi kich
        slug = click_arr[index]['url'].split("-")[-1]
        find_post = mongo_col.find_one({"slug":slug})
        content = html_to_text(markdown2.markdown(find_post["content"]))
        text_corpus = make_texts_corpus([content])
        bow = id2word.doc2bow(next(text_corpus))
        doc_distribution = np.array([doc_top[1] for doc_top in lda_model.get_document_topics(bow=bow)])
        doc_topic_dist = joblib.load(
        settings.PATH_DOC_TOPIC_DIST)  
        most_sim_ids = list(get_most_similar_documents(doc_distribution, doc_topic_dist))[1:]
        most_sim_ids = [int(id_) for id_ in most_sim_ids]
        posts = list(mongo_col.find({"idrs": {"$in": most_sim_ids}}))
        index = 0 
        return json.dumps(posts, default=json_util.default)    
if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
