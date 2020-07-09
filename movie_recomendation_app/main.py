from flask import Flask
from flask import Blueprint, render_template, redirect, url_for, flash
from flask import request, session

from sqlalchemy.sql import text
import random
import numpy as np
import os
import re

from .models import db, User, Film, Rating
from .recomendation_model import recommended_model
from .config import DevelopmentConfig

main = Blueprint('main', __name__)

@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.before_request
def before_request():
    if 'username' not in session and request.endpoint in ['home']:
        return redirect(url_for('.login'))
    elif 'username' in session and request.endpoint in ['login', 'signup']:
        return redirect(url_for('.home'))
            
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login', methods= ['GET','POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username = username).first()
        session['current_user_id'] = user.id
        if user is not None and user.verify_password(password):
            return redirect(url_for('.home'))
        else:
            flash('Wrong Password','danger')
    return render_template('login.html')

@main.route('/logout')
def logout():
    if 'username' in session:
        session.clear()
    return redirect(url_for('.index'))

@main.route('/signup', methods= ['GET','POST'])
def signup():
    if request.method == 'POST':
        if request.form['password'] != request.form['confirm_password']:
            flash('Different password','danger')
        else:
            user = User(request.form['username'],
                        request.form['password'])
            db_user = User.query.filter_by(username = user.username).first()
            if db_user is None:
                db.session.add(user)
                db.session.commit()
                flash('Successful user','success')
                return redirect(url_for('.login'))
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

def get_film_data(all_film, list_name_film):
    aux_all_film = all_film[:]
    selected_films = []
    for i in range(4):
        if len(aux_all_film) > 0:
            for film in aux_all_film:
                if list_name_film[i] == film['title']:
                    selected_films.append(film)
                    aux_all_film.remove(film)
    return selected_films

def search_film(all_film):
    find_film = []
    for film in all_film:
        if re.search((request.form['search']).lower(),(film['title']).lower()):
            find_film.append(film)

    if len(find_film) == 0:
        flash('Not Found','warning')
    return find_film


@main.route('/home', methods= ['GET','POST'])
@main.route('/home/<section>', methods= ['GET','POST'])
def home(section = None):
    # Query Database
    current_user_id = session['current_user_id']
    category = list(db.engine.execute('select category from film'))
    film_data = list(db.engine.execute(
        text("select f.*, coalesce((select rating from ratings where user_id = :current_user_id and film_id = f.id),0) as rating from film as f where category = :section"),
        section = section, current_user_id = current_user_id))
    all_film = list(db.engine.execute("select * from film"))
    rating_film = list(db.engine.execute(
        text("select f.*, coalesce((select rating from ratings where user_id = :current_user_id and film_id = f.id),0) as rating from film as f"),
        current_user_id = current_user_id))
    recommended_film = random_film(all_film)
    action_lover = []
    for film in rating_film:
        if film[5] > 0:
            action_lover.append((film[1],film[5]))
    #recommended_film = recommended_model(action_lover)
    if len(recommended_model(action_lover)) >= 4:
        recommended_film = get_film_data(all_film,recommended_model(action_lover))
    else:
        recommended_film = random_film(all_film)

    #Search Film
    find_film = []
    if request.method == 'POST':
        find_film = search_film(all_film)

    if section != 'search':
        if section != None and section not in np.unique(category):
            return redirect(url_for('home'))

    return render_template('home.html', category_name = section,
                            list_category = np.unique(category),
                            film_data = film_data,
                            recommended_film = recommended_film,
                            find_film = find_film,
                            rating_film=rating_film)

@main.route('/home/rating', methods= ['POST'])
def change_rating():
    current_user_id = session['current_user_id']
    new_rating = request.form['rating']
    name_rating = request.form['name_rating']
    rating = Rating(name_rating,current_user_id,new_rating)
    db_rating = Rating.query.filter_by(
        film_id = rating.film_id).filter_by(
        user_id = rating.user_id).first()

    if db_rating is not None:
        db_rating.rating = new_rating
    else:
        db.session.add(rating)
    db.session.commit()

    response = {'status':200, 'rating':new_rating,'name_rating':name_rating}
    return response