from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


#Mixin provides generic login functions that we can reuse (is_authenticated etc.)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    admin_flag = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, pword):
        self.password_hash = generate_password_hash(pword)
    
    def check_password(self, pword):
        return check_password_hash(self.password_hash, pword)
    
    def check_admin(self):
        if self.admin_flag:
            return True
        return False

class Post(db.Model): #This will be my search result storage eventually
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #this is the many side of a relationship and is not really going to be shown

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(140))
    address = db.Column(db.String, unique=True, index=True)
    price = db.Column(db.Integer, index=True)
    zipcode =  db.Column(db.Integer, index=True)
    building_sqft = db.Column(db.Integer, index=True)
    lot_sqft = db.Column(db.Integer, index=True)
    year = db.Column(db.Integer, index=True)
    has_pool = db.Column(db.Boolean, unique=False, default=False)

    def __repr__(self):
        return '<Listing {}>'.format(self.address)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
