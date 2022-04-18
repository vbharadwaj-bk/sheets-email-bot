from __future__ import print_function

import os.path, base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from email.mime.text import MIMEText
import time
import argparse

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.compose',
'https://www.googleapis.com/auth/spreadsheets.readonly'
]

# This is only the test spreadsheet!
RANGE_NAME = 'Sheet1!A:E'

def create_message(sender, to, cc, bcc, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['cc'] = cc
  message['bcc'] = bcc
  message['from'] = sender
  message['subject'] = subject

  raw = base64.urlsafe_b64encode(message.as_bytes())
  raw = raw.decode()

  return {'raw': raw} 

def send_message(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print(f"Message Id: {message['id']}")
    return message
  except HttpError as error:
    print(f'An error occurred: {error}')

def main(sender_address, spreadsheet_id):
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # ==========================================================
    # Actually where the spreadsheet parsing occurs

    try:
        # Call the Gmail API
        rows = []
        service = build('sheets', 'v4', credentials=creds)

        keys = ["recipients", "cc", "bcc", "subject", "message"] 

        # Call the Sheets API
        sheet = service.spreadsheets()
        print(spreadsheet_id)
        result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                    range=RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        for row in values[1:]:
            rows.append(dict(zip(keys, row)))

        service = build('gmail', 'v1', credentials=creds)

        for el in rows:
            el['formatted_to'] = ', '.join(el['recipients'].replace(' ', '').split(','))
            el['formatted_cc'] = ', '.join(el['cc'].replace(' ', '').split(','))
            el['formatted_bcc'] = ', '.join(el['bcc'].replace(' ', '').split(','))

        # Compose the emails 
        for el in rows:
            to = el['formatted_to']
            cc = el['formatted_cc']
            bcc = el['formatted_bcc']
            msg = create_message(sender_address, to, cc, bcc, el['subject'], el["message"])
            print(f"Sending Email to {to}, CC: {cc}, bCC: {bcc}")
            send_message(service, 'me', msg)

            # Waits two seconds between email messages so that
            # spam detection doesn't get triggered 
            time.sleep(2)

    except HttpError as error: 
        print(f'An error occurred: {error}') 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('sender_address', type=str, 
                        help='The sender email address')
    parser.add_argument('sheet_id', type=str, 
                        help='The ID of the Google Sheet')

    args = parser.parse_args()
    main(args.sender_address, args.sheet_id)
