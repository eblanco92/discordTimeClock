import datetime

def timeNow():
    now = str(
        datetime.datetime.now()).split()[1].split('.')[0]
    return now