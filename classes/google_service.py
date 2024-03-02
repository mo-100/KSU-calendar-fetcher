import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from classes.uploadable import Uploadable


class GoogleService:
    def __init__(self):
        scopes = [
            "https://www.googleapis.com/auth/calendar",
            "https://www.googleapis.com/auth/calendar.events"
        ]
        creds = None

        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', scopes)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', scopes)
                creds = flow.run_local_server(port=0)

            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('calendar', 'v3', credentials=creds)

        self.color_num = 0
        self.course_colors = {}

    def color_of(self, symbol):
        if symbol not in self.course_colors.keys():
            self.course_colors[symbol] = self.color_num
            self.color_num = (self.color_num + 1) % 12
        return self.course_colors[symbol]

    def upload(self, items: list[Uploadable]):
        for item in items:
            try:
                color = self.color_of(item.symbol)
                self.service.events().insert(calendarId='primary', body=item.to_json(color)).execute()
                print(f"event created: {item}")
            except HttpError as e:
                print(f'An error occurred while uploading {item}')
                print(f'error: {e}')
