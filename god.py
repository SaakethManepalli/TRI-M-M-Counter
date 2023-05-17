import traceback
from googleapiclient.discovery import build
from oauth2client import client, file, tools
from googleapiclient.errors import HttpError
import httplib2
import pandas
import json

httplib2.debuglevel = 4
scopes = ['https://www.googleapis.com/auth/forms', 'https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']
store = file.Storage('token.json')
creds = None
if not creds:
    flow = client.flow_from_clientsecrets('client_secrets.json', scopes)
    creds = tools.run_flow(flow, store)

# build forms instance
forms = build('forms', 'v1', credentials=creds)
urmom = build('sheets', 'v4', credentials=creds)
formID = input("Enter Form ID")

try:
    responses = forms.forms().responses().list(formId=formID).execute()
    with open('form_responses.json', 'w') as f:
        json.dump(responses, f)
except HttpError:  # Cannot try/except non BaseException
    print(f"Error retrieving {formID} Data")
    print(traceback)

'''
begin the json-ing to sheet-ing
'''
with open('form_responses.json', 'r') as f:
    helpme = json.load(f)
    df = pandas.DataFrame.from_dict(helpme)
    print(df)
'''
lost i am
'''
