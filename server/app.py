from flask import Flask, send_from_directory

app = Flask(__name__, static_url_path='/EZ-CV/client')

# Static Files
@app.route('/')
def index(): return send_from_directory('../client/', 'index.html')
@app.route('/style.css')
def style(): return send_from_directory('../client/', 'style.css')

# Train the model
@app.route('/train_model')
def train_model(img_urls, annotations):
	print(img_urls)
	print(annotations)
	return 'all good'

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)
	print('Server hosted at: 35.237.13.210:8080')