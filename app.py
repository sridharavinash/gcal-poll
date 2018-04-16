from flask import Flask
from flask import render_template
from flask import request, jsonify
import argparse
import itertools
import os
from flask_sqlalchemy import SQLAlchemy
from libs import gcal_client
from operator import itemgetter, attrgetter

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

import models


@app.route('/')
def index():
    events = gcal_client.get_cal_details()
    gevents=[]
    for event in events:
        ge = gcal_client.gevent(event)
        db_event = models.Event(ge.name)
        db.session.merge(db_event)
        db.session.commit()
        playing =  db.session.query(models.Player.name)\
        .join(models.Event_Player, models.Player.id == models.Event_Player.player_id)\
        .filter(models.Event_Player.event_name == ge.name, models.Event_Player.is_playing)

        #flatten the list of tuple names
        ge.players = list(itertools.chain(*playing.all()))
        ge.count = len(ge.players)
        gevents.append(ge)
    players = sorted(models.Player.query.all(), key=attrgetter('name'))

    return render_template("index.html", events=gevents,players=players)

@app.route('/_update_poll', methods=['POST'])
def update_poll():
    new_ep = models.Event_Player(request.form['player_id'], request.form['event_name'], True)
    ep = models.Event_Player.query.filter_by(player_id = new_ep.player_id, event_name = new_ep.event_name).first()
    if ep:
        new_ep.is_playing = not ep.is_playing
        db.session.merge(new_ep)
        db.session.commit()
        return jsonify({'msg': 'updated'})

    db.session.add(new_ep)
    db.session.commit()
    return jsonify({'msg':'added'})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
