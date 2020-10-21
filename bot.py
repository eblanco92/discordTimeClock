import discord
from config.secret_credentials import discordSecret, sheetName
from config.checkin_keywords import keywordLogin, keywordBreak, keywordReturn, keywordOffline, AllKeywords
from lib.sheetsFunctions import initializeSheet
from lib.message_condition import msgCondition
from localization.channel_names import channelNames
from localization.message_translations import translations
from lib.shiftClass import Shift

# Initialize discord client
client = discord.Client()
# Declare globals so that they can be used by the shift class
# global sheet
inFrame, employees, sheet, dummy = initializeSheet(sheetName)

shift = Shift()


@client.event
async def on_ready():
    # Informs that discord client is connected to Discord.
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    # whenever message is in the check in channel and it is not in the keyword set
    if str(message.channel) == channelNames['checkInChannel']:
        validMessage = msgCondition(AllKeywords, message)
        if not validMessage[0]:
            if message.author.name != channelNames['botName']:
                await message.channel.send(str(message.author.name) + '  ' +
                                           translations['incorrectKeyword'] + '  ' +
                                           translations['usageScreenShot'] + '  ' +
                                           translations['usageScreenShot2']
                                           )
    # Checks that keyword is in the message
    online = msgCondition(keywordLogin, message)
    if online[0]:
        msg = shift.login(online, message.channel)
        await message.channel.send(msg)

    # break mechanism. Called 'break_' to avoid conflict with Python's native function.

    break_ = msgCondition(keywordBreak, message)
    if break_[0]:
        msg = shift.takeABreak(break_)
        await message.channel.send(msg)

    # return from break
    breakReturn = msgCondition(keywordReturn, message)
    # check, timeStamp, author
    if breakReturn[0]:
        msg = shift.returnFromBreak(breakReturn)
        await message.channel.send(msg)

    # offline mechanism

    offline = msgCondition(keywordOffline, message)
    # check, timeStamp, author
    if offline[0]:
        msg = shift.logOut(offline, sheetName)
        if msg is None:
            print('message is empty')
        await message.channel.send(msg)
        inFrame[offline[2]] = dummy


client.run(discordSecret)
