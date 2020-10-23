# discordTimeClock
Allows you to invite a bot into your discord server so your remote workers or freelancers can log the time they spent in your project. This information will be readily available in a Google Sheet so you can perform other operations with their hours (such as calculating salaries and payrolls)
The bot takes each worker's username and writes how long they spent in the project everyday.

### Join the test Discord server!
https://discord.gg/Vk7YTh
- There you can try out the discord bot
- You can ask how to use and implement the bot on your own


## Setup

- You will need to first setup a Google service account and enable its usage for Google Drive and Google Sheets
- Get the JSON that is used for authentication, download and place in this project's /config
  https://cloud.google.com/iam/docs/creating-managing-service-account-keys
- Create a Google Sheet in which your worker's shifts are going to be logged. Note that the A1 cell is reserved for the =today() function
  Example: https://cloud.google.com/iam/docs/creating-managing-service-account-keys
- From the secret JSON file, you need to get your app's email will be something like this:
  "client_email": "your-app-name.iam.gserviceaccount.com",
- Then go to your Google sheet and click on the share button and paste the your app's email, and give it editing rights to it
- Create a Discord server in which your bot and workers are going to interact (join the Discord server above for an example) 
  Create a Discord bot tutorial https://discordpy.readthedocs.io/en/latest/discord.html
- Go to Discord's developers website and create a Bot, name it whatever you want and get the Bot's secret key.
  Example: https://snipboard.io/LHKuTh.jpg
- Invite your bot to your server
- In the /config/secret_credentials.py file, enter your Discord app's secret, your google sheet's name (needs to be exactly as the title) and the exact name of the JSON file from the Google App
- (Optional) Modify the translations file so you can customize the messages and language the bot uses to communicate with your workers. 
- Finally, deploy this app to any hosting service of your choice (Heroku is not a good option since it restarts daily)
- Now you can invite your workers to the Discord server, instruct them on how to use it and forget about counting the hours they have worked as they will be logged for you.
