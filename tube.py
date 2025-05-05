from pytubefix import Search
from pytubefix import YouTube
import os
import shutil #import libs
import queue
# We are finding the addresses of the vids that we want to find and then downloading them.

#Finding the IDs for the videos we want to find
def give_link(name): 
    s = Search(f"{name}")
    yt_id = s.results #a list of yt vids
    video_ids = [video.video_id for video in yt_id] # scrapin the data that we want
    video_id = video_ids[0] # get the first video
    base_url = f"https://youtube.com/watch?v={video_id}" #yt link
    #print(base_url)
    return base_url

def download_vid(name):
    base_url = give_link(name)
    #print(base_url)
    #put the link into youtube
    yt = YouTube(base_url)
    #gets a list of audio, but we choose to use the first result instead in mp4.
    yt.title = name
    audio_stream = yt.streams.filter(only_audio=True, file_extension="mp4").first() #only download the first result
    audio_stream.download(output_path="music") # we are deciding where we want to install

    print(yt.title + " has been successfully downloaded.")
    
'''
def play_test():
    print('Playtest')
    try:
        YouTube('https://youtu.be/2lAe1cqCOXo').streams.first().download()
        print('YouTube link downloaded')
        yt = YouTube('http://youtube.com/watch?v=2lAe1cqCOXo')
        print(f'yt = {yt}')
        yt.streams.filter(only_audio=True, file_extension="mp4").first()
    except Exception as e:
        print(f"An error occurred: {e}")
'''

def add_to_queue(name):
    print(f"Adding to {name} to the queue.")
        
    
#remove the directory labled music
def delete_audio():
    shutil.rmtree("music")

#find the first files in the directory "music"
def find_music_name():
    print(str(os.listdir("music")[0]))
    return (str(os.listdir("music")[0]))

#find music by title
def find_music_by_title(song):
    return song + ".m4a"

#remove all in the queue (directory)
def remove_all_files(dir):
    for file in os.listdir(dir):
        os.remove(os.path.join(dir, file))
        
#delete file
def delete_selected_file(name):
    #directory = f"C:\\Users\\Bryce\\PythonProjects\\DiscordBot\\music\\{name}"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    music_dir = current_dir + "\\music\\" + name
    #print(music_dir)
    try:
        os.remove(music_dir)
    except Exception as e:
        print(e)
