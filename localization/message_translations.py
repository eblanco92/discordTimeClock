from lib.timegen import timeNow
"""
Just a dictionary containing all the possible bot responses, change any that you want to modify the tone of voice.
"""
translations = {
    'incorrectKeyword': " I don't understand you, the keyword you used is invalid. Here are some tips: ",
    'usageScreenShot': 'https://i.snipboard.io/6mwv4q.jpg',
    'usageScreenShot2': 'https://i.snipboard.io/SvZTOB.jpg',
    'checkedInMessage': ' I register your check in at: ',
    'emergencyWelcome': ' Thanks for spending extra time!',
    'outForLunchMessage': 'Enjoy your lunch!',
    'outForLunchError': 'Your break request could not be processed, it seems you forgot to check in at the beginning '
                        'of your shift',
    'timeNow': ' It is now ' + timeNow(),
    'returnFromBreak': ' I register that you are back from your break you took: ',
    'minutes': ' minutes',
    'returnFromBreakError': 'Your return from break request could not be processed, it seems you forgot to '
                            'inform of your break ',
    'notLoggedInError': 'Your request could not be processed, it seems you forgot to login at the beginning of your'
                        ' shift',
    'logOutBonusMessage': ' Thanks for taking the time to help outside your shift',
    'logOutMessage': ' I register your logout request. You worked for: ',
    'hours': ' hours',
    'logOutWhileInBreakError':'You cannot logout while in a break'

}
