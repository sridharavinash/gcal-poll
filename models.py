from app import db
from sqlalchemy.dialects.postgresql import JSON

class Player(db.Model):
    __tablename__= 'player'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), primary_key=True)

    def __init__(self, id, name):
        self.id = id
        self.name = name

class Event(db.Model):
    __tablename__ = 'event'

    event_name = db.Column(db.String(), primary_key=True)

    def __init__(self, event_name):
        self.event_name = event_name

    def __repr__(self):
        return self.event_name

class Event_Player(db.Model):
    __tablename__ = 'event_player'

    player_id = db.Column(db.Integer(), primary_key=True)
    event_name = db.Column(db.String(), primary_key=True)
    is_playing = db.Column(db.Boolean())

    def __init__(self,player_id, event_name, is_playing):
        self.player_id = player_id
        self.event_name = event_name
        self.is_playing = is_playing
