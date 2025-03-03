from datetime import date


def parse_date(s_date: str):
    d_date = None
    sep = filter(lambda x: x in s_date, ["-", "/", ":"]).__next__()
    my_date = [int(i) for i in s_date.split(sep)]
    try:
        d_date = date(*my_date)
    except:
        print("Wrong string given")
    finally:
        return d_date
