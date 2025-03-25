from datetime import date
from db_handler.manager import *
from google_handler.manager import main as g_main


def test_database():
    initialize_database(reset=True)

    list_of_events = [
        (date(2025, 1, 12), 1, "PRM", "Kol 1"),
        (date(2024, 12, 29), 2, "ANL", "Kol 1"),
        (date(2025, 3, 30), 3, "PSYG", "Kol 1"),
    ]
    g = []

    for i in list_of_events:
        add_event(*i)
        _ = g.append(f"{i[3]} {i[2]} gr. {i[1]} dzień: {i[0].strftime('%d-%m-%Y')}")

    for event in get_events():
        assert event in g


def test_google_api():
    g_main()


if __name__ == "__main__":
    test_google_api()
    print("test")
    # test_database()
    pass
