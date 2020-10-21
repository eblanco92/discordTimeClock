'''
These keywords are used throughout a worker's shift. You can replace them or add more.
They use any command in keywordLogin to indicate that they started to work.
Breaks are optional.
They use any command in keywordBreak to indicate that they went for a break. (only one break allowed per shift)
They use any command in keywordReturn to indicate that they returned from the break. (only one break allowed per shift)
They use any command in keywordLogin to indicate that they finished work for the day.
'''

keywordLogin = ['online!', 'Online!']
keywordBreak = ['break!', 'Break!']
keywordReturn = ['return!', 'Return!', 'Back!', 'back!']
keywordOffline = ['offline!', 'Offline!']
AllKeywords = keywordLogin + keywordBreak + keywordReturn + keywordOffline
