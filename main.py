from flask import Flask
from flask import render_template, redirect, url_for
from flask import request, session

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import forms
from models import db
from models import User

from config import DevelopmentConfig

app = Flask(__name__, static_url_path='/static')
app.config.from_object(DevelopmentConfig)

admin = Admin(app)
#admin.add_view(ModelView(User, db.session))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.before_request
def before_request():
    if 'username' not in session and request.endpoint in ['home']:
        return redirect(url_for('login'))
    elif 'username' in session and request.endpoint in ['login', 'signup']:
        return redirect(url_for('home'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods= ['GET','POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username = username).first()
        if user is not None and user.verify_password(password):
            return redirect(url_for('home'))
        else:
            print('Error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('index'))

@app.route('/signup', methods= ['GET','POST'])
def signup():
    if request.method == 'POST':
        user = User(request.form['username'],
                    request.form['password'])
        db_user = User.query.filter_by(username = user.username).first()
        if db_user is None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            print('Error')
    return render_template('signup.html')


@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.run(port = 8000)