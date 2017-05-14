# gcal-poll

* Simple polling app.
* Syncs with gcal.
* Hosted on Heroku.

# Development

## setting up local postgres db

Make sure you have postgresql installed for your environment.
See Ubuntu instructions [here](https://help.ubuntu.com/community/PostgreSQL)
```
$ sudo apt-get install postgresql postgresql-contrib
```

Optionally install a handy GUI:
```
$ sudo apt-get install pgadmin3
```

Create a local database named `mylocaldb`
```
$ sudo -u postgres psql postgres
postgres=# \password postgres
Ctrl+D
$ sudo -u postgres createdb mylocaldb
```

## Setup app

Setup `virtualenv`. If it's not installed on your system follow instructions
from [here](http://flask.pocoo.org/docs/0.12/installation/)
```
$ sudo apt-get install python-virtualenv
```

In a terminal run
```
> cd gcal-poll

> virtualenv venv
> . venv/bin/activate
> pip install -r requirements.txt
> export DATABASE_URL='postgres://postgres:<password>@localhost/mylocaldb'
```

## Init db

Setup db schema
```
> python manage_db.py db upgrade
```

## Setup gcal credentials

We'll need to add google calendar credentials.

Setup an [OAUTH Service account](https://developers.google.com/identity/protocols/OAuth2ServiceAccount).
Make sure you give the service account access to the calendar.

Set the content of the downloaded credentials as an ENV var for testing.

```
> export GCLIENT_DATA=`cat client_secret.json`
> export CALENDAR_ID=<your_calendar_address>
```

## Run the app

```
> python app.py
```

The local server should be available at http://localhost:5000
