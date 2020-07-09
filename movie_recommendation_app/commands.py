import click
from flask.cli import with_appcontext

from .models import User, db

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()

@click.command(name='create_super_user')
@with_appcontext
def create_super_user():
    user = User('admin','admin')
    db_user = User.query.filter_by(username = user.username).first()
    if db_user is None:
        db.session.add(user)
        db.session.commit()