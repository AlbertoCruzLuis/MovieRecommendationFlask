from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask import session
from .config import DevelopmentConfig as DC
import os

class CustomView(ModelView):
    def is_accessible(self):
        return session['username'] == 'admin'

class CustomAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return session['username'] == 'admin'

class CustomFileAdmin(FileAdmin):
    def is_accessible(self):
        return session['username'] == 'admin'

class FilmView(CustomView):
    list_image = [(img,img) for img in (os.listdir(DC.UPLOAD_FOLDER))]
    form_choices = {
            'image_name': list_image
    }
    column_searchable_list = ('title', 'year','category')
    can_export = True
    
    def is_accessible(self):
        return session['username'] == 'admin'
        