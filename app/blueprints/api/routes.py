from . import api
from flask import request, jsonify
from flask_login import current_user

@api.get("/pokemon/<pokemonId>")
def getPokemonById(pokemonId):
    pokemon = current_user.pokemon.all()
    print(pokemonId)