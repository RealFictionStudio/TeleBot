from datetime import date
import os
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import Resource, build
from googleapiclient.errors import HttpError

from helpers import event_gen

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

if not load_dotenv():
    print("No new env variables")

PRIMARY = os.getenv("CALNEDAR_ALL")

GROUPS = [
    os.getenv("CALNEDAR_GR1"),
    os.getenv("CALNEDAR_GR2"),
    os.getenv("CALNEDAR_GR3"),
]


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


def del_event(ggl_id_a: int, ggl_id_g: int, group: int):
    try:
        service = build("calendar", "v3", credentials=get_credentials())

        if service.events().delete(calendarId="primary", event_Id=ggl_id_a):
            print("Succesfully deleted event from pirmary calendar")
        if service.events().delete(calendarId=GROUPS[group], event_Id=ggl_id_g):
            print("Succesfully deleted event from group calendar")

    except HttpError as error:
        print("Err: ", error)


def upd_event(
    ggl_id_a: int, ggl_id_g: int, e_date: date, group: int, subject: str, desc: str
):
    try:
        service = build("calendar", "v3", credentials=get_credentials())

        # TODO: Add records that can be changed
        creds = [""]

        event_a = service.events().get(calendar="primary", eventId=ggl_id_a)

        b_event = event_gen(desc, group, subject, e_date)

        for cred in creds:
            event_a[cred] = b_event[cred]

        if service.events().update(
            calendarId="primary", eventId=event_a["id"], body=event_a
        ):
            print("Updated event succesfully in primary calendar")

        event_g = service.events().get(calendar=GROUPS[group], eventId=ggl_id_a)

        b_event = event_gen(desc, group, subject, e_date)

        for cred in creds:
            event_g[cred] = b_event[cred]

        if service.events().update(
            calendarId=GROUPS[group], eventId=event_g["id"], body=event_g
        ):
            print("Updated event succesfully in group calendar")

    except HttpError as error:
        print("Err: ", error)


def create_event(e_date: date, group: int, subject: str, desc: str):
    try:
        service = build("calendar", "v3", credentials=get_credentials())

        b_event = event_gen(desc, group, subject, e_date)

        # calendar = service.calendars().get(calendarId=GROUP1).execute()
        event_a = service.events().insert(calendarId="primary", body=b_event).execute()
        event_g = (
            service.events().insert(calendarId=GROUPS[group], body=b_event).execute()
        )

        print(event_a, event_g)

        return int(event_a.id), int(event_g.id)
    except HttpError as error:
        print("Err: ", error)
        return 0, 0


def main(): ...


if __name__ == "__main__":
    ...
