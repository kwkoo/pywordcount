# all the imports
######s2i build . registry.access.redhat.com/rhscl/python-27-rhel7:latest luke-web

from __future__ import print_function
import os
from os import listdir
from os.path import isfile, join
import imghdr
import shutil
from shutil import copyfile
import sys
import subprocess

from flask import Flask, request, session, g, redirect, url_for, abort, \
	render_template, flash, json, jsonify, Response
import re

import requests

from flask_restful import reqparse, abort, Api, Resource
from distutils.dir_util import copy_tree
from werkzeug import secure_filename

import email, emaildata
from emaildata.text import Text

import HTMLParser
from nltk.tokenize import sent_tokenize

from flask import Flask
app = Flask(__name__)
app._static_folder = './static/'

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
UPLOAD_FOLDER = 'uploads/'
FS_COPY_PATH = 'outputs/keywordhits/'

# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'eml'])


URL_WORLD_CLOUD_API = os.getenv("URL_WORLD_CLOUD_API")
URL_ENTITY_API = os.getenv("URL_ENTITY_API")
URL_TOPIC_API = os.getenv("URL_TOPIC_API")
URL_SENTIMENT_API = os.getenv("URL_SENTIMENT_API")



# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
	# remove files from folder
	for fileitem in os.listdir(UPLOAD_FOLDER):
		file_path = os.path.join(UPLOAD_FOLDER, fileitem)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
		except Exception as e:
			print(e)

    # Get the name of the uploaded files
	uploaded_files = request.files.getlist("file[]")
	filenames = []
	for file in uploaded_files:
        # Check if the file is one of the allowed types/extensions
		if file and allowed_file(file.filename):
        	# Make the filename safe, remove unsupported chars
			filename = secure_filename(file.filename)
            # Move the file form the temporal folder to the upload folder we setup
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Save the filename into a list, we'll use it later
			filenames.append(filename)
		file.close()
            # Redirect the user to the uploaded_file route, which
            # will basicaly show on the browser the uploaded file
    # Load an html page with a link to each uploaded file
	return render_template('upload.html', filenames=filenames)

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/')
def index():
	#easygui.msgbox("This is a message!", title="simple gui")
	#pymsgbox.alert('This is an alert!', 'Title')
	return render_template('start.html')

#@app.route('/login') 
#def login():
#	print 'test'
#        return "Login ok"

@app.route('/wordcloud') 
def wordcloud():
	url = URL_WORLD_CLOUD_API #'http://wordclouddocker:8000/wordcloud_api'
	textData = json.dumps({"data": "this is Tom"})
	headers = {'Content-type': 'application/json'}
	
	#filepath = 'uploads/'
	filepath = UPLOAD_FOLDER

	filecount=0	
	infiles = [f for f in listdir(filepath) if isfile(join(filepath, f))]
	#print(infiles, file=sys.stderr) # print to python console
	intext=""
	imglist=[]
	if infiles=="":
		return render_template('nofile_error.html')
	else:		
		for infileName in infiles:
			
			if infileName[-3:]=="eml":
				infile = open(filepath+infileName)
				#msg = email.parser.BytesParser(policy=email.policy.default).parse(infile)
				#intext = msg.get_body(preferencelist=('plain')).get_content()
				message = email.message_from_file(infile)
				
				#msgHeaders = message['headers']
				intext = str(message.get_payload()[0])

				#intext = str(message.get_payload(decode=True))

				#print(intext, file=sys.stderr) # print to python console
			else:
				infile = open(filepath+infileName, 'r')	
				intext = infile.read()
			infile.close()
				
			textData = json.dumps({"data": intext})
			str_resp = 'false'
			
			try:
				resp = requests.post(url=url, json=textData, headers=headers) 	
				imgresp = resp.text.decode('UTF-8')
				#imgitems = [imgvalue] 		
				imglist.append(imgresp)
			except Exception as e:
				return e
	print(imglist, file=sys.stderr) # print to python console
	
	return render_template('wordcloud_response.html', imgvalue=imglist)

