import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import time
import sys
from random import choice
import threading

song_start_time = 0
song_start_time_lock = threading.Lock()

settings = json.load(open("settings.json"))
apiKey = json.load(open("apiKey.json"))

auth_manger = SpotifyOAuth(scope=apiKey['scope'], username=settings['username'], client_id=apiKey['id'], client_secret=apiKey['secret'], redirect_uri=apiKey['redirect_uri'])
client = spotipy.Spotify(auth_manager=auth_manger)

current_playback = client.current_playback()
current_song = current_playback['item']
current_analysis = client.audio_analysis(current_song['id'])

class timeCheckerThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global song_start_time, song_start_time_lock
        while True:
            playback_pos = client.current_playback()['progress_ms']
            curr_ms = time.time_ns()/1000000
            start_time_temp = curr_ms - playback_pos
            song_start_time_lock.acquire()
            if song_start_time < start_time_temp or song_start_time == 0:
                song_start_time = start_time_temp
            song_start_time_lock.release()

timeChecker = timeCheckerThread()
timeChecker.start()

event_types = ['bars','beats','sections']
next_event = {}
event_lists = {}

for event_string in event_types:
    event_lists[event_string] = current_analysis[event_string]
    event_lists[event_string].reverse()
    next_event[event_string] = event_lists[event_string].pop()['start']*1000

while song_start_time == 0:
    pass

while True:
    song_start_time_lock.acquire()
    curr_ms = (time.time_ns()/1000000) - song_start_time if song_start_time > 0 else 0
    song_start_time_lock.release()
    
    for event_id in event_types:
        if curr_ms > next_event[event_id]:
            print(event_id)
            if len(event_lists[event_id]) != 0:
                next_event[event_id] = event_lists[event_id].pop()['start']*1000
            else:
                next_event[event_id] = float('inf')
