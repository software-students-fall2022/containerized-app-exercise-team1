from flask import Flask, render_template, request, redirect, abort, url_for, make_response, flash
from bson.objectid import ObjectId
import pymongo
import os

# connect to the database

database = None
cxn = pymongo.MongoClient("mongodb",27017)
try:
    # verify the connection works by pinging the database
    cxn.admin.command('ping') # The ping command is cheap and does not require auth.
    database = cxn['ml_client'] # store a reference to the database
    print(' *', 'Connected to MongoDB!') # if we get here, the connection worked!

except Exception as e:
    # the ping command failed, so the connection is not available.
    # render_template('error.html', error=e) # render the edit template
    print('Database connection error:', e) # debug

def find_games(db):
    games = {}
    round_arr = []
    for game in db.games.find({}):
        for round_id in game["rounds"]:
            round_arr.append(db.rounds.find_one({"_id":ObjectId(round_id)}))
        games[game["date"]] = round_arr
    return games

def find_game_date(db, date):
    round_arr = []
    for round_id in db.games.find_one({"date":date})["rounds"]:
        round_arr.append(db.rounds.find_one({"_id":ObjectId(round_id)}))
    game = round_arr
    return game

def configure_routes(db):
    # set up a web app with correct routes
    app = Flask(__name__)
    @app.route('/')
    def home():
        games = find_games(db)
        return render_template("home.html", games=games)
    @app.route('/game/<date>')
    def game(date):
        game = find_game_date(db, date)
        return render_template("game.html", game = game)
    return app

app = configure_routes(db = database)

if __name__ == "__main__":
    app.run(debug=True)
