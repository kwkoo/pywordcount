### Entities extraction
###s2i build . registry.access.redhat.com/rhscl/python-36-rhel7:latest luke-entity-extract

import nltk
import json
from flask import Flask, request, session, g, redirect, url_for, abort, \
	render_template, flash, json, jsonify, Response
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS, cross_origin

from flask import Flask
app = Flask(__name__)
CORS(app)
api = Api(app)
import sys


@app.route('/extract_entity_api', methods=['GET','POST']) 
def extract_entity_api():
	textdata = request.get_data().decode("utf-8")
	if textdata is None:
		resp=jsonify({"error": "no data"})
		return resp

	print(textdata)
	
	jsondata = json.loads(textdata)
	strdata = jsondata['data']
	print(strdata, file=sys.stderr) # print to python console
	outputList = []

	for sent in nltk.sent_tokenize(strdata):
		for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
			if hasattr(chunk, 'label'):
				print(chunk.label(), ' '.join(c[0] for c in chunk))
				#strA = str(chunk.label(), ' '.join(c[0] for c in chunk))
				out = chunk.label(), ' '.join(c[0] for c in chunk)		
				outputList.append(out)

	json_str = json.dumps(outputList)
	
	#json_str = "test"
	resp=jsonify(json_str)
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp

#api.add_resource(extract_entity_api, '/')

if __name__ == '__main__':
	#app.run(host='0.0.0.0')
	app.run(host='0.0.0.0', debug=True, port=8080)
