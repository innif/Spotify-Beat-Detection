import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import time
import sys
from random import choice
import threading
import pygame

pygame.init()
screen = pygame.display.set_mode((400, 400))

song_start_time = 0
song_start_time_lock = threading.Lock()

settings = json.load(open("settings.json"))
apiKey = json.load(open("apiKey.json"))

auth_manger = SpotifyOAuth(scope=apiKey['scope'], username=settings['username'], client_id=apiKey['id'], client_secret=apiKey['secret'], redirect_uri=apiKey['redirect_uri'])
client = spotipy.Spotify(auth_manager=auth_manger)

current_playback = client.currently_playing()
current_song = current_playback['item']
current_analysis = client.audio_analysis(current_song['id'])

class timeCheckerThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global song_start_time, song_start_time_lock
        while True:
            curr_ms = time.time_ns()/1000000
            playback_pos = client.currently_playing()['progress_ms']
            start_time_temp = curr_ms - playback_pos
            song_start_time_lock.acquire()
            if song_start_time < start_time_temp or song_start_time == 0:
                song_start_time = start_time_temp
            song_start_time_lock.release()

timeChecker = timeCheckerThread()
timeChecker.start()

event_types = ['bars','beats','sections']
next_event = {}
last_event = {}
event_lists = {}

for event_string in event_types:
    event_lists[event_string] = current_analysis[event_string]
    event_lists[event_string].reverse()
    next_event[event_string] = event_lists[event_string].pop()['start']*1000
    last_event[event_string] = 0

while True:
    song_start_time_lock.acquire()
    curr_ms = (time.time_ns()/1000000) - song_start_time if song_start_time > 0 else 0
    song_start_time_lock.release()
    
    for event_id in event_types:
        if curr_ms > next_event[event_id]:
            print(event_id)
            last_event[event_id] = next_event[event_id]
            if len(event_lists[event_id]) != 0:
                next_event[event_id] = event_lists[event_id].pop()['start']*1000
            else:
                next_event[event_id] = float('inf')

    beat_time = (curr_ms-last_event['beats'])
    screen.fill((0,0,0))
    pygame.draw.circle(screen, (255, 255, 255), (200,200), int(max(100-beat_time/10, 5)))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()