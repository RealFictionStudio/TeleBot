from datetime import date
from db_handler import manager


def test_database():
    db = manager.manager()
    db.add_event(date(1, 1, 1), 1, "PRM", "Kol 1")
    db.add_event(date(2, 2, 2), 2, "ANL", "Kol 1")
    db.add_event(date(3, 3, 3), 3, "PSYG", "Kol 1")

    for event in db.get_events():
        print(event)


if __name__ == "__main__":
    test_database()
