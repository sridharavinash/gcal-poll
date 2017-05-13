# gcal-poll

* Simple polling app.
* Syncs with gcal.
* Hosted on Heroku.

# Development

## setting up local postgres db

Make sure you have postgresql installed for your environment.

Create a local database named `mylocaldb`

## Setup app

Setup `virtualenv`. If it's not installed on your system follow instructions
from [here](http://flask.pocoo.org/docs/0.12/installation/)

In a terminal run
```
> cd gcal-poll

> virtualenv venv
> . venv/bin/activate
> pip install -r requirements.txt
> export DATABASE_URL="postrgres:\\localhost\mylocaldb"
```

## Init db

Init scripts to setup migrations
```
> python manage_db.py db init
> python manage_db.py db migrate
> python manage_db.py db upgrade
```

## Setup gcal credentials

We'll need to add google calendar credentials.

Setup an [OAUTH Service account](https://developers.google.com/identity/protocols/OAuth2ServiceAccount).
Make sure you give the service account access to the calendar.

Set the content of the downloaded credentials as an ENV var for testing.

```
> export GCLIENT_DATA=`cat client_secret.json`
```

## Run the app

```
> python app.py
```

The local server should be available at http://localhost:5000
