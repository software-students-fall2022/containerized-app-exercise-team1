from flask import Flask, render_template, request, redirect, abort, url_for, make_response, flash
from pymongo import MongoClient
import os

#TODO uncomment
# connect to the database
# cxn = MongoClient('localhost', 27017)
# try:
#     # verify the connection works by pinging the database
#     cxn.admin.command('ping') # The ping command is cheap and does not require auth.
#     db = cxn['sample_airbnb'] # store a reference to the database
#     print(' *', 'Connected to MongoDB!') # if we get here, the connection worked!

# except Exception as e:
#     # the ping command failed, so the connection is not available.
#     # render_template('error.html', error=e) # render the edit template
#     print('Database connection error:', e) # debug


# Dummy data!
games = {}

game1 = [
    {
        "roundNum": 1,
        "playerMove": "Scissor",
        "computerMove": "Rock",
        "result": "Lose",
        "timeOfRoundEnd": "...",
        "snapShot": "...",
    },
    {
        "roundNum": 2,
        "playerMove": "Paper",
        "computerMove": "Rock",
        "result": "Win",
        "timeOfRoundEnd": "...",
        "snapShot": "...",
    },
    {
        "roundNum": 3,
        "playerMove": "Scissor",
        "computerMove": "Scissor",
        "result": "Tie",
        "timeOfRoundEnd": "...",
        "snapShot": "...",
    },
    {
        "roundNum": "Invalid",
        "playerMove": "Invalid",
        "computerMove": "Invalid",
        "result": "Invalid",
        "timeOfRoundEnd": "...",
        "snapShot": "...",
    },
]

game2 = [
    {
        "roundNum": 1,
        "playerMove": "Scissor",
        "computerMove": "Rock",
        "result": "Lose",
        "timeOfRoundEnd": "...",
        "snapShot": "...",
    },
    {
        "roundNum": 2,
        "playerMove": "Paper",
        "computerMove": "Rock",
        "result": "Win",
        "timeOfRoundEnd": "...",
        "snapShot": "...",
    },
    {
        "roundNum": 3,
        "playerMove": "Scissor",
        "computerMove": "Scissor",
        "result": "Tie",
        "timeOfRoundEnd": "...",
        "snapShot": "...",
    },
    {
        "roundNum": "Invalid",
        "playerMove": "Invalid",
        "computerMove": "Invalid",
        "result": "Invalid",
        "timeOfRoundEnd": "...",
        "snapShot": "...",
    },
]

games["game1"] = game1
games["game2"] = game2

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html", games=games)


if __name__ == "__main__":
    app.run(debug=True)