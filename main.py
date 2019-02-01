from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from hashutils import make_pw_hash, check_pw_hash
import datetime

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://RSKiosk:ESkw73gANMJBlqXe@localhost:3306/RSKiosk"
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)
app.secret_key = "super_secret_key"

#------start of databases------
class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(120))
    title = db.Column(db.String(120))
    amount = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    price = db.Column(db.Integer)

    def __init__(self, category, title, amount, cost, price):
        self.category = category
        self.title = title
        self.amount = amount
        self.cost = cost
        self.price = price
        
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(120))
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    user_level = db.Column(db.Integer)

    def __init__(self, username, password, first_name, last_name, user_level):
        self.username = username
        self.password_hash = make_pw_hash(password)
        self.first_name = first_name
        self.last_name = last_name
        self.user_level = user_level

#------end of databases------

#------start of account information gathering(login/logout, signup, index)------
@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')
    
@app.route('/')
def index():
    time= datetime.datetime.now().strftime("%I:%M%p | %B %d, %Y")
    return render_template("index.html", header='HOME', time=time)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    time= datetime.datetime.now().strftime("%I:%M%p | %B %d, %Y")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        user_level = request.form['user_level']

        existing_user = User.query.filter_by(username=username).first()

        if password != verify:
            flash('Password does not match', "error")
        elif len(username) < 3 or len(password) < 3:
            flash('Username and password must be more than 3 characters', 'error')
        elif len(first_name) < 1 or len(last_name) < 1:
            flash('please fill in the full name of the user', 'error')
        elif existing_user:
            flash('User already exists', 'error')
        elif user_level > 0 or user_level < 1:
            flash('User level must be 0 (server/cashier) or 1 (manager)', 'error')
        else:
            new_user = User(username, password, first_name, last_name, user_level)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/user_session')

    return render_template('signup.html', header='SIGNUP', time=time)
    
@app.route('/login', methods=['POST', 'GET'])
def login():
    time= datetime.datetime.now().strftime("%I:%M%p | %B %d, %Y")
    if 'username' in session:
        del session['username']
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()      
        if user and check_pw_hash(password, user.password_hash):                      
            session['username'] = username
            flash('Logged in')
            return redirect('/user_session')
        else:
            flash('User password is incorrect, or user does not exist', 'error')
    
    return render_template('login.html', header='LOGIN', time=time)

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

#------end of account information gathering------

#------start of flow stream for user functions------
@app.route('/user_session', methods=['POST','GET'])
def user_session():
    time= datetime.datetime.now().strftime("%I:%M%p | %B %d, %Y")
    if request.method == 'POST':
        button = request.form['submit_button']
        if button == 'create order': #TODO create HTML and function in main
            flash('Under construction', 'error')
            #return redirect('/create_order')

        if button == 'check tips': #TODO create HTML and function in main
            flash('Under construction', 'error')
            #return redirect('/check_tips')

        if button == 'open tables': #TODO create HTML and function in main
            flash('Under construction', 'error')

        if button == 'pay bill': #TODO create HTML and function in main
            flash('Under construction', 'error')
            #return redirect('/pay_bill')

        if button == 'clock in/out': #TODO create timesheet function
            flash('Under construction', 'error')
            #return redirect('/clock_in_clock_out')

        if button == 'check sales': #TODO create HTML and function in main
            flash('Under construction', 'error')
            #return redirect('/check_sales')

        if button == 'inventory':
            return redirect('/inventory')
        
    return render_template('session.html', header='NEW SESSION', user = session['username'], time=time)
#------end of flow stream for user functions------

#------Functions for users to perform------#
@app.route('/clock_in_clock_out', methods=['POST','GET'])
def clock_in_clock_out():
    return render_template('clock_in_clock_out.html')

@app.route('/create_order', methods=['POST', 'GET'])
def create_order():
    time= datetime.datetime.now().strftime("%I:%M%p | %B %d, %Y")
    return render_template('create_order.html', header='Create an Order', user = session['username'], time=time)

@app.route('/check_tips', methods=['POST', 'GET'])
def check_tips():
    time= datetime.datetime.now().strftime("%I:%M%p | %B %d, %Y")
    return render_template('check_tips.html', header='Check Tips', user = session['username'], time=time)

@app.route('/open_tables', methods=['POST', 'GET'])
def open_tables():
    time= datetime.datetime.now().strftime("%I:%M%p | %B %d, %Y")
    return render_template('open_tables.html', header='Open Tables', user = session['username'], time=time)

@app.route('/pay_bill', methods=['POST', 'GET'])
def pay_bill():
    time= datetime.datetime.now().strftime("%I:%M%p | %B %d, %Y")
    return render_template('pay_bill.html', header='Pay Open Bill', user = session['username'], time=time)

@app.route('/check_sales', methods=['POST', 'GET'])
def check_sales():
    time= datetime.datetime.now().strftime("%I:%M%p | %B %d, %Y")
    return render_template('check_sales.html', header='Check Sales from Today', user = session['username'], time=time)


# START OF INVENTORY
@app.route('/inventory',methods=['POST','GET'])
def inventory():
    time= datetime.datetime.now().strftime("%I:%M%p | %B %d, %Y")
    items = Food.query.all()

    if request.method == 'POST':
        button = request.form["submit_button"]
        
        if button == "Go Back to Session":
            return redirect("/user_session")

        if button == "Submit":
            category = request.form['category']
            title = request.form['title']
            amount = request.form['amount']
            cost = request.form['cost']
            price = request.form['price']
            if len(title) <1:
                flash('You must enter the name of the food item', 'error')
            elif cost == '' or price == '' or amount == '':
                flash('Cost of item, price of item, and amount of orders available must be entered between 0.01 and 999.99','error')
            else:
                cost = float(cost)
                price = float(price)
                amount = int(amount)

                if cost < 0.01 or cost > 999.99:
                    flash('Cost of item must be between $0.01 and $999.99','error')
                elif price < 0.01 or price > 999.99:
                    flash('Price of item must be between $0.01 and $999.99', 'error')
                elif amount < 1 or price > 999:
                    flash('Amount of item must be between 1 and 999', 'error')
                else:
                    new_Food = Food(category, title, amount, cost, price)
                    db.session.add(new_Food)
                    db.session.commit()
                    flash('Item has been added to the inventory system', 'error')
                    return redirect('/inventory')
    return render_template('inventory.html',header='INVENTORY' , user = session['username'], items=items, time=time)
# END OF INVENTORY
#------End of functions for users to perform------#


if  __name__ == "__main__":
    app.run()