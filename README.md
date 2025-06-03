A bot created for Discord. 

Currently you need to register the bot through discord before using it. 

It usues Youtube to play music. The queue works but currently cannot play playlists.

Commands:
```
$join
```
```
$play <title>
```
```
$skip
```
```
$stop
```
```
$resume
```
```
$pause
```
```
$leave
```
```
$meme
``` 
---- $meme will post a random meme
```
$ask "Prompt"
```
---- $ask will return an openai answer to the prompt given.

Currently, it works by downloading the songs from the queue as they go. The issue with that is that its slow. If I can download the songs as I put them in the queue instead of right before they play, then it'll be much faster.

This new build should have the following:
1. Ability to queue and download ✅
2. take playlists but only download a section of them to keep down on space.✅
4. figure out how environment secrets work through github.\
   a. Still havent figured it out. Any help would be greatly apprectiated.\
5. Impliment OpenAI ✅\
6. Ability to translate to Spanish\
  a. Text\ ✅
  b. Audio (Real Time)\ 

<b>Install instructions:</b> \
Program installs:\
Install the following programs on the computer/server you intend to run the bot from
1. You will need at least Python3
2. You will need FFMPEG (this will be the audio player)\
   a. Install here: https://ffmpeg.org/download.html#build-windows \
   b. Install FFMPEG in C:\ffmpeg

Python libraries needed:
1. discord
2. asyncio
3. json
4. requests
5. openai
6. dotenv
7. queue
8. copy
9. pytubefix

Configuration:
1. Discord Token\
   a. Go to https://discord.com/developers/docs/intro \
   b. Login or Create an account \
   c. Go to Applications -> New Application \
   d. After you create it go to the Bot tab \
   e. Add a bot \
   f. Select Reset Token \
   g. Copy the Token \
   h. Open the Discordbot project on a code editor and create an .env file \
   i. Create a variable names TOKEN and paste the token from discord \
2. OpenAI Token\
   a. Go to https://www.openai.com and sign up for an OpenAI account. \
   b. After you've created an account, click on your profile picture on the top right, then click "View API keys" to access your API key. \
   c. In the .env file create a variable named API and paste the the api token \

<b>Run instructions</b>
Run bot.py in python3 or terminal with:
```& <Python3 path> <path to bot file>/bot.py``` \
for my environment its ```& C:/Python313/python.exe c:/Users/<personal stuff>/DiscordBot-1/bot.py```
