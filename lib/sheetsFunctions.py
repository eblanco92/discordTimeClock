from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas as pd
from config.secret_credentials import secretJsonFile, sheetName
import datetime

'''
The pdtemplate.csv csv contains the overall structure of a shift and each block's duration. 
index, variable name,  type, description:
0 Checkin       time  - Timestamp when worker logs in 
1 Checkout      time  - Timestamp when worker logs out
2 Duration      time  - Difference between Checkin and Checkout. If a break occurred, then it substracts break time
3 Break out     time  - Timestamp when worker goes for lunch
4 Break In      time  - Timestamp when worker comes back from lunch
5 CheckedIn     Boolean - Checkin condition, if worker is logged in, then True
6 CheckedOut    Boolean - Checkout condition, if worker finished his shift, then True
7 Breaktaken    Boolean - Break condition, if worker has taken a break then True
8 Breakreturned Boolean - Return from break condition, if worker has returned from his break, then True
9 Emergency     Boolean - Special condition given to workers who log in in a "special" channel, used for emergency since
                          it pays more.
'''
inFrame = pd.read_csv('config/pdtemplate.csv')
# Used to reset the shift data frame
dummy = [0, 0, 0, 0, 0, False, False, False, False, False]
# Used to give the bot write access to the Google sheet
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']


def gsheetcreds(sheetName):
    """
    Used to access the Google sheet and authenticate
    :param sheetName: Uses it to connect to the sheet
    :return: gspread sheet object
    """
    creds = ServiceAccountCredentials.from_json_keyfile_name(secretJsonFile, scope)
    excel = gspread.authorize(creds)
    sheet = excel.open(sheetName).sheet1
    return sheet


def calendarUpdate(sheet):
    """
    Writes a new day in the google sheet in case the day does not exist already. Requires A1 cell to have the =TODAY()
    function.
    :param sheet: gspread sheet object
    :return: nothing, just updates the Google sheet itself
    """
    today = sheet.acell('A1').value
    calendar = sheet.col_values(2)
    calLen = len(calendar)
    if today not in calendar:
        sheet.update_cell(calLen + 1, 2, today)


def findAuthor(sheet, author):
    """
    Takes the author of the discord message and tries to find in the google sheet. If the author is not there, it will
    create a pandas dataFrame in memory to match his discord username.

    :param sheet: gspread sheet object
    :param author: author of the discord message (username)
    :return: Nothing, it just updates the Google sheet in case the author does not exist in it.
    """
    try:
        sheet.find(author)
    except:
        employees = sheet.row_values(1)
        employeeCount = len(employees)
        sheet.update_cell(1, employeeCount + 1, author)
        inFrame[author] = dummy


def refresh(author, sheetName):
    """
    Utility function that refreshes google authentication credentials, updates the day list in the google sheet and finds
    the author of a message in there.
    :param author: author of the discord message (username)
    :param sheetName: Uses it to connect to the sheet
    :return: gspread sheet object
    """
    sheet = gsheetcreds(sheetName)
    calendarUpdate(sheet)
    findAuthor(sheet, author)
    return sheet


def initializeSheet(sheetName):
    """
    Function to initialize the google sheet. Only runs when the service starts.

    :param sheetName: Uses it to connect to the sheet
    :return: inFrame - data frame containing the shift values and statuses, employees - list of employees currently in
    the sheet, sheet - gspread sheet object, dummy - sample data frame column used to reset the shift when its over.
    """

    creds = ServiceAccountCredentials.from_json_keyfile_name(secretJsonFile, scope)
    excel = gspread.authorize(creds)
    sheet = excel.open(sheetName).sheet1
    employees = sheet.row_values(1)
    for employee in employees:
        inFrame[employee] = dummy
    return inFrame, employees, sheet, dummy


def findColumnToWrite(author):
    """
    Function to find which row and which column is to be updated in the google sheet. Changes daily
    :param author: author of the discord message (username)
    :return: column, row - location in the sheet where the shift duration is to be written , hour - current hour (00-23)
    """
    sheet = refresh(author, sheetName)
    today = sheet.acell('A1').value
    column = str(sheet.find(author)).split()[1].split('C')[1]
    row = str(sheet.findall(today)).split()[4].split('C')[0].split('R')[1]
    hour = str(datetime.datetime.now()).split()[1].split('.')[0].split(':')[0]
    return column, row, hour
