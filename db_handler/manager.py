from datetime import date
import sqlite3
from typing import final


def initialize_database(): ...
def add_event():
    with sqlite3.connect("calendar.db"):
        pass


def del_event(): ...
def upd_event(): ...
def get_events(): ...


@final
class manager:
    def __init__(self):
        self.con = sqlite3.connect(
            "calendar.db", sqlite3.PARSE_DECLTYPES, sqlite3.PARSE_COLNAMES
        )
        self.cur = self.con.cursor()
        _ = self.cur.execute(
            "CREATE TABLE IF NOT EXISTS event(date text, e_grupa integer, subject text, desc text)"
        )

    def add_event(self, date: date, group: int, subject: str, desc: str):
        _ = self.cur.execute(
            "INSERT INTO event VALUES (?,?,?,?)", (date, group, subject, desc)
        )
        self.con.commit()

    def updt_event(self, date: date, group: int, subject: str, desc: str):
        _ = self.cur.execute(
            "UPDATE event SET desc = ? WHERE date = ? AND e_group = ? AND subject = ?",
            (desc, date, group, subject),
        )
        self.con.commit()

    def del_event(self, date: date, group: int, subject: str):
        _ = self.cur.execute(
            "DELETE FROM event WHERE date = ? AND e_group = ? AND subject = ?",
            (date, group, subject),
        )
        self.con.commit()

    def get_events(self):
        for event in self.cur.execute(
            'SELECT date AS "date [date]", e_group AS "group [integer]", subject, desc FROM event'
        ).fetchall():
            yield f"{event[3]} {event[2]} gr. {event[1]} dzień: {event[0].strftime('%d-%m-%Y')}"
