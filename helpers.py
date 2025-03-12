from datetime import date, timedelta
from db_handler.manager import get_events


def parse_date(s_date: str):
    d_date = None
    sep = filter(lambda x: x in s_date, ["-", "/", ":"]).__next__()
    try:
        my_date = [int(i) for i in s_date.split(sep)]
        d_date = date(*my_date)
    except ValueError as err:
        print("Wrong date given")
    finally:
        return d_date


def event_gen(desc: str, group: int, subject: str, e_date: date):
    return {
        # Template for date "%Y-%m-%dT%H:%M:%S.%fZ"
        "summary": f"{desc} z {subject}",
        "desctiption": f"Przedmiot: {subject}, Grupa: {group}, Opis: {desc}",
        "start": {
            "date": e_date.strftime("%Y-%m-%d"),
            "timeZone": "Europe/Warsaw",
        },
        "end": {
            "date": e_date.__add__(timedelta(days=1)).strftime("%Y-%m-%d"),
            "timeZone": "Europe/Warsaw",
        },
    }


def dc_msg_gen():
    msg = "Terminarz:\n"
    events = get_events()
    for event in events:
        msg += "\n" + ",".join(event)
    return msg
