from datetime import date
import sqlite3


def initialize_database(reset: bool = False):
    if reset:
        with sqlite3.connect("calendar.db") as con:
            _ = con.cursor().execute("DROP TABLE IF EXISTS event")

    with sqlite3.connect(
        "calendar.db", sqlite3.PARSE_DECLTYPES, sqlite3.PARSE_COLNAMES
    ) as con:
        cur = con.cursor()
        _ = cur.execute(
            "CREATE TABLE IF NOT EXISTS event(date text, e_group integer, subject text, desc text)"
        )


def add_event(e_date: date, group: int, subject: str, desc: str):
    with sqlite3.connect("calendar.db") as con:
        cur = con.cursor()
        _ = cur.execute(
            "INSERT INTO event VALUES (?,?,?,?)", (e_date, group, subject, desc)
        )
        con.commit()


def del_event(e_date: date, group: str, subject: str):
    with sqlite3.connect("calendar.db") as con:
        cur = con.cursor()
        _ = cur.execute(
            "DELETE FROM event WHERE date = ? AND e_group = ? AND subject = ?",
            (e_date, group, subject),
        )
        con.commit()


def upd_event(e_date: date, group: int, subject: str, desc: str):
    with sqlite3.connect("calendar.db") as con:
        cur = con.cursor()
        _ = cur.execute(
            "UPDATE event SET desc = ? WHERE date = ? AND e_group = ? AND subject = ?",
            (desc, e_date, group, subject),
        )
        con.commit()


def get_events():
    with sqlite3.connect("calendar.db") as con:
        cur = con.cursor()
        event: tuple[str, int, str, str]
        for event in cur.execute(
            'SELECT date AS "date [date]", e_group AS "group [integer]", subject, desc FROM event'
        ).fetchall():
            e_date = event[0].split("-")
            e_date.reverse()
            yield f"{event[3]} {event[2]} gr. {event[1]} dzień: {'-'.join(e_date)}"
