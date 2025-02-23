from datetime import date
from db_handler.manager import *


def test_database():
    initialize_database(reset=True)
    add_event(date(2025, 1, 12), 1, "PRM", "Kol 1")
    add_event(date(2024, 12, 29), 2, "ANL", "Kol 1")
    add_event(date(2025, 3, 30), 3, "PSYG", "Kol 1")

    for event in get_events():
        print(event)


if __name__ == "__main__":
    test_database()
