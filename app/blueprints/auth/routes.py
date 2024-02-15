from . import auth
from .forms import Login, Signup
from flask import request, render_template, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from app.models import User

@auth.route("/login", methods=["GET", "POST"])
def login():
    loginForm = Login()
    if loginForm.validate_on_submit() and request.method == "POST":
        email = loginForm.email.data
        password = loginForm.password.data
        user = User.query.filter(User.email == email).first()
        if user and check_password_hash(user.password, password):
            flash(f"Welcome Back {user.username}!", 'success')
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('Invalid username email or password...', 'danger')
            return render_template("login.html", loginForm=loginForm)
    else:
        return render_template("login.html", loginForm=loginForm)
    

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    signupForm = Signup()
    if signupForm.validate_on_submit() and request.method == "POST":
        username = signupForm.username.data
        email = signupForm.email.data
        password = signupForm.password.data
        new_user = User(username, email, password)
        new_user.save()
        flash("Success! Thank you for signing up!", 'success')
        return redirect(url_for('auth.login'))
    return render_template("signup.html", signupForm=signupForm)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Successfully Logged Out!", "success")
    return redirect(url_for('auth.login'))