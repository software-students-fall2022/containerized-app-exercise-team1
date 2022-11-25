from app import configure_routes
from flask import Flask, render_template
import pytest
import pytest_flask

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