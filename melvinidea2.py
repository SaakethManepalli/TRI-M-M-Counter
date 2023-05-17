from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google_auth_oauthlib.flow import InstalledAppFlow
import json

# Load credentials from the credentials.json file
flow = InstalledAppFlow.from_client_secrets_file('/Users/saakethmanepalli/Desktop/Intro Comp Sci/cred/credentials.json',
                                                 ['https://www.googleapis.com/auth/forms',
                                                  'https://www.googleapis.com/auth/spreadsheets'])

# Authorize the application to access the Google APIs
creds = flow.run_local_server(port=0)
'''
port 0 just chooses a random port?
'''
# create a sheets / forms  API client
sheets_service = build('sheets', 'v4', credentials=creds)
forms = build('forms', 'v1',credentials=creds )

# define the sheet and range
sheet_id = '1429282887'
range_name = 'Sheet1!A1:D1'

# retrieve the sheet data
try:
    rows = forms.responses.get()
    # convert the data to a JSON object
    data = {}
    for row in rows:
        email = row[2]
        event = row[1]
        response = row[3]
        if email not in data:
            data[email] = {}
        data[email][event] = response
    with open('form_responses.json', 'w') as f:
        json.dump(data, f)
except HttpError as error:
    print(f'HTTP ERROR: {error}')

# update the sheet data
with open('form_responses.json', 'r') as f:
    data = json.load(f)
for email, events in data.items():
    for event, response in events.items():
        try:
            # find the row then column for each email
            email_range = f'Sheet1!C:C'
            email_index = sheets_service.spreadsheets().values().get(
                spreadsheetId=sheet_id, range=email_range).execute()['values'].index([email]) + 1
            event_range = f'Sheet1!1:1'
            event_index = sheets_service.spreadsheets().values().get(
                spreadsheetId=sheet_id, range=event_range).execute()['values'][0].index(event) + 1
            # place response in da inaugurated box
            value_range = f'Sheet1!{event_index}{email_index}:{event_index}{email_index}'
            value_input_option = 'USER_ENTERED'
            value_range_body = {
                'range': value_range,
                'majorDimension': 'ROWS',
                'values': [[response]],
            }
            sheets_service.spreadsheets().values().update(
                spreadsheetId=sheet_id, range=value_range,
                valueInputOption=value_input_option, body=value_range_body).execute()
        except ValueError:
            print(f'Email {email} or event {event} not found.')
