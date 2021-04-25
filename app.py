import logging
from flask import Flask, request, render_template
from flask_sprinkler import Sprinkler

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

ser = Sprinkler(app)

@app.route('/')
def hello():
    return(render_template('index.html'))

@app.route('/v1/zone', methods=['POST'])
def zone_set():
    zone = request.form['zone']
    time = int(request.form['time'])
    ser.write(f'SPRz{zone}q{time:03}')
    logging.info(f'Sent SPRz{zone}q{time:03}')
    return(render_template('index.html'))

@app.route('/v1/zone', methods=['GET'])
def zone_get():
    return("Current zones waiting:")