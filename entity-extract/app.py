### Entities extraction
###s2i build . registry.access.redhat.com/rhscl/python-36-rhel7:latest luke-entity-extract

import nltk
import json
from flask import Flask, request, session, g, redirect, url_for, abort, \
	render_template, flash, json, jsonify, Response
from flask_restful import reqparse, abort, Api, Resource

from flask import Flask
app = Flask(__name__)
api = Api(app)
import sys

@app.route('/extract_entity_api', methods=['GET','POST']) 
def extract_entity_api():
#def extract_entity_api(textdata):
	#textdata = request.data.get_json()
	textdata = request.json
	
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
	return jsonify(resp=json_str)

#api.add_resource(extract_entity_api, '/')

if __name__ == '__main__':
	#app.run(host='0.0.0.0')
	app.run(host='0.0.0.0', debug=True, port=8080)
