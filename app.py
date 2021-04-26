import logging
import json
from flask import Flask, request, render_template
from flask_sprinkler import Sprinkler
from flask_bootstrap import Bootstrap

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
Bootstrap(app)

spr = Sprinkler(app)

@app.route('/')
def hello():
    return(render_template('index.html'))

@app.route('/v1/zone', methods=['POST'])
def zone_set():
    zone = request.form['zone']
    time = int(request.form['time'])
    spr.write(f'SPRz{zone}q{time:03}')
    logging.info(f'Sent SPRz{zone}q{time:03}')
    return(render_template('index.html'))

@app.route('/v1/zone', methods=['GET'])
def zone_get():
    return(json.dumps(spr.get_sprinkler_state()))

@app.route('/v1/stopall', methods=['POST'])
def stop_all():
    spr.write('SPRz00t000')
    return(render_template('index.html'))

@app.route('/v1/pause', methods=['POST'])
def pause_program():
    spr.write('SPRw')
    spr.write('SPR?')
    return(render_template('index.html'))