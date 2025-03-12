from datetime import date
import os
from dotenv import load_dotenv
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import Resource, build
from googleapiclient.errors import HttpError
from googleapiclient.http import HttpRequest

from helpers import event_gen

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

if not load_dotenv():
    print("No new env variables")

PRIMARY = os.getenv("CALNEDAR_ALL")

GROUPS = [
    os.getenv("CALNEDAR_GR1"),
    os.getenv("CALNEDAR_GR2"),
    os.getenv("CALNEDAR_GR3"),
    None,
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


def del_event(ggl_id_a: str, ggl_id_g: str, group: int):
    try:
        service = build("calendar", "v3", credentials=get_credentials())

        _ = service.events().delete(calendarId="primary", eventId=ggl_id_a).execute()
        print("Succesfully deleted event from primary calendar")

        if group == 4:
            return

        _ = (
            service.events()
            .delete(calendarId=GROUPS[group], eventId=ggl_id_g)
            .execute()
        )

        print("Succesfully deleted event from group calendar")

    except HttpError as error:
        print("Err: ", error)


def upd_event(
    ggl_id_a: str, ggl_id_g: str, e_date: date, group: int, subject: str, desc: str
):
    try:
        service = build("calendar", "v3", credentials=get_credentials())

        # TODO: Add records that can be changed
        creds = [""]

        event_a = service.events().get(calendar="primary", eventId=ggl_id_a).execute()

        b_event = event_gen(desc, group, subject, e_date)

        for cred in creds:
            event_a[cred] = b_event[cred]

        if (
            service.events()
            .update(calendarId="primary", eventId=event_a["id"], body=event_a)
            .execute()
        ):
            print("Updated event succesfully in primary calendar")

        if group == 4:
            return

        event_g = (
            service.events().get(calendar=GROUPS[group], eventId=ggl_id_a).execute()
        )

        b_event = event_gen(desc, group, subject, e_date)

        for cred in creds:
            event_g[cred] = b_event[cred]

        if (
            service.events()
            .update(calendarId=GROUPS[group], eventId=event_g["id"], body=event_g)
            .execute()
        ):
            print("Updated event succesfully in group calendar")

    except HttpError as error:
        print("Err: ", error)


def create_event(e_date: date, group: int, subject: str, desc: str):
    try:
        service = build("calendar", "v3", credentials=get_credentials())

        b_event = event_gen(desc, group, subject, e_date)
        print("event: ", b_event)

        event_a = service.events().insert(calendarId="primary", body=b_event).execute()
        if group == 4:
            return str(event_a["id"]), ""
        event_g = (
            service.events().insert(calendarId=GROUPS[group], body=b_event).execute()
        )

        print("Events: ", event_a, event_g)

        return str(event_a["id"]), str(event_g["id"])
    except HttpError as error:
        print("Err: ", error)
        return "", ""
    except RefreshError as error:
        print("Error:", error)
        return "", ""


def main(): ...


if __name__ == "__main__":
    ...
