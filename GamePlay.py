from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = "asuhdiaduf8oduiahsfkjewhRIOYUEWH"


class Player(db.Model, UserMixin):
    User_id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(40), unique=True, nullable=False)
    Table_id = db.relationship('Table', backref='player')
    Hand = db.Column(db.Integer)
    Dealer = db.Column(db.Integer)

class Table(db.Model):
    Table_id = db.Column(db.Integer)
    NumPlayers = db.Column(db.Integer)

class Dealer(db.Model):
    Deck_id = db.Column(db.Integer)
    Table_id = db.Column(db.Integer)

class Hand(db.Model):
    Player_id = db.Column(db.Integer)
    Table_id = db.Column(db.Integer)
    Card_id = db.Column(db.Integer)

class Deck(db.Model):
    Card_id = db.relationship('Card', backref='deck')

class Card(db.Model):
    value = db.Column(db.Integer)
    suit = db.Column(db.String)

class User(db.Model):
    Account_id = db.Column(db.Integer)
    Active = db.Column(db.Boolean)
    Account_Bal = db.Column(db.Integer)


login_manager = LoginManager(app)
login_manager.init_app(app)

