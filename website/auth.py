from flask import Blueprint, render_template, request, flash, url_for, redirect, session, logging
import psycopg2
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
from .security import encrypt_pwd, verify_pwd
from .models import User, Menu
from .utils import load_menu
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

# Register Form Class
class RegisterForm(Form):
    firstname = StringField('fa fa-user','First Name', [
        validators.DataRequired(),
        validators.Regexp('^[A-Za-z]+$',0,'First Name only allow Alphabet characters.'),
        validators.Length(min=1, max=50)])
    lastname = StringField('fa fa-user-alt','Last Name', [
        validators.DataRequired(),
        validators.Regexp('^[A-Za-z]+$',0,'Last Name only allow Alphabet characters.'),
        validators.Length(min=1, max=50),])
    username = StringField('fas fa-id-card-alt','Username', [
        validators.DataRequired(),
        validators.Length(min=6, max=25),
        validators.Regexp('^\w+$',0,'Username only allow Alpha Numeric & Underscore _ character')])
    email = StringField('fa fa-envelope','Email', [
        validators.Email()])
    password = PasswordField('fa fa-lock','Password', [
        validators.DataRequired(),
        validators.StrongPassword()
    ])
    confirm = PasswordField('fa fa-lock','Confirm Password',[
        validators.EqualTo('password', message='Passwords do not match')
    ])
    usergroup = SelectField('fa fa-users','User Group', choices=[('ADMIN', 'Admin'), ('SUPP', 'Supplier'), ('CUST', 'Customer')])

@auth.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        username = form.username.data
        password = encrypt_pwd(str(form.password.data))
        usergroup = form.usergroup.data

        cek_user = User.query.filter_by(username=username).first()
        cek_email = User.query.filter_by(email=email).first()
        
        if cek_user:
            flash('Username already exists.','danger')
        elif cek_email:
            flash('Email already exists.','danger')
        else:        
            new_user = User(first_name=firstname, last_name=lastname, email=email.lower(), username=username.lower(), password=password, user_group=usergroup)
            db.session.add(new_user)
            db.session.commit()
            
            flash('Registration Finished. <br/> Please wait for Web Admin to Approve your registration.', 'success')
            return redirect(url_for('auth.login'))
        
    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        is_password_passed = 0;
        is_status_passed = 0;
        user = User.query.filter_by(username=username).first()
        if user:
            if verify_pwd(password, user.password):
                is_password_passed = 1
            else:
                is_password_passed = 0
                flash('Incorrect Username/Password','danger')
                
            if user.status_id == 4:
                is_status_passed = 1
            else:
                is_status_passed = 0
                flash('User not allowed to Login !<br/>Please contact our administrator.','danger');
        else:
            flash('Incorrect Username/Password.','danger')
            
        if (is_password_passed and is_status_passed):
            login_user(user)
            menus = load_menu(user.user_group)
            return render_template('home.html',user=current_user, menus=menus)
    else:
        if current_user.is_authenticated:
            return redirect(url_for('views.home'))
    
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
