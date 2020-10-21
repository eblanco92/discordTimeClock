import time as t

"""
Checks if a keyword is contained within a message. Returns a true if the keyword is in the message, a timestamp and 
the author of the message.
"""


def msgCondition(keywords, message):
    check = False
    timeStamp = None
    author = None
    for word in keywords:
        if word in message.content:
            check = True
    if check:
        author = str(message.author.name)
        timeStamp = t.time()
    return check, timeStamp, author
