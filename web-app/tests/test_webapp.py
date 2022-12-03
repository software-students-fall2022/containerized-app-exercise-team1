from app import configure_routes
from app import find_games
from app import find_game_date
from flask import Flask, render_template
import pytest
import pytest_flask
import pymongo
import mongomock
from datetime import datetime
from bson.objectid import ObjectId

# game = [
#     {
#         "roundNum": 1,
#         "playerMove": "Scissor",
#         "computerMove": "Rock",
#         "result": "Lose",
#         "timeOfRoundEnd": "...",
#         "snapShot": "...",
#     }
# ]


collection = mongomock.MongoClient().db.collection
def test_base_route():

    app = configure_routes(db = collection)
    client = app.test_client()
    url = '/'
    response = client.get(url)
    assert response.status_code == 200
   # assert response.get_data == render_template("home.html",games = {})

def test_game_route():

    app = configure_routes(db = collection)
    client = app.test_client()
    url = '/game'
    response = client.get(url)
    assert response.status_code == 404

def test_wrong_route():
    
    app = configure_routes(db = collection)
    client = app.test_client()
    url = '/test'
    response = client.get(url)
    assert response.status_code == 404

def test_find_games():
    fmt = '%b %d %Y, %I:%M%p'
    date_now = datetime.now().strftime(fmt)
    games = {}
    game_id = collection.games.insert_one({"rounds": [], "date": date_now}).inserted_id
    round_id = collection.rounds.insert_one({"round": 0,
        "user_score": 1,
        "user_gesture": "scissor",
        "cp_score": 0,
        "cp_gesture": "paper",
        "result": "user"}).inserted_id
    game = collection.games.find_one({"_id": ObjectId(game_id)})
    rounds_arr = game["rounds"]
    rounds_arr.append(round_id)
    filter = {"_id": ObjectId(game_id)}
    new_values = {"$set": {"rounds": rounds_arr}}
    collection.games.update_one(filter, new_values)

    this_round = {"_id": round_id,
        "round": 0,
        "user_score": 1,
        "user_gesture": "scissor",
        "cp_score": 0,
        "cp_gesture": "paper",
        "result": "user"}
    games[date_now] = [this_round]
    assert games == find_games(collection)

def test_find_game_date():
    pass
