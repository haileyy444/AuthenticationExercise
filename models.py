"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users" 

    username = db.Column(db.String(20), nullable=False, unique=True, primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedback = db.relationship("Feedback", backref="user", cascade="all,delete")

    @classmethod
    def registar(info, username, password, email, first_name, last_name):
        hash = bcrypt.generate_password_hash(password)
        encrypted = hash.decode("utf8")
        user = info(
            username=username,
            password=encrypted,
            email=email,
            first_name=first_name,
            last_name=last_name)
        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(info, username, password):
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False
 
class Feedback(db.Model):
    __tablename__ = "feedback"

    id=db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('users.username'), nullable=False)
   
def connect_db(app): 
    db.app = app
    db.init_app(app)


    