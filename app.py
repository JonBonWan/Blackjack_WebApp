from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, \
    login_user, logout_user, current_user, login_required, UserMixin

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'fidhos'
login_manager = LoginManager(app)
login_manager.init_app(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    Account_id = db.Column(db.Integer)
    Active = db.Column(db.Boolean)
    Account_Bal = db.Column(db.Float)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))


class Player(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(40), unique=True, nullable=False)
    Hand_id = db.relationship('Hand', backref='player')
    Table = db.Column(db.Integer, db.ForeignKey('table.id'))
    User = db.relationship('User', backref='player', uselist=False)
    Dealer_id = db.Column(db.Integer, db.ForeignKey('dealer.id'))


class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    NumPlayers = db.Column(db.Integer)
    Player_id = db.relationship('Player', backref='table')
    Dealer_id = db.relationship('Dealer', backref='table', uselist=False)


class Dealer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Table_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    Deck_id = db.relationship('Deck', backref='dealer')
    Player_id = db.relationship('Player', backref='dealer')


class Hand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    Card_id = db.relationship('Card', backref='hand')
    Card_total = db.Column(db.Integer)


class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Card_id = db.relationship('Card', backref='deck')
    Dealer_id = db.Column(db.Integer, db.ForeignKey('dealer.id'))


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'))
    hand_id = db.Column(db.Integer, db.ForeignKey('hand.id'))
    value = db.Column(db.Integer)
    suit = db.Column(db.String)


@login_manager.user_loader
def load_user(uid):
    user = User.query.get(uid)
    return user


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/account', methods=['GET', 'POST'])
def account():
    #if request.method == 'POST':
    #    n = request.form['name']
    #    h = request.form['height']
    #    t = request.form['town']
    #    mountain = Mountains(name=n, height=h, town=t, user=current_user)
    #    db.session.add(mountain)
    #    db.session.commit()
    #    return redirect('/Game')
    return render_template('Account.html')


@login_manager.user_loader
def load_user(uid):
    user = User.query.get(uid)
    return user


#@app.route('/update/<id>', methods=['GET', 'POST'])
#def update(id):
  #  mountain = Mountains.query.get(id)
 #   if request.method == 'POST':
 #       mountain.height = request.form['height']
 #       mountain.town = request.form['town']
 #       db.session.commit()
 #      return redirect('/userMoutains')
 #   return render_template('update.html', mountain=mountain)


#@app.route('/delete/<id>')
#def delete(id):
  #  mountain = Mountains.query.get(id)
  #  db.session.delete(mountain)
  #  db.session.commit()
   # return redirect('/userMoutains')


@app.route('/newUser', methods=['GET', 'POST'])
def newUser():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        n = request.form['name']
        user = User.query.filter_by(username=u).first()
        if user == None:
            newuser = User(username=u, password=p, name=n)
            db.session.add(newuser)
            db.session.commit()
            login_user(newuser)
            return redirect('/create')
        if user != None:
            return render_template('Login.html')
    return render_template('newUser.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user != None:
            if password == user.password:
                login_user(user)
                return redirect('/Game')
                #return 'SUCCESS'
        return render_template('Login.html', notuser='Username or password was incorrect.')
    return render_template('Login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('logout.html')


@app.route('/Game')
@login_required
def Game():
    #   mountains = Mountains.query.filter_by(user=current_user)
    return render_template('Game.html')


@app.errorhandler(404)
def err404(err):
    return render_template('404.html', err=err)


@app.errorhandler(401)
def err401(err):
    return render_template('401.html', err=err)


if __name__ == '__main__':
    app.run(debug=True)