@app.route('/keywordsearch') 
def keywordsearch():
	#url = 'http://keywordsearch:8000/keywordsearch_api'
	#headers = {'Content-type': 'application/json'}
		
	#filepath = '/home/audi7/Dockerfiles/dockercompose/uploads/'
	#filepath = 'uploads/'
	#copypath = 'outputs/keywordhits/'

	filepath = UPLOAD_FOLDER
	copypath = FS_COPY_PATH

	# remove files from folder
	for fileitem in os.listdir(copypath):
		file_path = os.path.join(copypath, fileitem)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
		except Exception as e:
			print(e)

	# Extract keywords
	#kwfile = open('keywords.txt', 'r')

	kwfile = open('vocab/keywords', 'r')
	kwtext = kwfile.read()
	kwlist = kwtext.split('\n')
	regStr = "(\\b" 
	for kw in kwlist:
		kw=kw.lower()
		if kw == kwlist[-1]:
			regStr = regStr[:-4]
		else:
			regStr = regStr+kw+"\\b)|(\\b"

	print(regStr,file=sys.stderr)
	regStr = regStr[:-4]
	print(regStr,file=sys.stderr)
	regex = re.compile(regStr, re.I)
	print(regStr, file=sys.stderr) # print to python console

	filecount=0	
	infiles = [f for f in listdir(filepath) if isfile(join(filepath, f))]
	#print(infiles, file=sys.stderr) # print to python console
	intext=""
	if infiles=="":
		return render_template('nofile_error.html')
	else:		
		for infileName in infiles:
			
			if infileName[-3:]=="eml":
				infile = open(filepath+infileName)
				#msg = email.parser.BytesParser(policy=email.policy.default).parse(infile)
				#intext = msg.get_body(preferencelist=('plain')).get_content()
				message = email.message_from_file(infile)
				
				#msgHeaders = message['headers']
				intext = str(message.get_payload()[0])

				#intext = str(message.get_payload(decode=True))

				#print(intext, file=sys.stderr) # print to python console
			else:
				infile = open(filepath+infileName, 'r')	
				intext = infile.read()
			infile.close()
				
			textData = json.dumps({"data": intext})
			str_resp = 'false'

			if len(list(regex.finditer(intext)))>0:
				copyfile(filepath+infileName, copypath+infileName)
				filecount=filecount+1
			
			#try:
			#	resp = requests.post(url=url, json=textData, headers=headers)
				#str_data = json.loads(resp.text)
				#str_resp = str_data['result']
				#str_resp = str_resp.decode('utf8')
								
				#if str_resp == "true":
				#	print(str_resp, file=sys.stderr) # print to python console
				#	copyfile(filepath+infileName, copypath+infileName)
				#	filecount=filecount+1
				
			#except Exception as e:
			#	return e

		strfilecount = str(filecount)
		return render_template('keywordsearch_response.html', value=strfilecount)	

@app.route('/readtext') 
def readtext():

	# comments - run "sudo docker network ls" and "docker network inspect" in cmd line to get ip address of extract entity node
	#url = 'http://172.26.0.2:8000/extract_entity_api'	
	#url = 'http://readtext:8000/readtext_api'
	#headers = {'Content-type': 'application/json'}

	# Extract keywords
	#kwfile = open('keywords.txt', 'r')
	kwfile = open('vocab/keywords', 'r')
	
	kwtext = kwfile.read()
	kwlist = kwtext.split('\n')
	regStr = "(\\b" 
	for kw in kwlist:
		kw=kw.lower()
		if kw == kwlist[-1]:
			regStr = regStr[:-4]
		else:
			regStr = regStr+kw+"\\b)|(\\b"
	
	regex = re.compile(regStr, re.I)
	#regex = re.compile(r"(\bfairuzjunaidi@gmail.com\b)|(\bSingapore\b)|(\bcpf\b)", re.I)
	
	COLOR='red'
	
	#filepath = 'outputs/keywordhits/'
	filepath = FS_COPY_PATH
	

	infiles = [f for f in listdir(filepath) if isfile(join(filepath, f))]
	#texttData = json.dumps({"data": "this is Tom and Jane"})
	#print(infiles, file=sys.stderr) # print to python console
	if len(infiles)==0:
		return render_template('nofile_error.html')
	else:
		#fileList = []
		str_overall_resp=""		
		for infileName in infiles:
			output=""
			intext=""
			stroutput=""
			str_overall_resp = str_overall_resp+"<h3>File Name: "+infileName+"</h3>"		
			if infileName[-3:]=="eml":
				infile = open(filepath+infileName)
				message = email.message_from_file(infile)
				
				# Multipart email implementation
				#if message.is_multipart():
				#	for part in message.get_payload():
				#		intext = str(part.get_payload())
				#else:
				#	intext = str(message.get_payload())
				
				intext = str(message.get_payload()[0])
				#print(intext, file=sys.stderr) # print to python console
			else:
				infile = open(filepath+infileName, 'r')	
				intext = infile.read()
			infile.close()
			
			i = 0; output = "&lt;html&gt;"
			#print(type(regex.finditer(intext)), file=sys.stderr) # print to python console
			
			if len(list(regex.finditer(intext)))>0:
				for m in regex.finditer(intext):
					output+="".join([intext[i:m.start()],
					"&lt;strong&gt;&lt;span style='color:%s'&gt;" % COLOR,
					intext[m.start():m.end()],
					"&lt;/span&gt;&lt;/strong&gt;"])
					#print(m, file=sys.stderr) # print to python console
					i=m.end()
				stroutput = "".join([output, intext[m.end():], "&lt;/html&gt;"])
			else:
				stroutput = output+"&lt;/html&gt;"
			
			stroutput = stroutput.replace("\r\n", "<br />")
			str_overall_resp = str_overall_resp+"<br/>"+stroutput+"<br>"
		str_overall_resp = str_overall_resp.decode('utf8')
		str_overall_resp_decoded = HTMLParser.HTMLParser().unescape(str_overall_resp)
		
		return str_overall_resp_decoded

