from app import configure_routes
from flask import Flask, render_template
import pytest
import pytest_flask
from pymongo import MongoClient

game = [
    {
        "roundNum": 1,
        "playerMove": "Scissor",
        "computerMove": "Rock",
        "result": "Lose",
        "timeOfRoundEnd": "...",
        "snapShot": "...",
    }
]

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


def test_base_route():

    app = configure_routes()
    client = app.test_client()
    url = '/'
    response = client.get(url)
    #assert response.get_data() == b'Hello, World!'
    assert response.status_code == 200

def test_wrong_route():

    app = configure_routes()
    client = app.test_client()
    url = '/test'
    response = client.get(url)
    assert response.status_code == 404