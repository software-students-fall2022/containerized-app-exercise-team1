from app import configure_routes
from flask import Flask, render_template
import pytest
import pytest_flask
import pymongo
import mongomock


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
    assert response.get_data == render_template("home.html",games = {})

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
