
import requests
from flask import Flask, request, render_template


# Build a Single Page Flask Application that has a home page that just greets the user, and 
# then a second route that will have a form to enter a pokemon name that will on submit update the page with 
# some properties listed about the pokemon(properties listed below).  Use your homework (Week 4: Day 4) from 
# when we did this during python to help you with your API call. 



app = Flask(__name__)
if __name__ == "__main__":
    app.run(debug=True)

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



@app.route("/poke-info")
def getPokeInfo():
    return render_template("pokeSearch.html")


@app.route("/poke-info", methods=["POST"])
def addPokeInfo():
    name = request.form.get("name")
    info = fetchPokeInfo(name)
    return render_template("pokeSearch.html", info=info[0], abilityInfo=info[1])

        
