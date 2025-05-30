from discord.ext import commands
import discord
from discord import FFmpegPCMAudio
from discord import FFmpegAudio
from discord import FFmpegOpusAudio
import asyncio
import requests
import json
#import openai
from openai import OpenAI
#import spotipy
#from spotipy.oauth2 import SpotifyOAuth
#import webbrowser
from tube import download_vid,remove_all_files,delete_selected_file,find_music_by_title,playlist_titles,find_audio_by_title,downloadtranslation # pytube file
import os
from dotenv import load_dotenv
import queue
import copy
#import translate
from translate import Translator
import datetime

#ENV Variables

load_dotenv()
disc_token = os.getenv('TOKEN')
api = os.getenv('API')
client = OpenAI(api_key = api)


#Discord Intents

intents = discord.Intents.all()
intents.members = True
intents.message_content = True

### Bot and its Commands
bot = commands.Bot(command_prefix = "$", help_command=None, intents = intents) 
play_list = queue.Queue()

@bot.event
async def on_ready():
  try:
    #await bot.tree.sync(guild=bot.settings.GUILD_OBJECT)
    print('Discord bot sucessfully connected!')
  except:
    print('Could not connect to Discord.')

'''
#Test Commands
@bot.command()
async def test(ctx, title):
    test = find_music_by_title(title)
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
  #global current_downloads
  # if you are not in vc
  if not ctx.voice_client:
    #connect to vc
    print('Joining chat.')
    await join(ctx)
  if "playlist" in title:
    await play_list(ctx, title)
    exit
  print(title)
  #check if playing in voice chat
  if ctx.voice_client.is_playing():
    await add_to_queue(ctx, title)
    download_vid(title)
  else:
    download_vid(title)
    await play_song(ctx, title)
    

async def play_song(ctx, title):
  #voice_channel = ctx.author.voice.channel
  # if you are not in vc
  if not ctx.voice_client:
    #connect to vc
    print('Joining chat.')
    await join(ctx)
  try:
    async with ctx.typing():
      #executable part is where we downloaded ffmpeg. 
      #find_music_name func because we want to bot to play our desired song from the folder
      player = discord.FFmpegPCMAudio(executable="C:\\ffmpeg\\bin\\ffmpeg.exe",source=f"music/{find_music_by_title(title)}")
      ctx.voice_client.play(player, after=lambda e: print('Player error: %s" %e') if e else None)
    #send confirmation
    await ctx.send(f'Now playing: {find_music_by_title(title)}')
    while ctx.voice_client.is_playing():
      await asyncio.sleep(1)
    #delete the file after finished playing
    delete_selected_file(find_music_by_title(title))
    #TODO fix the way this goes to the next song. 
    if not play_list.empty():
      song = play_list.get()
      #await asyncio.sleep(10)
      print(song)
      await play(ctx, title=song)
    else:
      await ctx.send("End of song Queue! Good bye!") 
      await leave(ctx)
    
  except Exception as e :
    #sending error 
    #await ctx.send(f'Error: {e}') 
    print(f"Error: {e}")

@bot.command()
async def playlist(ctx, url):
  q = playlist_titles(url)
  print("Entering queueing loop.")
  for songs in range(q.qsize()):
    play_list.put(q.get())
  print("Checking if in VC.")
  if not ctx.voice_client:
    #connect to vc
    print('Joining chat.')
    await join(ctx)
  print("Checking if playing.")
  await ctx.send(f"{play_list.qsize()} songs in the queue!") 
  if not ctx.voice_client.is_playing():
    print("Download video.")
    song = play_list.get()
    download_vid(song)
    print("Play the song.")
    await play_song(ctx, song)
  

def merge_queue(q):
  while not q.empty():
    #Get all in queue from other queue and put it in play_list queue
    play_list.put(q.get())
  
async def play_from_queue(ctx):
  if not play_list.empty():
    await play_song(ctx, play_list.get())
  else:
    await ctx.send("End of song Queue! Good bye!") 
    leave()
    
async def download_queue():
  play_list_copy = copy.deepcopy(play_list)
  for i in range(5):
    if play_list_copy.empty():
      break
    download_vid(play_list_copy.get())

@bot.command()
async def skip(ctx):
  if not play_list.empty():
    ctx.voice_client.stop()
    await play_song(ctx, play_list.get())
  else:
    await ctx.send("End of song Queue! Good bye!") 
    await leave(ctx)

@bot.command()
async def add_to_queue(ctx, title):
  play_list.put(title)
  await ctx.send(f"{play_list.qsize()} songs in the queue!") 
  
@bot.command()
async def meme(ctx):
  response = requests.get('https://meme-api.com/gimme/')
  json_data = json.loads(response.text)
  #return json_data['url']
  await ctx.send(json_data['url'])  
  
@bot.command()
async def ask(ctx, *, question):
  response = client.completions.create(
    model = 'gpt-3.5-turbo-instruct',
    prompt = question,
    max_tokens = 300,
    temperature = 0.3
  )
  await ctx.send(response.choices[0].text) 

#Text to spanish and then spanish audio
@bot.command()
async def tospanish(ctx, *, text):
  translator = Translator(to_lang='es')
  translation = translator.translate(text)
  print(translation)
  await ctx.send(translation)
  await translate_to_audio(ctx, text=translation)

async def translate_to_audio(ctx, *, text):
  time = datetime.datetime.now()
  mp3_file = f'{time.strftime("%Y-%m-%d-%H-%M-%S")}_output.mp3'
  downloadtranslation(mp3_file=mp3_file, trans=text)
  await play_audio(ctx=ctx, path=mp3_file)

async def play_audio(ctx, path):
  if not ctx.voice_client:
    #connect to vc
    print('Joining chat.')
    await join(ctx)
  if ctx.voice_client.is_playing():
    await ctx.send(f'Audio translation not available while Audio Activity is in use.')
  else:
    try:
      async with ctx.typing():
        #executable part is where we downloaded ffmpeg. 
        #find_music_name func because we want to bot to play our desired song from the folder
        player = discord.FFmpegPCMAudio(executable="C:\\ffmpeg\\bin\\ffmpeg.exe",source=f"{path}")
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s" %e') if e else None)
      while ctx.voice_client.is_playing():
        await asyncio.sleep(1)
      #delete the file after finished playing
      delete_selected_file(path)
      await ctx.send("End of translation! Goodbye!\nFin de la traducción. ¡Adiós!") 
      await leave(ctx)
    
    except Exception as e :
      #sending error 
      #await ctx.send(f'Error: {e}') 
      print(f"Error: {e}")
    
bot.run(disc_token)
    
#client = MyClient(intents=intents)
#client.run(spot_token) # Replace with your own token.