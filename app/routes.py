from flask import request, render_template, redirect, url_for, flash
import requests
from app import app
from app.forms import LoginForm, SignupForm, Get_Poke_Info
from app.models import db, User
# Home


# put of poke_info in to a dict
#
#
def get_poke_info(data):
    poke_info = {
        'baseExp': data.get('base_experience'),
        'spriteURL': data.get('sprites', {}).get('front_default'),
        'spriteShinyURL': data.get('sprites', {}).get('front_shiny'),
        'baseStats': {stat.get('stat', {}).get('name', '').upper() + ':': stat.get('base_stat') for stat in data.get('stats', [])},
        'pokemonType': [pkmnType.get('type', {}).get('name') for pkmnType in data.get('types', [])],
        'pokedexID': data.get('id')
    }
    return poke_info


@app.route('/pokedex', methods=['GET', 'POST'])
def pokedex():
    
    if request.method == 'POST':
        form = get_poke_info()
        pkmn = form.WhateverYouNamedTheFormVariable.data
        
        
        url = url = f"https://pokeapi.co/api/v2/pokemon/{pkmn}"
        response = requests.get(url)
        try:
            data = response.json()['base_experience']['StandingsTable']['StandingsLists'][0]['DriverStandings']
        #call helper function
            all_drivers = get_driver_data(data)
            return render_template('pokedex.html', all_drivers=all_drivers)
        except IndexError:
            return 'Invalid Pokemon'
    else:
        return render_template('pokedex.html', form=form)

@app.route("/")
def home():
    return render_template('base.html')

REGISTERED_USERS = {
    'test@email.com': {
        'name': 'test',
        'password': 'testPassword'
    }
}

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        if email in REGISTERED_USERS and REGISTERED_USERS[email] ['password'] == password:
            flash(f'Login Successful, {REGISTERED_USERS[email]["name"]}!', 'success')
            return redirect(url_for('pokedex'))
        else:
            return 'Invaild email or passord'
    else:
        return render_template('login.html', form=form)
    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        full_name = f'{form.first_name.data} {form.last_name.data}'
        email = form.email.data
        password = form.password.data
        
        
        REGISTERED_USERS[email] = {
            'name': full_name,
            'password': password
        }
        return f'Thank you for signing up {full_name}'
    else:
        return render_template('signup.html', form=form)


