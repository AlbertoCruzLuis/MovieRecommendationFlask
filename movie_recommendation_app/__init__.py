from flask import Flask 
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os

from .commands import create_tables, create_super_user
from .config import DevelopmentConfig
from .views import CustomAdminIndexView, CustomFileAdmin, FilmView, CustomView
from .models import db, User, Film, Rating
from .main import main

def create_app():
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(DevelopmentConfig)

    admin = Admin(app, index_view= CustomAdminIndexView())
    admin.add_view(CustomView(Rating, db.session))
    admin.add_view(CustomView(User, db.session))
    admin.add_view(FilmView(Film, db.session))

    path = os.path.join(os.path.dirname(__file__), 'static/img/film')
    fileadmin = CustomFileAdmin(path, name='Films Image')
    fileadmin.allowed_extensions = DevelopmentConfig.ALLOWED_EXTENSIONS
    admin.add_view(fileadmin)

    db.init_app(app)

    app.register_blueprint(main)

    app.cli.add_command(create_tables)
    app.cli.add_command(create_super_user)

    return app