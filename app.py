from flask import Flask,render_template,request,url_for,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
import os
from flask_login import LoginManager, UserMixin, login_user



app=Flask(__name__)

db_path = os.path.abspath(os.path.dirname(__file__)) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(os.path.join(db_path, 'database.db'))

app.config['SECRET_KEY'] = 'thisissecretkey'
db=SQLAlchemy(app)

bcrypt=Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(30),nullable=False,unique=True)
    password=db.Column(db.String(30),nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def run():
    return render_template('Login_Page.html')



@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('pass')
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return render_template('dashboard.html', email=email, password=password)
        else:
            flash('Login failed. Please check your credentials.', 'danger')
    return render_template('Login_Page.html')


@app.route('/sign_up',methods=['POST','GET'])
def sign_up():
    
    if request.method=='POST':

        email=request.form.get('email')
        password=request.form.get('pass')

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already exists. Please use a different email.", "danger")
            return redirect(url_for('sign_up'))

        hashed_password=bcrypt.generate_password_hash(password).decode('utf-8')
        new_user=User(email=email,password=hashed_password)

        db.session.add(new_user)
        db.session.commit()
        flash("Your account has been created. You can now log in.", "success")
        return redirect(url_for('login'))



        
@app.route('/Sign_up_page',methods=['POST','GET'])
def sign_up_page():
    return render_template('Sign_up.html')

@app.route('/Login_page',methods=['POST','GET'])
def login_page():
    return render_template('Login_Page.html')


if __name__=='__main__':
    with app.app_context():
        db.create_all()
        print("Database Created")
    app.run(debug=True)

