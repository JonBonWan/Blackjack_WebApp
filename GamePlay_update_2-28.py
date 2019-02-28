from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = "asuhdiaduf8oduiahsfkjewhRIOYUEWH"

class Player(db.Model, UserMixin):
    id = db.Column(db.Integer)
    Name = db.Column(db.String(40), unique=True, nullable=False)
    Table_id = db.Column(db.Integer, db.ForeignKey('Table.Table'))
    Hand_id = db.Column(db.Integer)
    Table = db.relationship('Table', backref='Player')
    User = db.relationship('User', backref='Player', uselist=False)

class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    NumPlayers = db.Column(db.Integer)
    Table = db.relationship('Player', backref='table')
    Players = db.Column(db.Integer, db.ForeignKey('Player.id'))
    Dealer_id = db.relationship('Dealer', backref='Table', uselist=False)

class Dealer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Table_id = db.Column(db.Integer)
    Deck_id = db.relationship('Deck', backref='Dealer')
    Players = db.relationship('Player', backref='Dealer')


class Hand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Player_id = db.Column(db.Integer, db.ForeignKey('Player.id'))
    Card_id = db.Column(db.Integer, db.ForeignKey('Card.id'))
    Card_total = db.Column(db.Integer)

class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Card_id = db.relationship('Card', backref='deck')
    Dealer_id = db.Column(db.Integer, db.ForeignKey('Dealer.id'))

class Card(db.Model):
    id = db.Column(db.Integer)
    Deck_id = db.Column(db.Integer, db.ForeignKey('Deck.id'))
    value = db.Column(db.Integer)
    suit = db.Column(db.String)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Account_id = db.Column(db.Integer)
    Active = db.Column(db.Boolean)
    Account_Bal = db.Column(db.Integer)
    Player_id = db.Column(db.Integer, db.ForeignKey('Player.id'))


login_manager = LoginManager(app)
login_manager.init_app(app)