@app.route('/extract_entity') 
def extract_entity():

	# comments - run "sudo docker network ls" and "docker network inspect" in cmd line to get ip address of extract entity node
	#url = 'http://entitiesextraction:8000/extract_entity_api'
	url = URL_ENTITY_API 
	headers = {'Content-type': 'application/json'}

	#filepath = '/home/audi7/Dockerfiles/dockercompose/uploads/'
	#filepath = 'uploads/'
	filepath = UPLOAD_FOLDER
	resp_list=[]

	infiles = [f for f in listdir(filepath) if isfile(join(filepath, f))]
	#texttData = json.dumps({"data": "this is Tom and Jane"})
	print(infiles, file=sys.stderr) # print to python console
	if infiles=="":
		return render_template('nofile_error.html')
	else:		
		for infile in infiles:
			resp_list.append(str(infile))
			
			intext = open(filepath+infile, 'r').read()
	
			textData = json.dumps({"data": intext})
			
			#texttData = json.dumps({"data": "this is Tom and Jane"})
			try:
				resp = requests.post(url=url, json=textData, headers=headers)
				#str_resp = str(json.loads(resp.text))
				str_resp = resp.text
				str_resp = str_resp.replace("[","")
				str_resp = str_resp.replace("]","")
				str_resp = str_resp.replace("\\","")
				str_resp = str_resp.replace("{ \"resp\":","")
				print(resp.text, file=sys.stderr)
				resp_list.append(str_resp)

			except Exception as e:
				return e

		return render_template('entity_response.html', value=resp_list)	

@app.route('/topic_detection') 
def topic_detection():

	# comments - run "sudo docker network ls" and "docker network inspect" in cmd line to get ip address of extract entity node
		
	#url = 'http://topicdetection:8000/topic_detection_api'
	url = URL_TOPIC_API 
	headers = {'Content-type': 'application/json'}

	#filepath = '/home/audi7/Dockerfiles/dockercompose/uploads/'
	#filepath = 'uploads/'
	filepath = UPLOAD_FOLDER
	resp_list=[]

	infiles = [f for f in listdir(filepath) if isfile(join(filepath, f))]
	#texttData = json.dumps({"data": "this is Tom and Jane"})
	print(infiles, file=sys.stderr) # print to python console
	if infiles=="":
		return render_template('nofile_error.html')
	else:		
		for infile in infiles:
			resp_list.append(str(infile))
			
			intext = open(filepath+infile, 'r').read()
	
			textData = json.dumps({"data": intext})
			
			#texttData = json.dumps({"data": "this is Tom and Jane"})
			#print(textData, file=sys.stderr) # print to python console
			try:
				resp = requests.post(url=url, json=textData, headers=headers)
				#str_resp = str(json.loads(resp.text))
				str_resp = resp.text
				str_resp = str_resp.replace("[","")
				str_resp = str_resp.replace("]","")
				str_resp = str_resp.replace("\\","")
				str_resp = str_resp.replace("{ \"resp\":","")
				print(resp.text, file=sys.stderr)
				resp_list.append(str_resp)

			except Exception as e:
				return e

		return render_template('topicdetection_response.html', value=resp_list)	

@app.route('/sentiment_analysis') 
def sentiment_analysis():

	# comments - run "sudo docker network ls" and "docker network inspect" in cmd line to get ip address of extract entity node
		
	#url = 'http://sentimentanalysis:8000/sentiment_analysis_api'
	url = URL_SENTIMENT_API
	headers = {'Content-type': 'application/json'}

	#filepath = '/home/audi7/Dockerfiles/dockercompose/uploads/'
	#filepath = 'uploads/'
	filepath = UPLOAD_FOLDER
	resp_list=[]

	infiles = [f for f in listdir(filepath) if isfile(join(filepath, f))]
	#texttData = json.dumps({"data": "this is Tom and Jane"})
	#print(infiles, file=sys.stderr) # print to python console
	if infiles=="":
		return render_template('nofile_error.html')
	else:		
		for infile in infiles:
			resp_list.append(str(infile))
			
			intext = open(filepath+infile, 'r').read()
	
			sent_tokenize_list = sent_tokenize(intext)

			for sentence in sent_tokenize_list:
				#texttData = json.dumps({"data": "this is Tom and Jane"})
				#print(sentence, file=sys.stderr) # print to python console
				sentStr = str(sentence)
				
				textData = json.dumps({"data": sentStr})
				try:
					resp = requests.post(url=url, json=textData, headers=headers)
					str_resp = resp.text
					str_resp = str_resp.replace("[","") 
					str_resp = str_resp.replace("]","")
					resp_list.append(str_resp)
					#str_resp = str(textData) + "==" + str_resp

				except Exception as e:
					return e

		return render_template('sentimentanalysis_response.html', value=resp_list)	

if __name__ == '__main__':
	#app.run(host='0.0.0.0')
	app.run(host='0.0.0.0', debug=True, port=8080)



