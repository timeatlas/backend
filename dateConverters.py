import datetime


def cf(date):
    year = date.year
    if year > 7000:
        year -= 7000
    else:
        year -= 7001
    return (year, date.month, date.day)

def ct(date):
    year = date[0]
    if year > 0:
        year += 7000
    else:
        year += 7001
    return datetime.date(year, date[1], date[2])

def dateCheck(year, month, day):
    try:
        datetime.date(abs(year), month, date):
    except ValueError:
        return False
    return True
