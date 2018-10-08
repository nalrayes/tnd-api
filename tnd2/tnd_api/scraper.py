import re

SAMPLE_DESC = "Listen: https://www.youtube.com/watch?v=C3-skAbrO2g\n\nLogic is, as always, well-intentioned and likable on YSIV, but his music remains middle-of-the-road.\n\nMore rap reviews: https://www.youtube.com/playlist?list=PLP4CSgl7K7ormBIO138tYonB949PHnNcP\n\nBuy this album: https://amzn.to/2OI39pw\n\n===================================\nSubscribe: http://bit.ly/1pBqGCN\n\nOfficial site: http://theneedledrop.com\n\nTND Twitter: http://twitter.com/theneedledrop\n\nTND Facebook: http://facebook.com/theneedledrop\n\nSupport TND: http://theneedledrop.com/support\n===================================\n\nFAV TRACKS: EVERYBODY DIES, THE RETURN, THE GLORIOUS FIVE, LEGACY\n\nLEAST FAV TRACK: ORDINARY DAY\n\nLOGIC - YSIV / 2018 / DEF JAM / BOOM BAP, POP RAP\n\n5/10\n\nY'all know this is just my opinion, right?"

def get_fav_tracks(desc):
    res = re.search("FAV TRACKS: ([\w+, ]+)", desc)
    return res[1]

def get_least_fav_track(desc):
    res = re.search("LEAST FAV TRACK: ([\w+ ]+)", desc
    return res[1]

def get_artist_name(desc):
    res = re.search("LEAST FAV TRACK: [\w+ ]+\n\n((\w+ )+)-", desc)
    return res[1].strip()

def get_album_name(desc):
    res = re.search("LEAST FAV TRACK: [\w+ ]+\n\n(\w+ )+-(( ?.+){1}?) \/ \d", desc)
    return res[2].strip()

def get_label(desc):
