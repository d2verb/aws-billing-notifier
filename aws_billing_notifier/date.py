import datetime

def today():
    return datetime.datetime.today()

def prevday(dt):
    return dt - datetime.timedelta(days=1)

def yesterday():
    return prevday(today())

def beginning_of_month(dt):
    return dt.replace(day=1)