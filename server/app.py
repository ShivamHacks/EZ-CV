from flask import Flask

app = Flask(__name__, static_url_path='/EZ-CV/client')

@app.route('/')
def hello_world():
	return send_from_directory('../client/', 'index.html')

@app.route('/train_model')
def train_model(img_urls, annotations):
	print(img_urls)
	print(annotations)
	return 'all good'

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)
	print('Server hosted at: 35.237.13.210:8080')