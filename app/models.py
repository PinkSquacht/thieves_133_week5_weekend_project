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
    baseStats = db.Column(db.String, nullable=False)
    pokemonType = db.Column(db.String, nullable=False)
    pokedexID = db.Column(db.String, nullable=False)
    

    def __init__(self, name, baseExp, spriteURL, spriteShinyURL, baseStats, pokemonType, pokedexID):
        self.name = name
        self.baseExp = baseExp
        self.spriteURL = spriteURL
        self.spriteShinyURL = spriteShinyURL
        self.baseStats = baseStats
        self.pokemonType = pokemonType
        self.pokedexID = pokedexID
