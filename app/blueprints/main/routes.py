from . import main
import requests
from flask import render_template, request, flash, redirect, url_for, session
from .forms import SearchPokemon
from app.models import Pokemon, User, db, user_pokemon
from flask_login import current_user, login_required
import random



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
    selected_pokemon_data = fetchPokeInfo(pokemonID)
    if selected_pokemon_data:
        selected_pokemon_name = selected_pokemon_data[0]['name']
        print(selected_pokemon_name)
        selected_pokemon = Pokemon.query.filter_by(name=selected_pokemon_name).first()

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
        
        selected_pokemon = Pokemon.query.filter_by(name=selected_pokemon_name).first()
    if len(current_user.pokemon.all()) >= 6:
        flash("You can only have 6 Pokemon", "warning")
        return redirect(url_for("main.getPokeInfo"))
    if current_user.pokemon.filter_by(name=selected_pokemon_name).first():
        flash(f"{selected_pokemon_name} is already in your Pokedex!", "warning")
    else:
        current_user.pokemon.append(selected_pokemon)
        db.session.commit()
        flash(f"{selected_pokemon_name} is added to your Pokedex", "success")

    return redirect(url_for("main.getPokeInfo"))



@main.route("/my_pokemon")
def my_pokemon():
    user = User.query.get(current_user.id)
    if user:
        userPokemon = user.pokemon.all()
        allUserPokemon = []
        for pokemon in userPokemon:
            pokeObj = {
            'id': pokemon.id,
            'sprite_img': pokemon.sprite_img,
            'name': pokemon.name,
            'base_hp': pokemon.base_hp,
            'base_attack': pokemon.base_attack,
            'base_defence': pokemon.base_defence,
            'ability_name': pokemon.ability_name,
            'ability_description': pokemon.ability_description
            }
            allUserPokemon.append(pokeObj)
        username = current_user.username
        return render_template("myPokemon.html", allUserPokemon=allUserPokemon, username=username)
    else:
        render_template("myPokemon.html")

@main.route('/release/<pokemonID>')
def release(pokemonID):
    user = User.query.get(current_user.id)
    print("USER =>", user.pokemon.all())
    if user:
        selectedPokemon = user.pokemon.filter_by(id = pokemonID).first()
        if selectedPokemon:
            db.session.delete(selectedPokemon)
            db.session.commit()
            return redirect(url_for("main.my_pokemon"))
    return redirect(url_for("main.my_pokemon"))

@main.route("/battle")
def battle():
    allUsers = User.query.filter(User.id != current_user.id).all()
    randomUserID = random.randint(1, len(allUsers))
    print("RANDOM", randomUserID)
    randomUser = User.query.get(randomUserID)
    session['randomUserID'] = randomUserID
    
    randomUsername = randomUser.username
    currentUsername = current_user.username
    session['randomUsername'] = randomUsername
    if randomUser.id != current_user.id:
        randomUserPokemon = randomUser.pokemon.all()
        allRandomUserPokemon = []
        for pokemon in randomUserPokemon:
            pokeObj = {
            'id': pokemon.id,
            'sprite_img': pokemon.sprite_img,
            'name': pokemon.name,
            'base_hp': pokemon.base_hp,
            'base_attack': pokemon.base_attack,
            'base_defence': pokemon.base_defence,
            'ability_name': pokemon.ability_name,
            'ability_description': pokemon.ability_description
            }
            allRandomUserPokemon.append(pokeObj)
        currentUserPokemon = current_user.pokemon.all()
        allCurrentUserPokemon = []
        for pokemon in currentUserPokemon:
            pokeObj = {
            'id': pokemon.id,
            'sprite_img': pokemon.sprite_img,
            'name': pokemon.name,
            'base_hp': pokemon.base_hp,
            'base_attack': pokemon.base_attack,
            'base_defence': pokemon.base_defence,
            'ability_name': pokemon.ability_name,
            'ability_description': pokemon.ability_description
            }
            allCurrentUserPokemon.append(pokeObj)
            session['opponentPokeData'] = allRandomUserPokemon
            session['playerPokeData'] = allCurrentUserPokemon
        if allRandomUserPokemon and allCurrentUserPokemon:
            return render_template("currentFight.html", allRandomUserPokemon=allRandomUserPokemon, allCurrentUserPokemon=allCurrentUserPokemon, randomUsername=randomUsername, currentUsername=currentUsername, randomUserID=randomUserID)

    return redirect(url_for("main.my_pokemon"))

def getPokeInfoById(listOfPokemon, id):
    id = int(id)
    if not listOfPokemon:
        return "No pokemon found"
    for poke in listOfPokemon:
        
        if poke['id'] == int(id):
            return poke

    return f"cound not find pokemon with id of {id}"


@main.route("/attack/<attackerID>/<defenderID>")
def attack(attackerID, defenderID):
    # if not attackerID or not defenderID: 
    #     flash("Please select a valid pokemon to attack", "success")
    #     return redirect(url_for('main.battle'))
    playerPokeData = session['playerPokeData']
    opponentPokeData = session['opponentPokeData']
    mainUser = User.query.get(current_user.id)
    mainUsername = mainUser.username
    print("MAIN USER", mainUsername)
    print("RANDOM USERNAME!!! =>>", session['randomUsername'])
    attacker = {}
    defender = {}
    for pokemon in playerPokeData:
        if pokemon['id'] == int(attackerID):
            attacker = pokemon
    for pokemon in opponentPokeData:
        if pokemon['id'] == int(defenderID):
            defender = pokemon
    if attacker is None or defender is None:
        flash("Attacker or Defender Pokemon not found.")
        return redirect(url_for('main.battle'))

    print("ORIGINAL HP =>", defender['base_hp'])
    defender['base_hp'] -= attacker['base_attack'] // (defender['base_defence'] // 2) * 10
    attacker['base_hp'] -= defender['base_attack'] // (attacker['base_defence'] // 2) * 10
    if defender['base_hp'] <= 0:
        opponentPokeData = [pokemon for pokemon in opponentPokeData if pokemon['id'] != defender['id']]
        print("NEW HP =>>", defender['base_hp'])
    if attacker['base_hp'] <= 0:
        playerPokeData = [pokemon for pokemon in playerPokeData if pokemon['id'] != attacker['id']]

    session['opponentPokeData'] = opponentPokeData
    session['playerPokeData'] = playerPokeData
    print("CURRENT OPPONENT POKEMON", opponentPokeData)


    return render_template("currentFight.html", mainUsername=mainUsername, )
    
    # store results in battle results table
    # display rest of pokemon expect losers