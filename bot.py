from discord.ext import commands
import discord
from discord import FFmpegPCMAudio
from discord import FFmpegAudio
from discord import FFmpegOpusAudio
import logging
import asyncio
import requests
import json
#import spotipy
#from spotipy.oauth2 import SpotifyOAuth
#import webbrowser
from tube import give_link,download_vid,find_music_name,remove_all_files,delete_selected_file # pytube file
import os
from dotenv import load_dotenv
import queue
import copy

#ENV Variables

load_dotenv()
disc_token = os.getenv('TOKEN')

intents = discord.Intents.all()
intents.members = True
intents.message_content = True

### Bot and its Commands
bot = commands.Bot(command_prefix = "$", help_command=None, intents = intents) 
play_list = queue.Queue()
current_downloads = 0

@bot.event
async def on_ready():
  try:
    #await bot.tree.sync(guild=bot.settings.GUILD_OBJECT)
    print('Discord bot sucessfully connected!')
  except:
    print('Could not connect to Discord.')


''' Test Commands
@bot.command()
async def test(ctx):
    voice_channel = ctx.author.voice.channel
    print(voice_channel)
    voice_channel = await voice_channel.connect()

@bot.command()
async def pl_test(ctx):
  print('Trying to get the voice channel the author is in.')
  voice_channel = ctx.author.voice.channel
  print(f'Author channel is: {voice_channel}')
  # if you are not in vc
  if not ctx.voice_client:
    #connect to vc
    print('Trying to connect to vc!')
    voice_channel = await voice_channel.connect()
  try:
    print('Trying the play test.')
    play_test()
  except Exception as e :
    #sending error 
    await ctx.send(f'Error: {e}') 
    
'''

@bot.command()
async def pause(ctx):
  #check if music is playing
  if ctx.voice_client and ctx.voice_client.is_playing(): 
    #if playing, then pause
    ctx.voice_client.pause()
    #send confirmation
    await ctx.send('Playback paused.') 
  else:
    #if you are not in voice chat, send an error notification
    await ctx.send('[-] An error occured: You have to be in voice channel to use this commmand') #if you are not in vc

@bot.command()
async def resume(ctx):
  #if music is already paused
  if ctx.voice_client and ctx.voice_client.is_paused():
    #resume the music
    ctx.voice_client.resume()
    #send confirmation on channel
    await ctx.send('Playback resumed.')
  else:
    #if you are not in voice chat, send an error notification
    await ctx.send('[-] An error occured: You have to be in voice channel to use this commmand')

@bot.command()
async def leave(ctx):
  # if you're in voice chat
  if ctx.voice_client:
    #disconnect bot from voice chat
    await ctx.guild.voice_client.disconnect() 
    #send confirmation
    await ctx.send("Left the voice channel.")
    asyncio.sleep(1)
    # Remove the queue
    remove_all_files("music")
  else:
    #if you are not in vc
    await ctx.send("[-] An Error occured: You have to be in a voice channel to run this command") 
    
@bot.command()
async def join(context):
  if context.author.voice:
    channel = context.message.author.voice.channel
    try:
      #connect to the channel
      await channel.connect()
    except:
      #if there is an error
      await context.send("[-] An error occured: Couldn't connect to the channel") 
  else:
    #if you are not in vc
    await context.send("[-] An Error occured: You have to be in a voice channel to run this command") 
    
@bot.command(name="play")
async def play(ctx, *, title):
  global current_downloads
  # if you are not in vc
  if not ctx.voice_client:
    #connect to vc
    print('Joining chat.')
    await join(ctx)
  if(current_downloads < 5):  
    download_vid(title)
    current_downloads += 1
  #check if playing in voice chat
  if ctx.voice_client.is_playing():
    await add_to_queue(ctx, title)
  else:
    await play_song(ctx)

async def play_song(ctx):
  global current_downloads
  #voice_channel = ctx.author.voice.channel
  # if you are not in vc
  if not ctx.voice_client:
    #connect to vc
    print('Joining chat.')
    await join(ctx)
  if current_downloads == 0:
    download_queue(play_list)
  try:
    async with ctx.typing():
      #executable part is where we downloaded ffmpeg. 
      #find_music_name func because we want to bot to play our desired song from the folder
      player = discord.FFmpegPCMAudio(executable="C:\\ffmpeg\\bin\\ffmpeg.exe",source=f"music/{find_music_name()}")
      ctx.voice_client.play(player, after=lambda e: print('Player error: %s" %e') if e else None)
    #send confirmation
    await ctx.send(f'Now playing: {find_music_name()}')
    #remove 1 from current downloads
    current_downloads -= 1
    if current_downloads < 5 and play_list.qsize() > 4:
      download_from_range(play_list)
    while ctx.voice_client.is_playing():
      await asyncio.sleep(1)
    #delete the file after finished playing
    delete_selected_file(find_music_name())
    #TODO fix the way this goes to the next song. 
    if not play_list.empty():
      song = play_list.get()
      print(song)
      await play_song(ctx)
    
  except Exception as e :
    #sending error 
    #await ctx.send(f'Error: {e}') 
    print(f"Error: {e}")

async def play_from_queue(ctx):
  if not play_list.empty():
    await play_song(ctx)
  else:
    await ctx.send("End of song Queue! Good bye!") 
    leave()
    
async def download_queue():
  play_list_copy = copy.deepcopy(play_list)
  for i in range(5):
    if play_list_copy.empty():
      break
    download_vid(play_list_copy.get())
    current_downloads += 1
    
async def download_from_range():
  #copy queue and convert to list
  play_list_copy = list(copy.deepcopy(play_list).queue)
  print(play_list_copy)
  #loop thorugh list to specific range ot download to specified amount
  if(play_list_copy.count > 4):
    for song in range[5]:
      print(song)
      if(song > current_downloads - 1):
        download_vid(play_list_copy[song])
        current_downloads += 1

@bot.command()
async def skip(ctx):
  if not play_list.empty():
    ctx.voice_client.stop()
    await play_song(ctx)
  else:
    await ctx.send("End of song Queue! Good bye!") 
    await leave(ctx)

'''    
@bot.command()
async def add_to_queue(ctx, title):
  play_list.put(title)
  await ctx.send(f"{play_list.qsize()} songs in the queue!") 
'''

@bot.command()
async def add_to_queue(ctx, title):
  global current_downloads
  play_list.put(title)
  download_vid(title)
  current_downloads += 1
  await ctx.send(f"{play_list.qsize()} songs in the queue!") 
  
@bot.command()
async def meme(ctx):
  response = requests.get('https://meme-api.com/gimme/')
  json_data = json.loads(response.text)
  #return json_data['url']
  await ctx.send(json_data['url'])  
    
bot.run(disc_token)
    
#client = MyClient(intents=intents)
#client.run(spot_token) # Replace with your own token.
