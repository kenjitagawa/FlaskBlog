from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from pyblog import db, login_manager, app
from flask_login import UserMixin

# Load user from db
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

"""
    This file contains all of the models for the database within the project. For now we have the User table and the Post table. 
"""

class User(db.Model, UserMixin):
    """
    The User model inherits from db.Model and the UserMixin. UserMixin handles the user session and several other complex concepts whereas the db.Model handles the databse management. 
    User takes in several arguments that can be found below:
    - id (auto-generated)
    - username (unique usernames, required)
    - email (unique email, required)
    - image_file (required, with a default image)
    - password (required)
    - posts ("one to many relation", alias = "author", lazy set to True (default -> "explicit is better than implicit"))
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    
    def get_reset_token(self, expires_seconds=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_seconds)
        return s.dumps({'user_id': self.id}).decode('utf8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try: 
            user_id = s.loads(token)['user_id']
        except:
            return None
        
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    """
    The Post model inherits from db.Model and the UserMixin. UserMixin handles the user session and several other complex concepts whereas the db.Model handles the databse management. 
    User takes in several arguments that can be found below:
    - id (auto-generated, primary-key)
    - title (required)
    - date_posted (required)
    - content (required)
    - user_id ("one to many relation", ForeignKey => "user.id")
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
