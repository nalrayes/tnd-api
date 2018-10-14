import re
import requests
import json
import dateutil.parser
from .models import *

with open('tnd_api/config.json', 'r') as f:
    config = json.load(f)

YOUTUBE_API_KEY = config['key']

SAMPLE_DESC = "Listen: https://www.youtube.com/watch?v=C3-skAbrO2g\n\nLogic is, as always, well-intentioned and likable on YSIV, but his music remains middle-of-the-road.\n\nMore rap reviews: https://www.youtube.com/playlist?list=PLP4CSgl7K7ormBIO138tYonB949PHnNcP\n\nBuy this album: https://amzn.to/2OI39pw\n\n===================================\nSubscribe: http://bit.ly/1pBqGCN\n\nOfficial site: http://theneedledrop.com\n\nTND Twitter: http://twitter.com/theneedledrop\n\nTND Facebook: http://facebook.com/theneedledrop\n\nSupport TND: http://theneedledrop.com/support\n===================================\n\nFAV TRACKS: EVERYBODY DIES, THE RETURN, THE GLORIOUS FIVE, LEGACY\n\nLEAST FAV TRACK: ORDINARY DAY\n\nLOGIC - YSIV / 2018 / DEF JAM / BOOM BAP, POP RAP\n\n5/10\n\nY'all know this is just my opinion, right?"

YOUTUBE_API_PATH = "/youtube"
YOUTUBE_API_VERSION = "/v3"
GOOGLE_API_URL = "https://www.googleapis.com"
YOUTUBE_API_URL = GOOGLE_API_URL + YOUTUBE_API_PATH + YOUTUBE_API_VERSION + "/"

# get video by id function
def get_video_by_id(video_id):
    payload = {"part": "snippet", "id": video_id ,"key": YOUTUBE_API_KEY}
    req = requests.get(YOUTUBE_API_URL + 'videos', params=payload)
    return req.json()

def get_video_information_from_item_list(item_list):
    video_info_list = []
    for i in range (len(item_list)):
        print("Starting " + str(i))
        video_info = get_video_information_from_item(item_list[i])
        video_info_list.append(video_info)
        print("Done " + str(i))
    return video_info_list

def get_video_information_from_item(item):
    snippet = item['snippet']
    title = snippet['title']
    description = snippet['description']
    if item['kind'] == "youtube#playlistItem":
        id = snippet["resourceId"]["videoId"]
    else:
        id = item['id']

    yt_link = "https://www.youtube.com/watch?v=" + id
    video_dict = {"youtube_link": yt_link}

    video_dict['review_release_date'] = dateutil.parser.parse(snippet["publishedAt"]).date()

    video_dict['artist_name'] = get_artist_name_from_title(title)
    video_dict['album_name'] = get_album_name_from_title(title)
    video_dict['album_type'] = get_album_type_from_title(title)

    video_dict['description'] = description
    video_dict['fav_tracks'] = get_fav_tracks(description)
    video_dict['least_fav_track'] = get_least_fav_track(description)
    video_dict['label'] = get_label(description)
    video_dict['rating'] = get_rating(description)
    video_dict['detailed_genres'] = get_detailed_genres(description)
    video_dict['year_released'] = get_year_released(description)

    return video_dict

# write video to database function
def write_video_to_db(video_dict):
    # create new artist for now, later check if it exists
    artist, artist_created = Artist.objects.update_or_create(name=video_dict['artist_name'])
    # also create new rating for now
    rating, rating_created = Rating.objects.update_or_create(rating_val=int(video_dict['rating']))
    # leave genre empty
    album = Album(
        title=video_dict['album_name'],
        review_release_date=video_dict['review_release_date'],
        fav_tracks=video_dict['fav_tracks'],
        least_fav_track=video_dict['least_fav_track'],
        year_released=video_dict['year_released'],
        record_company=video_dict['label'],
        album_type=video_dict['album_type'],
        detailed_genres=video_dict['detailed_genres'],
        youtube_link=video_dict['youtube_link'],
        description=video_dict['description'],
        rating=rating,
    )

    album.save()

    album.artists.add(artist)

# batch request function

# get most recent video function

# get videos by playlist id (can do uploads for all videos)
def get_playlist_items(playlist_id, page_token=None):
    payload = {"part": "snippet", "playlistId": playlist_id , "maxResults": 50, "key": YOUTUBE_API_KEY}
    if (page_token):
        payload["pageToken"] = page_token
    req = requests.get(YOUTUBE_API_URL + 'playlistItems', params=payload)
    return req.json()

def get_videos_by_playlist_id(playlist_id, page_token=None):
    playlist_items_json = get_playlist_items(playlist_id, page_token=page_token)
    playlist_items_items = playlist_items_json["items"]
    if ("nextPageToken" in playlist_items_json):
        token = playlist_items_json["nextPageToken"]
        next_page_items = get_videos_by_playlist_id(playlist_id, page_token=token)
        playlist_items_items.extend(next_page_items)
    return playlist_items_items



# get all reviews

# get array of videos by id

def get_album_type_from_title(title):
    res = re.search("- ( ?.+){1}? (\w+) REVIEW", title)
    return res[2].strip()

def get_artist_name_from_title(title):
    # maybe also a bit greedy
    res = re.search("(.+) ?-", title)
    return res[1].strip()

def get_album_name_from_title(title):
    # is this greedy
    res = re.search("- ( ?.+){1}? \w+ REVIEW", title)
    return res[1].strip()

# return list or string?
def get_fav_tracks(desc):
    # is this ok or is it too broad? seems ok but gotta double check
    res = re.search("FAV TRACKS: (.+?)\\n", desc)
    if (res == None):
        return ""
    return res[1]

def get_least_fav_track(desc):
    res = re.search("LEAST FAV TRACK: (.+?)\\n", desc)
    if (res == None):
        return ""
    return res[1]

def get_year_released(desc):
    res = re.search("\/ (\d+) \/", desc)
    return res[1].strip()

def get_label(desc):
    # this one search gets artist, album, and label. see if can consolidate? is that even necessary?
    res = re.search("\/ \d+ \/ (.+) \/", desc)
    if (res == None):
        return ""
    return res[1].strip()

# return int or string?
def get_rating(desc):
    if ("/10" not in desc):
        return ""
    res = re.search("\\n(( ?\w+ ?)|\d+)\/10", desc)
    # maybe check for isclassic or isnotgood
    return res[1]

# return list or string?
def get_detailed_genres(desc):
     res = re.search("\/(?!.+\/ ) (.+) ?\n\n\d+", desc)
     return res[1].strip()
