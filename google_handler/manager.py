from datetime import date, datetime, timedelta
import os
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import Resource, build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

if not load_dotenv():
    print("No new env variables")

PRIMARY = os.getenv("CALNEDAR_ALL")
GROUP1 = os.getenv("CALNEDAR_GR1")
GROUP2 = os.getenv("CALNEDAR_GR2")
GROUP3 = os.getenv("CALNEDAR_GR3")


def get_credentials():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            _ = creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


def main():
    try:
        service = build("calendar", "v3", credentials=get_credentials())

        b_event = {
            "summary": "Kolokwium z PRM",
            "desctiption": "Hehe",
            "start": {
                "dateTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "timeZone": "Europe/Warsaw",
            },
            "end": {
                "dateTime": (datetime.now() + timedelta(hours=1)).strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
                "timeZone": "Europe/Warsaw",
            },
        }

        # calendar = service.calendars().get(calendarId=GROUP1).execute()
        event = service.events().insert(calendarId="primary", body=b_event).execute()
        print(event)
    except HttpError as error:
        print("Err: ", error)


def event_gen(summary: str, desc: str, start: date, end: date): ...
