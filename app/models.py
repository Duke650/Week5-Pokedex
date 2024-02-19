from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

user_pokemon = db.Table(
    'user_pokemon',
    db.Column("userID", db.Integer, db.ForeignKey('user.id')),
    db.Column("pokemonID", db.Integer, db.ForeignKey("pokemon.id")))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    pokemon = db.relationship("Pokemon", 
                            secondary = "user_pokemon",
                            backref = "my_pokemon",
                            lazy = "dynamic"
                            )


    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def save(self):
        db.session.add(self)
        db.session.commit()

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, unique=True, nullable=False)
    base_hp = db.Column(db.Integer, nullable=False)
    base_attack = db.Column(db.Integer, nullable=False)
    base_defence = db.Column(db.Integer, nullable=False)
    sprite_img = db.Column(db.String, unique=True, nullable=False)
    ability_name = db.Column(db.String, nullable=False)
    ability_description = db.Column(db.String, nullable=False)


# crate battle result table
    # id of winner
    # id of loser
    # user id maybe
    


    def __init__(self, name, base_hp, base_attack, base_defence, sprite_img, ability_name, ability_description):
        self.name = name
        self.base_hp = base_hp
        self.base_attack = base_attack
        self.base_defence = base_defence
        self.sprite_img = sprite_img
        self.ability_name = ability_name
        self.ability_description = ability_description
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
