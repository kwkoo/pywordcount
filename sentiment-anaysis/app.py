### Topic Detection ###
###s2i build . registry.access.redhat.com/rhscl/python-36-rhel7:latest luke-sentiment

import nltk
import string
import re, os

from textblob import TextBlob

import json
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, json, jsonify, Response
from flask_restful import reqparse, abort, Api, Resource
from flask import Flask
import sys

app = Flask(__name__)
api = Api(app)

def analyze_sentiment(strdata):
    analysis = TextBlob(strdata)
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1

@app.route('/sentiment_analysis_api', methods=['GET','POST']) 
def sentiment_analysis_api():
    
    textdata = request.json
    
    jsondata = json.loads(textdata)
    strdata = jsondata['data']	
    print(strdata, file=sys.stderr) # print to python console
    
    sentpolarity = str(analyze_sentiment(strdata))
         
    json_str = json.dumps(sentpolarity)
    print(json_str, file=sys.stderr)
    #json_str = "test"
    
    return jsonify(resp=json_str)

if __name__ == '__main__':
    #app.run(host='0.0.0.0')
    app.run(host='0.0.0.0', debug=True, port=8080)