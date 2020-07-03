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
    column_searchable_list = ('title', 'year','category')
    can_export = True
    
    def is_accessible(self):
        return session['username'] == 'admin'
        