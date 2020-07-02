from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask import session
import os

class CustomAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return session['username'] == 'admin'

class CustomFileAdmin(FileAdmin):
    def is_accessible(self):
        return session['username'] == 'admin'

class FilmView(ModelView):
    form_choices = {
                 'image_name': [ (img,img) for img in (os.listdir('static/img/film'))
                ]
           }
    def is_accessible(self):
        return session['username'] == 'admin'