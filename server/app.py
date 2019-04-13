import os
import glob

from flask import Flask, request, send_from_directory
from google_images_download import google_images_download

app = Flask(__name__, static_url_path='/EZ-CV/client')

# Static Files
@app.route('/')
def index(): return send_from_directory('../client/', 'index.html')
@app.route('/style.css')
def style(): return send_from_directory('../client/', 'style.css')

# Static Image Serving

img_dir = '/home/sagrawa2/EZ-CV/images/'

@app.route('/img/<path:path>')
def send_image(path):
	return send_from_directory('/../images', path)

# Search for images
@app.route('/image_search', methods=['POST'])
def image_search():

	# Delete all images in the image directory
	old_imgs = glob.glob(img_dir + "*")
	for f in files: os.remove(f)

	# Download the new images
	query = request.get_json()['query']
	response = google_images_download.googleimagesdownload()
	absolute_image_paths = response.download({
		'keywords': query,
		'limit': 20,
		'output_directory': img_dir
	})

	return 'all good'

# Train the model
@app.route('/train_model', methods=['POST'])
def train_model():
	print(request.data)
	return 'all good'

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)
	print('Server hosted at: 35.237.13.210:8080')