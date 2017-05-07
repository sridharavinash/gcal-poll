from flask import Flask
from flask import render_template
import argparse

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools

import datetime
import os

app = Flask(__name__)

CALENDAR_ID = os.environ.get('CALENDAR_ID')
GCLIENT_DATA = os.environ.get('GCLIENT_DATA')

def get_service(api_name, api_version, scope, key_file_location):
  """Get a service that communicates to a Google API.

  Args:
    api_name: The name of the api to connect to.
    api_version: The api version to connect to.
    scope: A list auth scopes to authorize for the application.
    key_file_location: The path to a valid service account p12 key file.
    service_account_email: The service account email address.

  Returns:
    A service that is connected to the specified API.
  """
  credentials = ServiceAccountCredentials.from_json_keyfile_name(key_file_location, scopes=scope)
  http = credentials.authorize(httplib2.Http())

  # Build the service object.
  service = build(api_name, api_version, http=http)

  return service

@app.route('/')
def index():
    scope = ['https://www.googleapis.com/auth/calendar.readonly','https://www.googleapis.com/auth/calendar']

    # Use the developer console and replace the values with your
    # service account email and relative location of your key file.
    key_file_location = 'client_secret.json'

    #write out the json string to file
    client_json = open(key_file_location, 'w')
    client_json.write(GCLIENT_DATA)
    client_json.write("\n")
    client_json.close();

    # Authenticate and construct service.
    service = get_service('calendar', 'v3', scope, key_file_location)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    eventsResult = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=now,
        maxResults=2,
        singleEvents=True,
        orderBy='startTime').execute()

    events = eventsResult.get('items', [])


    return render_template("index.html", events=events)
