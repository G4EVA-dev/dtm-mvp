import requests
from flask import Flask

app = Flask(__name__)

def test_requests():
    response = requests.get('https://api.github.com')
    assert response.status_code == 200

def test_flask():
    assert app.name == 'test_app' 