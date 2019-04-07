### Topic Detection ###
### s2i build . registry.access.redhat.com/rhscl/python-36-rhel7:latest luke-topic-detection

import nltk
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string
import re, os
import gensim
from gensim import corpora

import json
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, json, jsonify, Response
from flask_restful import reqparse, abort, Api, Resource
from flask import Flask
app = Flask(__name__)
api = Api(app)
import sys

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()

def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

@app.route('/topic_detection_api', methods=['GET','POST']) 
def topic_detection_api():
    
    textdata = request.json
    
    jsondata = json.loads(textdata)
    strdata = jsondata['data']	
    print(strdata, file=sys.stderr) # print to python console
    
    doc_complete = [strdata]


    doc_clean = [clean(doc).split() for doc in doc_complete]
     
    # Creating the term dictionary of the corpus, where every unique term is assigned an index. 
    dictionary = corpora.Dictionary(doc_clean)
    
    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
    
    # Creating the object for LDA model using gensim library
    Lda = gensim.models.ldamodel.LdaModel
                
    # Running and Training LDA model on the document term matrix.
    ldamodel = Lda(doc_term_matrix, num_topics=10, id2word = dictionary, passes=10)
    output = ldamodel.print_topics(num_topics=1, num_words=5)
    
    strItem = ""
    for item in output:
        strItem = strItem+" "+str(item)
     
    json_str = json.dumps(strItem)
	
    #json_str = "test"
    
    return jsonify(resp=json_str)

#api.add_resource(extract_entity_api, '/')

if __name__ == '__main__':
    #app.run(host='0.0.0.0')
    app.run(host='0.0.0.0', debug=True, port=8080)