from flask import Flask
from flask import render_template, redirect, url_for, flash
from flask import request, session

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from views import CustomAdminIndexView, CustomFileAdmin, FilmView
import forms
from models import db
import numpy as np
from models import User, Film
from sqlalchemy.sql import text
import random

from config import DevelopmentConfig
import os
import re

app = Flask(__name__, static_url_path='/static')
app.config.from_object(DevelopmentConfig)

admin = Admin(app, index_view= CustomAdminIndexView())
#admin.add_view(ModelView(User, db.session))
# admin.add_view(ModelView(Film, db.session))
admin.add_view(FilmView(Film, db.session))

path = os.path.join(os.path.dirname(__file__), 'static/img/film')
fileadmin = CustomFileAdmin(path, name='Films Image')
fileadmin.allowed_extensions = DevelopmentConfig.ALLOWED_EXTENSIONS
admin.add_view(fileadmin)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.before_request
def before_request():
    if 'username' not in session and request.endpoint in ['home']:
        return redirect(url_for('login'))
    elif 'username' in session and request.endpoint in ['login', 'signup']:
        return redirect(url_for('home'))

def create_super_user():
    user = User('admin','admin')
    db_user = User.query.filter_by(username = user.username).first()
    if db_user is None:
        db.session.add(user)
        db.session.commit()
            
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
            flash('Wrong Password','danger')
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
            flash('Successful user','success')
            return redirect(url_for('login'))
        else:
            flash('User already exists','warning')
    return render_template('signup.html')

    
def random_film(all_film):
    aux_all_film = all_film[:]
    selected_films = []
    for _ in range(4):
        if len(aux_all_film) > 0:
            random_film = random.choice(aux_all_film)
            selected_films.append(random_film)
            aux_all_film.remove(random_film)
    return selected_films

def search_film(all_film):
    find_film = []
    for film in all_film:
        if re.search((request.form['search']).lower(),(film['title']).lower()):
            find_film.append(film)
            print(film)

    if len(find_film) == 0:
        flash('Not Found','warning')
    return find_film

@app.route('/home', methods= ['GET','POST'])
@app.route('/home/<section>', methods= ['GET','POST'])
def home(section = None):
    # Query Database
    category = list(db.engine.execute('select category from films'))
    film_data = list(db.engine.execute(text("select * from films where category = :section"), section = section))
    all_film = list(db.engine.execute("select * from films"))

    recommended_film = random_film(all_film)
    if section != None and section not in np.unique(category):
        return redirect(url_for('home'))

    #Search Film
    find_film = []
    if request.method == 'POST':
        find_film = search_film(all_film)


    return render_template('home.html', category_name = section,
                            list_category = np.unique(category),
                            film_data = film_data,
                            recommended_film = recommended_film,
                            find_film = find_film)


if __name__ == '__main__':
    db.init_app(app)

    with app.app_context():
        db.create_all()
        create_super_user()

    app.run(port = 8000)