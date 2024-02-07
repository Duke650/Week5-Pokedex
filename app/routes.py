import requests
from flask import Flask, request, render_template
from app import app
from .forms import SearchPokemon

@app.route("/")
def home():
    return "<p>Welcome!</p>"

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



@app.route("/poke-info", methods=["GET","POST"])
def getPokeInfo():
    form = SearchPokemon()
    if form.validate_on_submit() and request.method == "POST":
        name = request.form.get("name")
        print("IN THE FORM")
        info = fetchPokeInfo(name)
        defaultInfo = info[0]
        abilityInfo = info[1]
        return render_template("pokeSearch.html", form=form, defaultInfo=defaultInfo, abilityInfo=abilityInfo)
    return render_template("pokeSearch.html", form=form)

    