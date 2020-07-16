from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools
import os
import datetime
import dateutil.parser

CALENDAR_ID = os.environ.get('CALENDAR_ID')
GCLIENT_DATA = os.environ.get('GCLIENT_DATA')
NUM_OF_EVENTS = 3


class gevent:
    def __init__(self, event):
        self.name = event['summary']
        self.start = dateutil.parser.parse(event['start']['dateTime'])
        self.date = self.start.strftime("%B %d, %A %H:%M%p")
        self.dateTitle = self.start.strftime("%m/%d")
        self.players = []
        self.count = 0


def get_service(api_name, api_version, scope, key_file_location):
    """Get a service that communicates to a Google API.

    Args:
      api_name: The name of the api to connect to.
      api_version: The api version to connect to.
      scope: A list auth scopes to authorize for the application.
      key_file_location: The path to a valid service account p12 key file.

    Returns:
      A service that is connected to the specified API.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        key_file_location, scopes=scope)
    http = credentials.authorize(httplib2.Http())

    # Build the service object.
    service = build(api_name, api_version, http=http)

    return service


def get_cal_details():
    scope = ['https://www.googleapis.com/auth/calendar.readonly',
             'https://www.googleapis.com/auth/calendar']

    key_file_location = 'client_secret.json'

    # Write out the json string to file
    # since we're hosting it on heroku we need a way
    # to pass the client secrets to the service creation.
    client_json = open(key_file_location, 'w')
    client_json.write(GCLIENT_DATA)
    client_json.write("\n")
    client_json.close()

    # Authenticate and construct service.
    service = get_service('calendar', 'v3', scope, key_file_location)

    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    eventsResult = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=now,
        maxResults=NUM_OF_EVENTS,
        singleEvents=True,
        orderBy='startTime').execute()

    events = eventsResult.get('items', [])
    return events
