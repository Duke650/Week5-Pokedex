import requests
from flask import Flask, request, render_template
from app import app
from .forms import SearchPokemon, Login, Signup



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

@app.route("/poke-info/<id>", methods=["GET","POST"])
def getPokeInfoById(id):
    form = SearchPokemon()
    if form.validate_on_submit() and request.method == "POST":
        name = request.form.get("name")
        info = fetchPokeInfo(name)
        defaultInfo = info[0]
        abilityInfo = info[1]
        return render_template("pokeSearch.html", form=form, defaultInfo=defaultInfo, abilityInfo=abilityInfo)
    return render_template("pokeSearch.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    loginForm = Login()
    if loginForm.validate_on_submit() and request.method == "POST":
        return render_template("login.html", loginForm=loginForm)
    return render_template("login.html", loginForm=loginForm)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    signupForm = Signup()
    if signupForm.validate_on_submit() and request.method == "POST":
        return render_template("signup.html", signupForm=signupForm)
    return render_template("signup.html", signupForm=signupForm)
