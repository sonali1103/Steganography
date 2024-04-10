from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import hashlib
import os
from . import dbconn
auth = Blueprint('auth', __name__)



@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # validate user inputs
        msg = validateSignin(email,password)
        if(msg != 'valid'):
            flash(msg,category='error')
            return render_template("login.html")
        
        
        user_data = dbconn.get_user(email,password)
        if user_data != False:
            session['logged_in'] = True
            return redirect(url_for('home.homeview'))
        else:
            flash('Please enter valid credentials', category='error')
            return render_template("login.html")
        
    return render_template("login.html")   


@auth.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('firstName')
        password = request.form.get('password')
        
        # validate user inputs
        msg = validateRegister(name, email,password)
        if(msg != 'valid'):
            flash(msg,category='error')
            return render_template("signup.html")
        
        
        # check if user exists
        user_exsits = dbconn.check_user(email)
        if(user_exsits):
            flash('User already registered!', category='error')
            return render_template("signup.html")
        
        # save to db and login
        user_data = dbconn.save_user(name,email,password) 
        if(user_data): 
            flash('Account created!', category='success')
            session['logged_in'] = True
            return redirect(url_for('home.homeview')) 
        else:
            flash('Could not create, Try again!', category='error')
            return render_template("signup.html")
        
    return render_template("signup.html")  






# validate user inputs during signin
def validateSignin(email, password):
    if len(email) < 1:  
        return 'Please enter email'
        
    if len(password) < 1:
        return 'Please enter password'
           
    return 'valid'

# validate user inputs during register
def validateRegister(name, email, password):
    if len(email) < 1:
        return 'Please enter email'
    if len(name) < 3:
        return 'Please enter valid name'
    if len(password) < 4:
        return 'Please enter password with min length 4'
    return 'valid'


# generate hash for saving password
def hash_password(password, salt = None):
    if salt is None:
        # Generate a random salt if not provided
        salt = os.urandom(16)  # 16 bytes = 128 bits
    else:
        # Ensure the salt is in bytes
        salt = bytes.fromhex(salt)
      
    # Combine the password and salt
    salted_password = password.encode() + salt
    
    # Hash the salted password using SHA-256
    hashed_password = hashlib.sha256(salted_password).hexdigest()
    
    # Return the hashed password and salt
    return hashed_password, salt.hex()