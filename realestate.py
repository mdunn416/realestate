from app import app, db

#The following code is added to that if we use flask shell, we do not need to import a db,user,post - you also need to import db above
from app.models import User, Post, Listing

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Listing':Listing}


