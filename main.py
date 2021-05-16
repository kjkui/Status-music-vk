import requests
import os
import json
import time
from datetime import timedelta

URL_TRACK = 'https://api.spotify.com/v1/me/player/currently-playing'
URL_STATUS = "https://api.vk.com/method/status.set"
VK_TOKEN = 'VK TOKEN'
SP_TOKEN = 'SPOTIFY TOKEN'


def set_status():
    params = {
              'user_id': 42907325,
              'v': 5.92,
              'access_token': VK_TOKEN,
              'text': current_track()
    }

    status = requests.get(url=URL_STATUS, params=params)
    print(status.text)


def track_data():
    headers = {
               'Accept': 'application/json',
               'Content-Type': 'application/json',
               'Authorization': f'Bearer {SP_TOKEN}',
    }

    return requests.get(url=URL_TRACK, headers=headers)


def track_is_playing():
    return track_data().status_code == 200


def current_track():
    data = track_data().json()
    artist_path = data["item"]['artists'][0]['name']
    track_path = data["item"]['name']
    time_progress = str(timedelta(milliseconds = data["progress_ms"])).split(':', 1)[1].split('.')[0].replace('0', '', 1)
    time_all = str(timedelta(milliseconds = data["item"]['duration_ms'])).split(':', 1)[1].split('.')[0].replace('0', '', 1)

    return(f'▶ {artist_path} - {track_path} ({time_progress} - {time_all})' if data["is_playing"] else f'⏸ {artist_path} - {track_path} ({time_progress} - {time_all})')


def run_script():
    if track_is_playing():
        set_status()
        print(current_track())
    else:
        print('Not playing')


if __name__ == "__main__":
     while True:
         run_script()
         time.sleep(300)