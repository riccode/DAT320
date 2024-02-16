from flask import Flask, render_template
app = Flask(__name__)


#very basic flask app. Render a single view (index.html). This will be a page showing the project dashboard
@app.route('/')
def hello():
	return render_template('index.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000, debug=True)