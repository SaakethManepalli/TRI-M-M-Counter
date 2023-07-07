from googleapiclient.discovery import build
from oauth2client import client, file, tools
from googleapiclient.errors import HttpError
import traceback
import httplib2
import json


global responses


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
formID = '1PaUqIlTJX6Fc_vWVlGNiRvdOWDI9NJDNkmcbvOhFNyE'

responses = forms.forms().responses().list(formId=formID).execute()
with open('form_responses.json', 'w') as f:
    json.dump(responses, f)

if HttpError:
    print("HTTP ERROR")
    quit()


'''
begin the json-ing to sheet-ing
'''
JOSN = json.loads(responses)
rows = len(JOSN['responses'])
columns = len(JOSN['responses'][0]['answers'])
array = [[None for i in range(columns)] for j in range(rows)]
# Iterate over the JSON object and populate the 2D array with the corresponding data.
for i in range(rows):
    for j in range(columns):
        array[i][j] = JOSN['responses'][i]['answers'][j]['value']

spreadsheet = urmom.spreadsheets().create(body={'title': 'Form Responses'}).execute()
sheet = urmom.spreadsheets().get(spreadsheetId=spreadsheet['id']).execute()
values = urmom.spreadsheets().values().update(spreadsheetId=spreadsheet['id'], range='A1:' + chr(ord('A') + columns - 1), body={'values': array}).execute()