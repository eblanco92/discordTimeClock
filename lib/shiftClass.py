from config.secret_credentials import sheetName, hoursOfBonus
from lib.sheetsFunctions import refresh, initializeSheet, findColumnToWrite, gsheetcreds
from lib.timegen import timeNow
from localization.channel_names import channelNames
from localization.message_translations import translations

global inFrame, employees, dummy
inFrame, employees, sheet, dummy = initializeSheet(sheetName)


class Shift:

    @classmethod
    def login(cls, online, channel):
        """
        Executed when the user wants to start working.
        :param online: list containing a keyword match boolean and the author's username
        :param channel: Discord channel where the request was received
        :return: Discord message
        """
        author = online[2]
        refresh(author, sheetName)

        # Resets the shift by setting it equal to the dummy dataFrame. Only happens in the beginning since the worker
        # can only check in once a day.
        inFrame[author] = dummy
        inFrame[author][0] = online[1]

        # boolean checked in
        # 5 CheckedIn     Boolean
        inFrame[author][5] = True
        mssg = author + ' ' + translations['checkedInMessage'] + timeNow()

        # This is defined as an emergency channel. If a worker logs in here, he will get a bonus.
        if channel == channelNames['emergencyLogin']:
            mssg = mssg + author + translations['emergencyWelcome']
            # 9 Emergency condition
            inFrame[author][9] = True
            return mssg
        else:
            return mssg

    @classmethod
    def takeABreak(cls, break_):
        """
        Executed when the user wants to take a break.
        :param break_: list containing a keyword match boolean and the author's username
        :return: Discord message
        """
        author = break_[2]
        refresh(author, sheetName)
        inFrame[author][3] = break_[1]
        msg = author + ' ' + translations['outForLunchMessage'] + ' ' + translations['timeNow']

        # boolean break start
        # 7 Breaktaken   Boolean
        inFrame[author][7] = True

        # Throws an error message in case the worker tries to go to break without being logged in
        if not inFrame[author][5]:
            # 5 CheckedIn     Boolean
            return translations['outForLunchError']
        else:
            return msg

    @classmethod
    def returnFromBreak(cls, breakReturn):
        """
        Executed when the user wants to resume working after a break.
        :param breakReturn: list containing a keyword match boolean and the author's username
        :return: Discord message
        """
        author = breakReturn[2]
        refresh(author, sheetName)
        inFrame[author][4] = breakReturn[1]
        # Calculates break duration in minutes
        breakDuration = ((inFrame[author][4] - inFrame[author][3]) / 60)

        msg = (author + ' ' + translations['returnFromBreak'] + str(breakDuration) + translations['minutes'] +
               translations['timeNow'])

        # boolean break end
        # 8 Breakreturned Boolean
        inFrame[author][8] = True

        if not inFrame[author][5]:
            # 6 CheckedIn     Boolean
            return translations['notLoggedInError']

        elif not inFrame[author][7]:
            # 7 Breaktakenn   Boolean
            return translations['returnFromBreakError']

        else:
            return msg

    @classmethod
    def logOut(cls, offline, sheetName):
        """
        Used to log out the worker. It writes in the Google sheet the worker's shift duration.
        :param offline: list containing a keyword match boolean and the author's username
        :param sheetName: Google sheet name that will be updated
        :return: Discord message
        """
        sheet = gsheetcreds(sheetName)
        bonus = False
        author = offline[2]
        inFrame[author][1] = offline[1]

        # Calculates the session's duration:
        inFrame[author][2] = inFrame[author][1] - inFrame[author][0]

        column, row, hour = findColumnToWrite(author)
        sessionDuration = 0.0
        msg = 'error'
        try:
            # first condition is when agent took a break
            if inFrame[author][5]:
                if inFrame[author][7] and inFrame[author][8]:
                    # Calculate session duration in hours
                    sessionDuration = str(((inFrame[author][2] - (inFrame[author][4] - inFrame[author][3])) / 3600))
                # second condition is when agent did not take a break
                else:
                    if inFrame[author][9]:
                        bonus = True
                        bonusMessage = translations['logOutBonusMessage']
                        # await message.channel.send(translations['logOutBonusMessage'])
                        inFrame[author][2] = inFrame[author][2] + (hoursOfBonus * 3600)
                        inFrame[author][9] = False

                    # Calculate session duration in hours
                    sessionDuration = str((inFrame[author][2] / 3600))
                msg = (author + translations['logOutMessage'] + sessionDuration + translations['hours'])
                if bonus:
                    msg = msg + ' ' + bonusMessage

            # If a worker finishes work at midnight, his shift should be logged in day -1

            if hour == '00':
                try:
                    hoursToUpdate = float(sheet.cell(row, column).value) + sessionDuration
                    sheet.update_cell(int(row) - 1, column, hoursToUpdate)
                    inFrame[author][5] = True
                except Exception as e:
                    print(e)
                    hoursToUpdate = sessionDuration
                    sheet.update_cell(int(row) - 1, column, hoursToUpdate)
                    inFrame[author][5] = True
            # most cases midnight will be false
            elif hour != '00':
                try:
                    # Hours to update is used in case the worker had more than one shift already
                    hoursToUpdate = float(sheet.cell(row, column).value) + float(sessionDuration)
                    sheet.update_cell(row, column, hoursToUpdate)

                    inFrame[author][5] = True
                except Exception as e:
                    print(e)
                    hoursToUpdate = sessionDuration
                    sheet.update_cell(row, column, hoursToUpdate)
                    inFrame[author][5] = True

            # boolean checked out
            # 6 CheckedOut    Boolean

            inFrame[author][6] = True

            if not inFrame[author][5]:
                sheet.update_cell(row, column, 'WORKER ERROR')
                return translations['notLoggedInError']
            else:
                if inFrame[author][8] == False and inFrame[author][7] == True:
                    return translations['logOutWhileInBreakError']

                else:
                    return msg
                    # reset dataFrame Column after finishing the shift.
            inFrame[author] = dummy

        except Exception as e:
            print(e)
            # Catch all error
            notice = 'something went wrong ¯\_(ツ)_/¯ ' + str(e)
            return notice
