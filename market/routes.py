from market import app
from flask import render_template,redirect,url_for,flash, get_flashed_messages
from market.models import Item,User
from market.forms import RegisterForm, LoginForm
from market import db
from flask_login import login_user,logout_user,login_required
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/market')
@login_required
def market():
    items = Item.query.all()
    return render_template('market.html',items=items)

@app.route('/register',methods=['POST','GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create=User(username=form.username.data,
                    email=form.email.data, password1 = form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created Successfully! You are logged in as: {user_to_create.username}',category="success")       
    
        return redirect(url_for('market'))

    if form.errors != {}:
        for e in form.errors.values():
            flash(f'Error Occured: {e[0]}',category='danger')
    
    return render_template('register.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}',category="success")
            return redirect(url_for('market'))
        else:
            flash('Invalid Credentials',category='danger')

     
    return render_template('login.html',form=form)

@app.route('/logout')
def logout_page():

    logout_user()
    flash("You have been logged out!",category='info')
    return redirect(url_for("home"))


   