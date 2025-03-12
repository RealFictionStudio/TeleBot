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
            "CREATE TABLE IF NOT EXISTS event(id INEGER PRIMARY KEY, date text, e_group int, subject text, desc text, ggl_id_a int UNIQUE, ggl_id_g int UNIQUE)"
        )


def add_event(
    ggl_id_a: int, ggl_id_g: int, e_date: date, group: int, subject: str, desc: str
):
    with sqlite3.connect("calendar.db") as con:
        cur = con.cursor()

        _ = cur.execute(
            "INSERT INTO event VALUES (,?,?,?,?,?,?)",
            (e_date, group, subject, desc, ggl_id_a, ggl_id_g),
        )
        con.commit()


def del_event(event_id: int):
    with sqlite3.connect("calendar.db") as con:
        cur = con.cursor()

        event: tuple[int, int] = cur.execute(
            'SELECT ggl_id_a AS "a_id [int]", ggl_id_g "g_id [int]" FROM event WHERE id=?',
            (event_id,),
        ).fetchall()[0]

        _ = cur.execute("DELETE FROM event WHERE id=?", (event_id,))
        con.commit()
        return event


def upd_event(
    event_id: int, e_date: date | None, subject: str | None, desc: str | None
):
    # Add functionality to something depending on given inputs
    with sqlite3.connect("calendar.db") as con:
        cur = con.cursor()
        _ = cur.execute(
            "UPDATE event SET desc = ? ,date = ?, subject = ? WHERE id=?",
            (desc, e_date, subject, event_id),
        )

        event: tuple[int, int] = cur.execute(
            'SELECT ggl_id_a AS "a_id [int]", ggl_id_g "g_id [int]" FROM event WHERE id=?',
            (event_id,),
        ).fetchall()[0]

        con.commit()
        return event


def get_events():
    with sqlite3.connect("calendar.db") as con:
        cur = con.cursor()
        event: tuple[int, str, int, str, str]
        for event in cur.execute(
            'SELECT id AS "event_id [int]", date AS "date [date]", e_group AS "group [int]", subject, desc FROM event'
        ).fetchall():
            e_date = event[1].split("-")
            e_date.reverse()
            yield [str(event[0]), e_date, str(event[2]), event[3], event[4]]


if __name__ == "__main__":
    initialize_database(True)
    # add_event(date.today(), "1", "PRM2", "Kolokwium")
    # add_event(date.today(), "2", "PRM2", "Kolokwium")
    # add_event(date.today(), "3", "PRM2", "Śmierć")

    for event in get_events():
        print(event)
