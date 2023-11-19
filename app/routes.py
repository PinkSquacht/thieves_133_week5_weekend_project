from flask import request, render_template, redirect, url_for, flash
import requests
from app import app
from app.forms import LoginForm, SignupForm, Get_Poke_Info, BattleForm
from app.models import db, User, Pokemon
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import check_password_hash


# put of poke_info in to a dict
#
#
def get_poke_info(data):
    poke_info = {
        'name': data['forms'][0]['name'],
        'baseExp': data.get('base_experience'),
        'spriteURL': data.get('sprites', {}).get('front_default'),
        'spriteShinyURL': data.get('sprites', {}).get('front_shiny'),
        'hp': data.get('stats', [])[0].get('base_stat'),
        'attack': data.get('stats', [])[1].get('base_stat'),
        'defense': data.get('stats', [])[2].get('base_stat'),
        'specialAttack': data.get('stats', [])[3].get('base_stat'),
        'specialDefense': data.get('stats', [])[4].get('base_stat'),
        'speed': data.get('stats', [])[5].get('base_stat'),
        'pokemonType': [pkmnType.get('type', {}).get('name') for pkmnType in data.get('types', [])],
        'pokedexID': data.get('id')
    }
    return poke_info


# Pokedex route to get Pokemon info from the API and display it to the user in a template 
@app.route('/pokedex', methods=['GET', 'POST'])
@login_required
def pokedex():
    form = Get_Poke_Info()
    if request.method == 'POST' and form.validate_on_submit():
        pkmn = form.pokemon_name.data

        # Query the database to check if the Pokemon is in the user's team
        pokemon = next((p for p in current_user.pokemons if p.name == pkmn), None)

        if pokemon:
            # The Pokemon is in the user's team
            poke = pokemon
            
        elif pokemon and len(current_user.pokemons) >= 6:
            # Check if the user's team is full
                flash('Your team is full. You can have a maximum of 6 Pokemon in your team.')
        else:
            # The Pokemon is not in the user's team, fetch data from the API
            try:
                url = f"https://pokeapi.co/api/v2/pokemon/{pkmn}"
                response = requests.get(url)
                data = response.json()
                poke = get_poke_info(data)

                # Create a new Pokemon instance and add it to the user's team
                new_pokemon = Pokemon(name=poke['name'], baseExp=poke['baseExp'], spriteURL=poke['spriteURL'], spriteShinyURL=poke['spriteShinyURL'], hp=poke['hp'], attack=poke['attack'], defense=poke['defense'], specialAttack=poke['specialAttack'], specialDefense=poke['specialDefense'], speed=poke['speed'], pokemonType=poke['pokemonType'], pokedexID=poke['pokedexID'])
                current_user.pokemons.append(new_pokemon)
                db.session.commit()

            except IndexError:
                return 'Invalid Pokemon'

        return render_template('pokedex.html', pkmn=poke, form=form)
    else:
        return render_template('pokedex.html', form=form)

@app.route('/team')
@login_required
def team():
    # get the user's team from the database and display it to the user in a template
    team = current_user.pokemons
    
    return render_template('team.html', team=team)

@app.route('/remove_pokemon/<pokemon_name>', methods=['POST'])
@login_required
def remove_pokemon(pokemon_name):
    # Find the Pokemon in the user's team
    pokemon = next((p for p in current_user.pokemons if p.name == pokemon_name), None)

    if pokemon:
        # Remove the Pokemon from the user's team
        current_user.pokemons.remove(pokemon)
        db.session.commit()

    return redirect(url_for('team'))

@app.route("/")
def home():
    return render_template('base.html')

REGISTERED_USERS = {
    'test@email.com': {
        'name': 'test',
        'password': 'testPassword'
    }
}
# Battle Route
@app.route('/battle', methods=['GET', 'POST'])
@login_required
def battle():
    form = BattleForm()  # A form for entering the other user's username or email
    if request.method == 'POST' and form.validate_on_submit():
        opponent_email = form.email.data
        opponent = User.query.filter_by(email=opponent_email).first()
        if opponent:
            # Get the teams of the current user and the opponent
            current_user_team = current_user.pokemons
            opponent_team = opponent.pokemons
            return render_template('battle.html', current_user_team=current_user_team, opponent_team=opponent_team, form=form)
        else:
            flash('User not found', 'error')
    return render_template('battle.html', form=form)
# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
       # some extra error handling 
        user = User.query.filter_by(email=email).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('pokedex'))
        
    else:
        flash('Please Login', 'info')
        return render_template('login.html', form=form)
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        firstName = form.first_name.data
        lastName = form.last_name.data
        email = form.email.data
        password = form.password.data
        new_user = User(firstName, lastName, email, password)
        db.session.add(new_user)
        db.session.commit()
        
        

        #flash(f'Thank you for signing up {full_name}', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('signup.html', form=form)


