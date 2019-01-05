from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from hashutils import make_pw_hash, check_pw_hash

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://RSKiosk:ESkw73gANMJBlqXe@localhost:3306/RSKiosk"
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)
app.secret_key = "super_secret_key"

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    amount = db.Column(db.Integer)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, amount, owner):
        self.title = title
        self.amount = amount
        self.owner = owner
        
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(120))
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    Food = db.relationship('Food', backref='owner')

    def __init__(self, username, password, first_name, last_name):
        self.username = username
        self.password_hash = make_pw_hash(password)
        self.first_name = first_name
        self.last_name = last_name

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')
    
@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/login')
def login():
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()      
        if user and check_pw_hash(password, user.password_hash):                      
            session['username'] = username
            flash('Logged in')
            return redirect('/')
        else:
            flash('User password is incorrect, or user does not exist', 'error')
    
    return render_template('login.html', header='Login')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        existing_user = User.query.filter_by(username=username).first()

        if password != verify:
            flash('Password does not match', "error")
        elif len(username) < 3 or len(password) < 3:
            flash('Username and password must be more than 3 characters', 'error')
        elif len(first_name) < 1 or len(last_name) < 1:
            flash('please fill in the full name of the user')
        elif existing_user:
            flash('User already exists', 'error')
        else:
            new_user = User(username, password, first_name, last_name)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/')

    return render_template('signup.html', header='Signup')
if  __name__ == "__main__":
    app.run()