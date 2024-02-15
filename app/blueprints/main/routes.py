from . import main
import requests
from flask import render_template, request, flash, redirect, url_for
from .forms import SearchPokemon
from app.models import Pokemon, User, db
from flask_login import current_user, login_required



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

# def fetchAllPokemonOfUser(userID):

    
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
        # if not info:
        #     flash("Please enter a valid pokemon name")
        #     return render_template("pokeSearch.html", form=form)
        # else:
        defaultInfo = info[0]
        img_url = defaultInfo['sprites']['versions']['generation-v']['black-white']['animated']['front_shiny']
        if not img_url:
            img_url = defaultInfo['sprites']['front_default']
        abilityInfo = info[1]
        return render_template("pokeSearch.html", form=form, defaultInfo=defaultInfo, abilityInfo=abilityInfo, img_url=img_url)
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


@main.route("/addToPokedex/<pokemonID>")
def addToPokedex(pokemonID):
    print("POKEMONID =>", pokemonID)
    selected_pokemon_data = fetchPokeInfo(pokemonID)
    if selected_pokemon_data:
        selected_pokemon_name = selected_pokemon_data[0]['name']
        print(selected_pokemon_name)
        selected_pokemon = Pokemon.query.filter_by(name=selected_pokemon_name).first()
        print("SELECTED POKEMON =>>", selected_pokemon)
    if not selected_pokemon:
        sprite_img = selected_pokemon_data[0]['sprites']['versions']['generation-v']['black-white']['animated']['front_shiny']
        if not sprite_img:
            sprite_img =  selected_pokemon_data[0]['sprites']['front_default']
        name = selected_pokemon_name
        base_hp = selected_pokemon_data[0]['stats'][0]['base_stat']
        base_attack = selected_pokemon_data[0]['stats'][1]['base_stat']
        base_defence = selected_pokemon_data[0]['stats'][2]['base_stat']
        ability_name = selected_pokemon_data[0]['abilities'][0]['ability']['name']
        ability_description = selected_pokemon_data[1]['flavor_text_entries'][0]['flavor_text']
        new_pokemon = Pokemon(name, base_hp, base_attack, base_defence, sprite_img, ability_name, ability_description)
        print(new_pokemon)
        new_pokemon.save()
        flash(f"You have caught { selected_pokemon_name}!")
    if selected_pokemon:
        if current_user.pokemon.filter_by(name=selected_pokemon_name).first():
            flash(f"{selected_pokemon_name} is already in your Pokedex!")
        else:
            current_user.pokemon.append(selected_pokemon)
            db.session.commit()
            flash(f"{selected_pokemon_name} is added to your Pokedex")
        
        
    return redirect(url_for("main.getPokeInfo"))






# main.route("/my_pokemon")
# def my_pokemon():
#     pokemon = Pokemon()
#     return render_template("myPokemon.html", pokemon=pokemon)