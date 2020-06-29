from flask import Flask
from flask import render_template

from config import DevelopmentConfig

app = Flask(__name__, static_url_path='/static')
app.config.from_object(DevelopmentConfig)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(port = 8000)