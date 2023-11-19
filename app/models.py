from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

# creating instance of database
db = SQLAlchemy()

team = db.Table('team',
                db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                db.Column('pokemon_name', db.String, db.ForeignKey('pokemon.name'), primary_key=True)
                )

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    pokemons = db.relationship('Pokemon', secondary=team, backref=db.backref('users', lazy='dynamic'))       
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)
    

class Pokemon(db.Model):
    name = db.Column(db.String, primary_key=True)
    baseExp = db.Column(db.String, nullable=False)
    spriteURL = db.Column(db.String, nullable=False)
    spriteShinyURL = db.Column(db.String, nullable=False)
    hp = db.Column(db.String, nullable=False)
    attack = db.Column(db.String, nullable=False)
    defense = db.Column(db.String, nullable=False)
    speacial_Attack = db.Column(db.String, nullable=True)
    specialDefense = db.Column(db.String, nullable=True)
    speed =  db.Column(db.String, nullable=False)
    pokemonType = db.Column(db.String, nullable=False)
    pokedexID = db.Column(db.String, nullable=False)
    

    def __init__(self, name, baseExp, spriteURL, spriteShinyURL, pokemonType, pokedexID, hp, attack, defense, specialAttack, specialDefense, speed):
        self.name = name
        self.baseExp = baseExp
        self.spriteURL = spriteURL
        self.spriteShinyURL = spriteShinyURL
        self.pokemonType = pokemonType
        self.pokedexID = pokedexID
        self.hp = hp
        self.attack = attack     
        self.defense = defense
        self.special_Attack = specialAttack
        self.specialDefense = specialDefense
        self.speed = speed
        
