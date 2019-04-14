import os
import glob
import json
import shutil

from flask import Flask, request, send_from_directory, jsonify
from google_images_download import google_images_download

app = Flask(__name__)

port = 8080
server_url = '35.237.13.210:8080/'
img_dir = '/home/sagrawa2/EZ-CV/images/'

#port = 3000
#server_url = 'http://localhost:3000/'
#img_dir = '/Users/shivamagrawal/Desktop/Bitcamp2019/images'

# Static Files
@app.route('/')
def index(): return send_from_directory('../client/', 'index.html')
@app.route('/style.css')
def style(): return send_from_directory('../client/', 'style.css')
@app.route('/fancy.css')
def fancy(): return send_from_directory('../client/', 'fancy.css')

# Static Image Serving

@app.route('/img/<img>')
def send_image(img):
	return send_from_directory('../images/', img)

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
		'limit': 10,
		'output_directory': img_dir,
		'no_directory': True
	})

	return jsonify(
		['http://' + server_url + 'img/' + os.path.basename(img_path) for img_path in absolute_image_paths[query]]
	)

# Train the model
@app.route('/train_model', methods=['POST'])
def train_model():
	annotations = request.get_json()
	with open('../keras_frcnn/kitti_simple_label.txt', 'w') as f:
		for img_id, bbox, in annotations.items():
			img_path = '/home/sagrawa2/EZ-CV/images/' + img_id.split('http://35.237.13.210:8080/img/')[1]
			f.write(img_path + ',' + ','.join(map(str, bbox)) + ',bird\n')
	# os.system('cat ../keras_frcnn/kitti_simple_label.txt')  
	os.system('python3 ../keras_frcnn/test_frcnn_kitti.py')
	return jsonify(annotations)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port)
	print('Server hosted at: ' + server_url)