import dotenv
from dotenv import load_dotenv
import os
import time

clear = lambda: os.system('cls')

dotenv_file = dotenv.find_dotenv()


print("Welcome to the Heimerdinger-bot-setup!")
print("This guide runs you trough every step you need to take in order to activate this bot on your server!")
print("DISCLAIMER: read through every step carefully because this setup can be quite complicated")
print("My bot's main feature is the live feed - use it to automatically send a message with details to a discord channel if someone finnishes a match")
input("press any key to start the setup")
clear()




print("STEP 1: Let the bot join your server")

print("")
print("[1] head over to 'https://discord.com/developers/applications' and log in with your discord account (admin account of the server)")

print("")
print("[2] click the button 'New Application' in the top right corner")

print("")
print("[3] enter a name for your application (this will not be the name of your bot!)")

print("")
print("[4] on the left side, navigate to 'Bot' and click on 'Add Bot' on the right side of your screen")

print("")
print("[5] if you want to change the username of your bot (right now it should be the name of your application) (btw. in this menu you can change the outward appearance of your bot")

print("")
print("[6] click on 'OAuth2' in the left menu")

print("")
print("[7] in 'Scopes' select 'bot'. Then select 'Administrator' in 'BOT PERMISSIONS'")
 
print("")
print("[8] now copy the link at the end of 'SCOPES' and paste it into your browser")
 
print("")
print("[9] follow the steps until the green checkmark appears. You can now close all windows!")
 
print("")
print("[10] head over to your discord server and check if your bot appears in the member list")
 
print("")

input("press any key to start STEP 2: YOUR DISCORD TOKEN")
clear()

print("STEP 2: YOUR DISCORD TOKEN")
 
print("")
print("[1] head over to 'https://discord.com/developers/applications' and log in with your discord account (admin account of the server)")
 
print("")
print("[2] select the application you created in STEP 1")
 
print("")
print("[3] select the 'Bot' menu and click on the blue 'Copy' button in the 'TOKEN' sector")
 
print("")
discord_token = input("[4] please paste [CTRL + V]  your discord token and confirm with ENTER:")
 
print("")

input("press any key to start STEP 3: YOUR DISCORD SERVER NAME")
clear()

print("STEP 3: YOUR DISCORD SERVER NAME")
 
print("")
discord_name = input("enter your discord server/guild name:")
 
print("")

input("press any key to start STEP 4: CHANNEL ID")
clear()

print("STEP 4: CHANNEL ID")
 
print("")
print("[1] in your discord settings in 'Appearance' activate 'Developer Mode'")
 
print("")
print("[2] now create a text channel on your discord server in which you want your bot to send the messages of your live-feed")
 
print("")
print("[3] right click the channel and select 'Copy ID'")
 
print("")
discord_channel = input("[4] please paste [CTRL + V]  your channel ID and confirm with ENTER:")
 
print("")

input("press any key to start STEP 5: RIOT API KEY AND REGION")
clear()

print("STEP 5: RIOT API KEY AND REGION")
 
print("")
print("[1] head over to 'https://developer.riotgames.com/' and log in with your riot (league of legends) account")
 
print("")
print("[2] click the button 'GENERATE API KEY' at the bottom of your profile (https://developer.riotgames.com)")
 
print("")
print("[3] click 'Copy' on the right side of your api key (should be crypted, like passwords)")
 
print("")
print("[4] DISCLAIMER: your riot api key will only last 24 hours until you need to generate a new one. If you dont want to generate a new one click of 'Register Product' --> 'Personal Api Key'. This will take some time but if your request is checked you will get an 24/7 api key! If you dont want to do that you can simply change your api key with the api_key.exe")
 
print("")
riot_key = input("[5] please paste [CTRL + V]  your riot api key and confirm with ENTER:")
 
print("")
riot_region = input("[6] please enter your region (for euw enter euw1, for na enter na1):")
 
print("")

input("press any key to finish your bot setup")
clear()

print("Great! Now we are finished with setting up your bot")
time.sleep(2)
print("If you want to start your bot click on the .py script or execute the .exe")
time.sleep(2)
print("DISCLAIMER: your bot will only run while one of those programs is running")
time.sleep(2)
print("I also provided data for hosting with heroku.com --> if you want to know how to host with heroku --> there are many youtube tutorials for that!")
time.sleep(2)
print("You can change any data you inserted in this setup in your .env file. Just open it with notepad and change the values")
time.sleep(2)
input("press any key to exit. Run your heimerdinger-bot.exe file in order to start up your bot --> try !tutorial command in any channel for further instructions")
clear()

dotenv.set_key(dotenv_file, "DISCORD_TOKEN", discord_token)
dotenv.set_key(dotenv_file, "DISCORD_GUILD", discord_name)
dotenv.set_key(dotenv_file, "LIVE_FEED_CHANNEL_ID", discord_channel)
dotenv.set_key(dotenv_file, "TIME_IN_SECONDS", "60")
dotenv.set_key(dotenv_file, "RIOT_API_KEY", riot_key)
dotenv.set_key(dotenv_file, "RIOT_API_REGION", riot_region)


