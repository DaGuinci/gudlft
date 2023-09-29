import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


# Filter used in welcome template
def is_competition_in_the_past(competition):
    now = datetime.now()
    competition_datetime = datetime.strptime(
        competition['date'],
        '%Y-%m-%d %H:%M:%S'
        )
    if competition_datetime < now:
        return True
    else:
        return False


app.add_template_filter(is_competition_in_the_past)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    club = None
    for registered_club in clubs:
        if registered_club['email'] == request.form['email']:
            club = registered_club
    if club is None:
        flash('Email not found. Please verify email.')
        return redirect(url_for('index'))

    return render_template(
        'welcome.html',
        club=club,
        competitions=competitions
        )


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template(
            'booking.html',
            club=foundClub,
            competition=foundCompetition
            )
    else:
        flash("Something went wrong-please try again")
        return render_template(
            'welcome.html',
            club=club,
            competitions=competitions
            )


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():

    competition = None
    for c in competitions:
        if c['name'] == request.form['competition']:
            competition = c

    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])

    # Is the competition still to be played
    now = datetime.now()
    competition_datetime = datetime.strptime(
        competition['date'],
        '%Y-%m-%d %H:%M:%S'
        )
    if competition_datetime < now:
        flash('You can\'t book any place in a past competition.')
        return render_template(
            'welcome.html',
            club=club,
            competitions=competitions
            )
    # Does club have enough points
    elif int(club['points']) - placesRequired < 0:
        flash('You can\'t spend more points than you have.')
        return render_template(
            'booking.html',
            club=club,
            competition=competition
            )
    # isnt booking more than 12 places
    elif placesRequired > 12:
        flash('You can\'t book more than 12 places in a competition.')
        return render_template(
            'booking.html',
            club=club,
            competition=competition
            )
    # are there enough places available
    elif placesRequired > int(competition['numberOfPlaces']):
        flash('There aren\'t enough places available in this competition.')
        return render_template(
            'booking.html',
            club=club,
            competition=competition
            )
    else:
        competition['numberOfPlaces'] = (
            int(competition['numberOfPlaces']) - placesRequired
            )
        club['points'] = (int(club['points']) - placesRequired)
        flash('Great-booking complete!')
        return render_template(
            'welcome.html',
            club=club,
            competitions=competitions
            )


@app.route('/board')
def view_board():
    return render_template(
        'board.html',
        clubs=clubs,
        )


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
