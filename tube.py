from pytubefix import Search
from pytubefix import YouTube
from pytubefix import Playlist
from pytubefix.cli import on_progress
import os
import shutil #import libs
import queue
from gtts import gTTS
# We are finding the addresses of the vids that we want to find and then downloading them.

dic=('afrikaans', 'af', 'albanian', 'sq', 'amharic', 'am', 
     'arabic', 'ar', 'armenian', 'hy', 'azerbaijani', 'az',
 'basque', 'eu', 'belarusian', 'be', 'bengali', 'bn', 'bosnian',
     'bs', 'bulgarian', 'bg', 'catalan', 'ca',
  'cebuano', 'ceb', 'chichewa', 'ny', 'chinese (simplified)',
     'zh-cn', 'chinese (traditional)', 'zh-tw',
  'corsican', 'co', 'croatian', 'hr', 'czech', 'cs', 'danish',
     'da', 'dutch', 'nl', 'english', 'en', 'esperanto',
  'eo', 'estonian', 'et', 'filipino', 'tl', 'finnish', 'fi', 
     'french', 'fr', 'frisian', 'fy', 'galician', 'gl',
  'georgian', 'ka', 'german', 'de', 'greek', 'el', 'gujarati', 
     'gu', 'haitian creole', 'ht', 'hausa', 'ha', 
  'hawaiian', 'haw', 'hebrew', 'he', 'hindi', 'hi', 'hmong', 
     'hmn', 'hungarian', 'hu', 'icelandic', 'is', 'igbo',
  'ig', 'indonesian', 'id', 'irish', 'ga', 'italian', 'it', 
     'japanese', 'ja', 'javanese', 'jw', 'kannada', 'kn',
  'kazakh', 'kk', 'khmer', 'km', 'korean', 'ko', 'kurdish (kurmanji)',
     'ku', 'kyrgyz', 'ky', 'lao', 'lo', 
  'latin', 'la', 'latvian', 'lv', 'lithuanian', 'lt', 'luxembourgish',
     'lb', 'macedonian', 'mk', 'malagasy',
  'mg', 'malay', 'ms', 'malayalam', 'ml', 'maltese', 'mt', 'maori',
     'mi', 'marathi', 'mr', 'mongolian', 'mn',
  'myanmar (burmese)', 'my', 'nepali', 'ne', 'norwegian', 'no',
     'odia', 'or', 'pashto', 'ps', 'persian',
   'fa', 'polish', 'pl', 'portuguese', 'pt', 'punjabi', 'pa',
     'romanian', 'ro', 'russian', 'ru', 'samoan',
   'sm', 'scots gaelic', 'gd', 'serbian', 'sr', 'sesotho', 
     'st', 'shona', 'sn', 'sindhi', 'sd', 'sinhala',
   'si', 'slovak', 'sk', 'slovenian', 'sl', 'somali', 'so', 
     'spanish', 'es', 'sundanese', 'su', 
  'swahili', 'sw', 'swedish', 'sv', 'tajik', 'tg', 'tamil',
     'ta', 'telugu', 'te', 'thai', 'th', 'turkish', 'tr',
  'ukrainian', 'uk', 'urdu', 'ur', 'uyghur', 'ug', 'uzbek', 
     'uz', 'vietnamese', 'vi', 'welsh', 'cy', 'xhosa', 'xh',
  'yiddish', 'yi', 'yoruba', 'yo', 'zulu', 'zu')

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

def playlist_titles(url):
    pl = Playlist(url)
    q = queue.Queue()
    for video in pl.videos:
        print(video.title)
        q.put(video.title)
    return q
        
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

#find downloaded translated audio
def find_audio_by_title(text):
    return text + ".mp3"

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

def downloadtranslation(mp3_file, trans):
  tts = gTTS(text=trans, lang='es', slow=False)
  tts.save(mp3_file)
  
