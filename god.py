from logging import exception
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# import json

flow = InstalledAppFlow.from_client_secrets_file('/Users/saakethmanepalli/Desktop/Intro Comp Sci/cred/credentials.json',
                                                 ['https://www.googleapis.com/auth/forms',
                                                  'https://www.googleapis.com/auth/spreadsheets'])
# don't know how this works
creds = flow.run_local_server(port=0)

# build forms instance
forms = build('forms', 'v1', credentials=creds)
formID = input("Enter Form ID")



try:
    responses = forms.forms().responses().list(formId=formID).execute()
except exception as e:
    print(f"Error retrieving {formID} Data")

