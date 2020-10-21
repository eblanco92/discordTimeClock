"""
This file contains all the secret credentials you need to make the bot work,
make sure you have all of them ready before deploying the project.

Check the project out working in the demo sheet:
https://docs.google.com/spreadsheets/d/1X3Gj9u3JRp88tSA4hafcs-SYGWj4YoLCp1AReIzFYso/edit?usp=sharing
"""

'''
You can obtain it from discord itself whenever you create a bot with them.
Under Bot tab you will find the discord secret
https://discord.com/developers/applications/
'''
discordSecret = ''

'''
This is the name of the google sheet where you want your data to be stored.
'''
sheetName = 'Check-in bot test sheet'

'''
This is the name of the json file you obtain from the google cloud platform, it is used to authorize the app
to read and write in your sheets.
It should look something like this:
{
  "type": "service_account",
  "project_id": "",
  "private_key_id": "",
  "private_key": "-----BEGIN PRIVATE KEY----------END PRIVATE KEY-----\n",
  "client_email": ".iam.gserviceaccount.com",
  "client_id": "",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": ""
}
'''

secretJsonFile = 'config/' + 'checker_secret.json'

'''
This is how much more a worker will be given as a bonus if he logs in outside of his shift
'''

hoursOfBonus = 0.5
