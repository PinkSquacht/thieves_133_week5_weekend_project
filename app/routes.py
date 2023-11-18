from flask import request, render_template, redirect, url_for, flash
import requests
from app import app
from app.forms import LoginForm, SignupForm, Get_Poke_Info
from app.models import db, User, Pokemon
from flask_login import current_user, login_user, logout_user, login_required


# put of poke_info in to a dict
#
#
def get_poke_info(data):
    poke_info = {
        'name': data['forms'][0]['name'],
        'baseExp': data.get('base_experience'),
        'spriteURL': data.get('sprites', {}).get('front_default'),
        'spriteShinyURL': data.get('sprites', {}).get('front_shiny'),
        'baseStats': {stat.get('stat', {}).get('name', '').upper() + ':': stat.get('base_stat') for stat in data.get('stats', [])},
        'pokemonType': [pkmnType.get('type', {}).get('name') for pkmnType in data.get('types', [])],
        'pokedexID': data.get('id')
    }
    return poke_info


# Pokedex route to get Pokemon info from the API and display it to the user in a template 
@app.route('/pokedex', methods=['GET', 'POST'])
def pokedex():
    form = Get_Poke_Info()
    if request.method == 'POST' and form.validate_on_submit():
        pkmn = form.pokemon_name.data

        # Query the database to check if the Pokemon is in the user's team
        user = User.query.get(current_user.id)
        pokemon = next((p for p in user.pokemons if p.name == pkmn), None)

        if pokemon:
            # The Pokemon is in the user's team
            poke = pokemon
        else:
            # The Pokemon is not in the user's team, fetch data from the API
            try:
                url = f"https://pokeapi.co/api/v2/pokemon/{pkmn}"
                response = requests.get(url)
                data = response.json()
                poke = get_poke_info(data)

                # Create a new Pokemon instance and add it to the user's team
                new_pokemon = Pokemon(name=poke['name'], baseExp=poke['base_experience'], spriteURL=poke['sprites']['front_default'], spriteShinyURL=poke['sprites']['front_shiny'], baseStats=poke['stats'], pokemonType=poke['types'], pokedexID=poke['id'])
                user.pokemons.append(new_pokemon)
                db.session.commit()

            except IndexError:
                return 'Invalid Pokemon'

        return render_template('pokedex.html', pkmn=poke, form=form)
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
        flash('Please Login', 'info')
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
        #flash(f'Thank you for signing up {full_name}', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('signup.html', form=form)


