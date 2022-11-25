from flask import Flask, render_template, request, redirect, abort, url_for, make_response, flash
from bson.objectid import ObjectId
from pymongo import MongoClient
import os

# connect to the database


cxn = MongoClient("mongodb://127.0.0.1:27017")
try:
    # verify the connection works by pinging the database
    cxn.admin.command('ping') # The ping command is cheap and does not require auth.
    db = cxn['ml_client'] # store a reference to the database
    print(' *', 'Connected to MongoDB!') # if we get here, the connection worked!

except Exception as e:
    # the ping command failed, so the connection is not available.
    # render_template('error.html', error=e) # render the edit template
    print('Database connection error:', e) # debug

app = Flask(__name__)

@app.route('/')
def home():
    games = {}
    round_arr = []
    for game in db.games.find({}):
        for round_id in game["rounds"]:
            round_arr.append(db.rounds.find_one({"_id":ObjectId(round_id)}))
        games[game["date"]] = round_arr 
    return render_template("home.html", games=games)

if __name__ == "__main__":
    app.run(debug=True)