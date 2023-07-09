from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import json

scopes = ['https://www.googleapis.com/auth/forms',
          'https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

# Load the client secrets from the client_secret.json file
flow = InstalledAppFlow.from_client_secrets_file('secret.json', scopes=scopes)
credentials = flow.run_local_server()

# Build Forms and Sheets instances
forms = build('forms', 'v1', credentials=credentials)
sheets = build('sheets', 'v4', credentials=credentials)

formID = '1PaUqIlTJX6Fc_vWVlGNiRvdOWDI9NJDNkmcbvOhFNyE'
spreadsheetID = '1K8CnEoNG1nPKC_indjAZVN10WpiubQspN9X6ZgAHxIw'

# Retrieve form responses
responses = forms.forms().responses().list(formId=formID).execute()
with open('form_responses.json', 'w') as f:
    json.dump(responses, f)

# Begin processing the responses and storing them in the Google Sheets spreadsheet
rows = len(responses['responses'])
columns = len(responses['responses'][0]['answers'])
array = [[None for _ in range(columns)] for _ in range(rows)]

# Create a dictionary to store the event names and their corresponding column indices
event_mapping = {}
event_columns = []

# Iterate over the responses and populate the 2D array with the corresponding data
for i, response in enumerate(responses['responses']):
    for j, question_id in enumerate(response['answers']):
        answer = response['answers'][question_id]
        if question_id == '745132d8' and 'textAnswers' in answer:
            answer_value = answer['textAnswers']['answers'][0]['value']
            if answer_value.lower() == 'yes':
                value = 'Yes'
            else:
                value = 'No'
        elif question_id == '0f043af5' and 'textAnswers' in answer:
            event = answer['textAnswers']['answers'][0]['value']
            if event not in event_mapping:
                event_mapping[event] = len(event_columns)
                event_columns.append(event)
        elif question_id == '0cf1a445' and 'textAnswers' in answer:
            name = answer['textAnswers']['answers'][0]['value']

    # Find the index of the event column for the current response
    event_index = event_mapping.get(event)

    # Update the corresponding cell in the array with the answer value
    if event_index is not None:
        array[i][event_index] = value

# Create a new row to store the event names
header_row = ['Name'] + event_columns

# Insert the header row at the beginning of the array
array.insert(0, header_row)

# Update the existing spreadsheet with the array of values
range_name = 'Sheet1!A1:' + chr(ord('A') + columns - 1)
values = sheets.spreadsheets().values().update(spreadsheetId=spreadsheetID, range=range_name, valueInputOption='RAW', body={'values': array}).execute()
