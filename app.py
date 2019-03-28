import random
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


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    bet = db.Column(db.Integer)
    balance = db.Column(db.Integer, nullable=True)
    active = db.Column(db.Boolean)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(40), unique=True, nullable=False)
    Hand_id = db.relationship('Hand', backref='player')
    Table_id = db.Column(db.Integer, db.ForeignKey('table.id'))
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
    cards = db.relationship('Card', backref='deck', lazy='dynamic')
    Dealer_id = db.Column(db.Integer, db.ForeignKey('dealer.id'))


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'))
    hand_id = db.Column(db.Integer, db.ForeignKey('hand.id'))
    face = db.Column(db.String)
    value = db.Column(db.Integer)
    suit = db.Column(db.String)


def loadDeck():
    faces = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    suits = ['H', 'S', 'D', 'C']
    deck = Deck()
    db.session.add(deck)
    for i in range(52):
        j = i % 4
        suit = suits[j]
        k = i % 13
        face = faces[k]
        if face == 'A':
            value = 11
        elif face == '2':
            value = 2
        elif face == '3':
            value = 3
        elif face == '4':
            value = 4
        elif face == '5':
            value = 5
        elif face == '6':
            value = 6
        elif face == '7':
            value = 7
        elif face == '8':
            value = 8
        elif face == '9':
            value = 9
        elif face == '10':
            value = 10
        elif face == 'J':
            value = 10
        elif face == 'Q':
            value = 10
        elif face == 'K':
            value = 10

        card = Card(face=face, suit=suit, value=value, deck=deck)
        db.session.add(card)

    db.session.commit()


def logOutTable():
    key = current_user.player_id
    pl = Player.query.filter_by(id=key).first()
    if pl.Table_id is not None:
        key2 = pl.Table_id
        tb = Table.query.filter_by(id=key2).first()
        pl.Table_id = None
        tb.NumPlayers = tb.NumPlayers - 1
        db.session.commit()
        print("logged out of table")


@login_manager.user_loader
def load_user(uid):
    user = User.query.get(uid)
    return user


@app.route('/')
def home():
    if not current_user.is_anonymous:
        logOutTable()
    return render_template('home.html')


@login_manager.user_loader
def load_user(uid):
    user = User.query.get(uid)
    return user


@app.route('/newUser', methods=['GET', 'POST'])
def newUser():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        balance = int(request.form["balance"])
        active = True
        user = User(username=username, password=password, balance=balance, active=active)
        player = Player(Name=username, User=user)
        db.session.add(user)
        db.session.add(player)
        db.session.commit()
        login_user(user)
        return redirect('/account')
    return render_template('newUser.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user is None:
            return render_template('Login.html')
        else:
            user.active=True
            db.session.commit()
            login_user(user)
            return redirect('/account')
    return render_template('Login.html')


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    logOutTable()
    key = current_user
    profile = Player.query.filter_by(User=key).all()
    return render_template('account.html', profile=profile, key=key, player=Player)


@app.route('/logout')
@login_required
def logout():
    logOutTable()
    logout_user()
    return render_template('logout.html')


@app.route('/Game')
@login_required
def Game():
    lst = User.query.all()
    loadDeck()
    key = current_user.player_id
    pl = Player.query.filter_by(id=key).first()
    if pl.Table_id is None:
        tb = Table.query.filter(Table.NumPlayers != 5).all()
        if tb:
            tb = tb[0]
            tb.NumPlayers = tb.NumPlayers + 1
            pl.Table_id = tb.id
            db.session.commit()
            dealer = Dealer.query.filter_by(Table_id=tb.id).first()
            player = Player.query.filter_by(Dealer_id=dealer.id).first()
            print(player)
            return render_template('Game.html', lst=lst, dealer=player)

        tabl = Table(NumPlayers=1)
        db.session.add(tabl)
        db.session.commit()
        dealer = Dealer(Table_id=tabl.id)
        db.session.add(dealer)
        pl.Table_id = tabl.id
        db.session.commit()
        dpl = Player(Name="Dealer", Table_id=tabl.id, Dealer_id=dealer.id)
        db.session.add(dpl)
        db.session.commit()
    tb = Table.query.filter_by(id=pl.Table_id).first()
    dealer = Dealer.query.filter_by(Table_id=tb.id).first()
    dpl = Player.query.filter_by(Dealer_id=dealer.id).first()
    print(dpl)
    return render_template('Game.html', lst=lst, dealer=dpl)


@app.route('/startingHand/<key>', methods=['GET', 'POST'])
@login_required
def startingHand(key):
    pl = Player.query.filter_by(id=key).first()
    hand = Hand(Player_id=pl.id)
    db.session.add(hand)
    db.session.commit()
    cards = Card.query.filter_by(hand_id=None).all()
    first = random.choice(cards)
    first.hand_id = hand.id
    db.session.commit()
    cards = Card.query.filter_by(hand_id=None).all()
    second = random.choice(cards)
    second.hand_id = hand.id
    hand.Card_total = first.value + second.value
    db.session.commit()
    # placeBet()
    return first.face+''+first.suit+'         '+second.face+''+second.suit


@app.route('/getCard', methods=['GET', 'POST'])
@login_required
def getCard():
    cards = Card.query.filter_by(hand_id=None).all()
    card = random.choice(cards)
    card.hand_id = current_user.id
    db.session.commit()

    return card.face+''+card.suit


@app.errorhandler(404)
def err404(err):
    return render_template('404.html', err=err)


@app.errorhandler(401)
def err401(err):
    return render_template('401.html', err=err)


if __name__ == '__main__':
    app.run(debug=True)
