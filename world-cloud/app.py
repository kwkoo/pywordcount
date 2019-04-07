### Word Clouds ###
######s2i build . registry.access.redhat.com/rhscl/python-36-rhel7:latest luke-worldcloud

from flask import Flask, send_file, request, make_response
from flask_restful import reqparse, abort, Api, Resource
from wordcloud import WordCloud
import matplotlib.pyplot as plt
plt.switch_backend('agg')

#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
#from matplotlib.figure import Figure

import json, os, io
import base64

#import urllib
#from urllib.parse import quote
 
app = Flask(__name__)
#api = Api(app)

strTweet = ''

@app.route('/wordcloud_api', methods=['GET', 'POST'])
def wordcloud_api():

	textdata = request.json
	#print(textdata)
	strDict = json.loads(textdata)
	strdata = str(strDict['data'])
	print(strdata)
	#strdata = "The quick brown fox jumps over the lazy dog"
	wc = WordCloud(max_font_size=80, background_color='black').generate(strdata)
	
	plt.imshow(wc, interpolation='bilinear')
	#plt.axis("off")
	
	img = io.BytesIO()
	plt.savefig(img, format='png')
	img.seek(0)
	img64 = base64.b64encode(img.getvalue()) #.decode('UTF-8')
	
	return img64
	#response = make_response(img.getvalue())
	#response.headers.set('Content-Type','image/png')
	#img.close() 
	
	#response = send_file(img, attachment_filename='logo.png', mimetype='image/png')

	#return response

	#wc.to_image().save(img, 'PNG')	
	#plt.savefig(img)	
	#img.seek(0)
	
	#filename = 'wordcloud_output.png'
	#imageOut = wc.to_file(filename)
		
	#return send_file(img, mimetype='image/png')


if __name__ == '__main__':
	#app.run(host='0.0.0.0')
	app.run(host='0.0.0.0', debug=True, port=8080)
    

