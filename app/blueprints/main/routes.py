from . import main
import requests
from flask import render_template, request
from .forms import SearchPokemon



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
@main.route("/")
def home():
    return render_template("home.html")

@main.route("/poke-info", methods=["GET","POST"])
def getPokeInfo():
    form = SearchPokemon()
    if form.validate_on_submit() and request.method == "POST":
        name = request.form.get("name")
        info = fetchPokeInfo(name)
        defaultInfo = info[0]
        abilityInfo = info[1]
        print("INFO =>", info)
        return render_template("pokeSearch.html", form=form, defaultInfo=defaultInfo, abilityInfo=abilityInfo)
    return render_template("pokeSearch.html", form=form)

@main.route("/poke-info/<id>/<direction>", methods=["GET","POST"])
def getPokeInfoById(id, direction):
    newDirection = 1 if direction == 'next' else -1 
    form = SearchPokemon()
    # if form.validate_on_submit() and request.method == "POST":
    #name = request.form.get("name")
    info = fetchPokeInfo(str(int(id) + newDirection))
    defaultInfo = info[0]
    abilityInfo = info[1]
    return render_template("pokeSearch.html", form=form, defaultInfo=defaultInfo, abilityInfo=abilityInfo)
    # return render_template("pokeSearch.html", form=form)