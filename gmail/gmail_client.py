import base64
import os
import pickle
from email.mime.text import MIMEText
from typing import Dict

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GmailClient:
    def __init__(self, service):
        self._gmail_service = service

    def send_email(
            self,
            receiver: str,
            subject: str,
            body: str,
    ):
        gmail_msg = self._build_gmail_msg_payload(
            sender='me',
            receiver=receiver,
            subject=subject,
            body=body
        )

        self._send_gmail_message(gmail_msg)

    @staticmethod
    def _build_gmail_msg_payload(sender, receiver, subject, body) -> Dict[str, str]:
        message = MIMEText(body)
        message['to'] = receiver
        message['from'] = sender
        message['subject'] = subject

        message_b64_bytes = base64.urlsafe_b64encode(message.as_bytes())
        message_b64_string = message_b64_bytes.decode()
        return {
            'raw': message_b64_string
        }

    def _send_gmail_message(self, message: Dict[str, str]) -> None:
        self._gmail_service.users() \
            .messages() \
            .send(userId='me', body=message) \
            .execute()

    @staticmethod
    def scopes():
        # Delete pickle file when changing this
        return [
            'https://www.googleapis.com/auth/gmail.send'
        ]


def authenticate_gmail_client():
    creds = None

    # The file gmail.token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('gmail.token.pickle'):
        with open('gmail.token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    # Creds can be obtained by following step 1 in
    # https://developers.google.com/gmail/api/quickstart/python
    # (local dev only; url redirect is `http://localhost:9090/`)
    # or from gcp for staging/prod environments
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json',
                GmailClient.scopes()
            )
            creds = flow.run_local_server(port=9090)
        with open('gmail.token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service


gmail_service = authenticate_gmail_client()
gmailClient = GmailClient(gmail_service)
