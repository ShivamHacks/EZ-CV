import os
import glob
import json

from flask import Flask, request, send_from_directory, jsonify
from google_images_download import google_images_download

app = Flask(__name__, static_url_path='/EZ-CV/client')

server_url = '35.237.13.210:8080/'
img_dir = '/home/sagrawa2/EZ-CV/images/'

# Static Files
@app.route('/')
def index(): return send_from_directory('../client/', 'index.html')
@app.route('/style.css')
def style(): return send_from_directory('../client/', 'style.css')

# Static Image Serving

@app.route('/img/<img>')
def send_image(img):
	print('requested img: ' + img)
	return send_from_directory('/../images', img)

# Search for images
@app.route('/image_search', methods=['POST'])
def image_search():

	# Delete all images in the image directory
	old_imgs = glob.glob(img_dir + "*")
	for f in old_imgs: os.remove(f)

	# Download the new images
	query = request.get_json()['query']
	response = google_images_download.googleimagesdownload()
	absolute_image_paths = response.download({
		'keywords': query,
		'limit': 20,
		'output_directory': img_dir,
		'no_directory': True
	})

	return jsonify(
		images = [server_url + os.path.basename(img_path) for img_path in absolute_image_paths[query]]
	)

# Train the model
@app.route('/train_model', methods=['POST'])
def train_model():
	print(request.data)
	return 'all good'

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)
	print('Server hosted at: 35.237.13.210:8080')