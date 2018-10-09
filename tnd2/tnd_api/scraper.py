import re
import requests
import json

with open('tnd_api/config.json', 'r') as f:
    config = json.load(f)

YOUTUBE_API_KEY = config['key']

SAMPLE_DESC = "Listen: https://www.youtube.com/watch?v=C3-skAbrO2g\n\nLogic is, as always, well-intentioned and likable on YSIV, but his music remains middle-of-the-road.\n\nMore rap reviews: https://www.youtube.com/playlist?list=PLP4CSgl7K7ormBIO138tYonB949PHnNcP\n\nBuy this album: https://amzn.to/2OI39pw\n\n===================================\nSubscribe: http://bit.ly/1pBqGCN\n\nOfficial site: http://theneedledrop.com\n\nTND Twitter: http://twitter.com/theneedledrop\n\nTND Facebook: http://facebook.com/theneedledrop\n\nSupport TND: http://theneedledrop.com/support\n===================================\n\nFAV TRACKS: EVERYBODY DIES, THE RETURN, THE GLORIOUS FIVE, LEGACY\n\nLEAST FAV TRACK: ORDINARY DAY\n\nLOGIC - YSIV / 2018 / DEF JAM / BOOM BAP, POP RAP\n\n5/10\n\nY'all know this is just my opinion, right?"

YOUTUBE_API_PATH = "/youtube"
YOUTUBE_API_VERSION = "/v3"
GOOGLE_API_URL = "https://www.googleapis.com"
YOUTUBE_API_URL = GOOGLE_API_URL + YOUTUBE_API_PATH + YOUTUBE_API_VERSION + "/"

# get video by id function
def get_video_by_id(videoId):
    payload = {"part": "snippet", "id": videoId ,"key": YOUTUBE_API_KEY}
    req = requests.get(YOUTUBE_API_URL + 'videos', params=payload)
    return req.json()

def get_video_information(video_json):
    snippet = video_json['items'][0]['snippet']
    title = snippet['title']
    description = snippet['description']
    video_dict = {}

    video_dict['artist_name'] = get_artist_name_from_title(title)
    video_dict['album_name'] = get_album_name_from_title(title)

    video_dict['fav_tracks'] = get_fav_tracks(description)
    video_dict['least_fav_track'] = get_least_fav_track(description)
    video_dict['label'] = get_label(description)
    video_dict['score'] = get_score(description)
    video_dict['genres'] = get_genres(description)

    return video_dict



# get most recent video function

# get videos by playlist id (can do uploads for all videos)

# get all reviews

# get array of videos by id

# return list or string?
def get_fav_tracks(desc):
    res = re.search("FAV TRACKS: ([\w+, ]+)", desc)
    return res[1]

def get_least_fav_track(desc):
    res = re.search("LEAST FAV TRACK: ([\w+ ]+)", desc)
    return res[1]

def get_artist_name_from_title(title):
    res = re.search("((\w+ +)+)-", title)
    return res[1].strip()

def get_artist_name_from_desc(desc):
    res = re.search("LEAST FAV TRACK: [\w+ ]+\n\n((\w+ )+)-", desc)
    return res[1].strip()

def get_album_name_from_title(title):
    res = re.search("-( ?.+){1}? \w+ REVIEW", title)
    return res[1].strip()

def get_album_name_from_desc(desc):
    res = re.search("LEAST FAV TRACK: [\w+ ]+\n\n(\w+ )+-(( ?.+){1}?) \/ \d", desc)
    return res[2].strip()

def get_label(desc):
    # this one search gets artist, album, and label. see if can consolidate? is that even necessary?
    res = re.search("LEAST FAV TRACK: [\w+ ]+\n\n(\w+ )+-( ?.+) \/ ?\d+ ?\/( ?\w+ ?)+\/", desc)
    return res[3].strip()

# return int or string?
def get_score(desc):
    res = re.search("(\d+)\/10", desc)
    return res[1]

# return list or string?
def get_genres(desc):
     res = re.search("\/((,?( +\w+ ?)+)+)\\n", desc)
     return res[1].strip()

# get album type
