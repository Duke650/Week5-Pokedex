import requests
from flask import request, render_template, redirect, url_for, flash
from app import app
from .forms import SearchPokemon, Login, Signup
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user



def fetchPokeInfo(pokeName):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokeName}"
    response = requests.get(url)
    if response.ok:
        data = response.json()
        abilityUrl = data['abilities'][0]['ability']['url']
        abilityResponse = requests.get(abilityUrl)
        abilityData = abilityResponse.json()
        
        return [data, abilityData]
    else:
        return None, "Oops! Seems this Pokemon is not in your Pokedex. Please try again..."

def fetchIdOfPokemon(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    response = requests.get(url)
    if response.ok:
        data = response.json()
        id = data['id']
        print("id =>", id)
        return id
    
    # ---- ROUTES -----
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/poke-info", methods=["GET","POST"])
def getPokeInfo():
    form = SearchPokemon()
    if form.validate_on_submit() and request.method == "POST":
        name = request.form.get("name")
        info = fetchPokeInfo(name)
        defaultInfo = info[0]
        abilityInfo = info[1]
        return render_template("pokeSearch.html", form=form, defaultInfo=defaultInfo, abilityInfo=abilityInfo)
    return render_template("pokeSearch.html", form=form)

@app.route("/poke-info/<id>/<direction>", methods=["GET","POST"])
def getPokeInfoById(id, direction):
    print("-----METHOD-----", request.method)
    newDirection = 1 if direction == 'next' else -1 
    form = SearchPokemon()
    # if form.validate_on_submit() and request.method == "POST":
    #name = request.form.get("name")
    info = fetchPokeInfo(str(int(id) + newDirection))
    print("INFO =>", info)
    defaultInfo = info[0]
    abilityInfo = info[1]
    return render_template("pokeSearch.html", form=form, defaultInfo=defaultInfo, abilityInfo=abilityInfo)
    # return render_template("pokeSearch.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    loginForm = Login()
    if loginForm.validate_on_submit() and request.method == "POST":
        email = loginForm.email.data
        password = loginForm.password.data
        user = User.query.filter(User.email == email).first()
        if user and check_password_hash(user.password, password):
            flash(f"Welcome Back {user.username}!", 'info')
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username email or password...', 'warning')
            return render_template("login.html", loginForm=loginForm)
    else:
        return render_template("login.html", loginForm=loginForm)
    

@app.route("/signup", methods=["GET", "POST"])
def signup():
    signupForm = Signup()
    if signupForm.validate_on_submit() and request.method == "POST":
        username = signupForm.username.data
        email = signupForm.email.data
        password = signupForm.password.data
        new_user = User(username, email, password)
        new_user.save()
        flash("Success! Thank you for signing up!", 'success')
        return redirect(url_for('login'))
    return render_template("signup.html", signupForm=signupForm)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))
