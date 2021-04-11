import logging
from flask import Flask
from flask_sprinkler import Sprinkler

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

ser = Sprinkler(app)

@app.route('/')
def hello():
    ser.write('!SPRw')
    return('Hello world!')