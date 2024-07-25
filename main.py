import os
import re
import unicodedata

import praw
import spotipy
from dotenv import load_dotenv
from halo import Halo
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")


reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri="http://localhost:8080",
    scope="playlist-modify-private"
))

@Halo(text='Searching for song recommendations', spinner='dots')
def search_reddit_for_recommendations(subreddit_name, query, limit=10):
    subreddit = reddit.subreddit(subreddit_name)
    posts = subreddit.search(query, limit=limit)
    
    recommendations = []
    for post in posts:
        post.comments.replace_more(limit=0)
        for comment in post.comments.list():
            recommendations.extend(extract_song_recommendations(comment.body))
    
    return recommendations

@Halo(text='Searching for latest song recommendations', spinner='dots')
def search_reddit_for_recommendations_latest(subreddit_name, query, limit=10):
    subreddit = reddit.subreddit(subreddit_name)
    # Search for posts in the subreddit using the given query
    # Sort by 'new' to get the latest posts, and limit to 3
    posts = subreddit.search(query, sort='new', limit=limit)
    
    recommendations = []
    for post in posts:
        post.comments.replace_more(limit=0)
        for comment in post.comments.list():
            recommendations.extend(extract_song_recommendations(comment.body))
    
    return recommendations

def extract_song_recommendations(text):
    return re.findall(r'"([^"]*)" by ([^,\n]+)', text)

def clean_query(text):
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode()
    text = re.sub(r'[^\w\s-]', '', text)
    text = ' '.join(text.split())
    return text[:20]

@Halo(text='Creating Spotify Playlist', spinner='growVertical')
def create_spotify_playlist(name, tracks):
    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user_id, name, public=False)
    
    track_ids = []
    for track, artist in tracks:
        query = clean_query(f'{track} {artist}')
        results = sp.search(q=query, type='track', limit=1)
        if results['tracks']['items']:
            track_ids.append(results['tracks']['items'][0]['id'])
    
    if track_ids:
        sp.playlist_add_items(playlist['id'], track_ids)
    
    return playlist['external_urls']['spotify']

def main():
    subreddit_name = "spotify" 
    query = "song recommendations OR favorite songs"
    
    recommendations = search_reddit_for_recommendations(subreddit_name, query)
    
    for track, artist in recommendations:
        print(f'"{track}" by {artist}')
    
    playlist_name = f"Reddit Song Recommendations from r/{subreddit_name}"
    playlist_url = create_spotify_playlist(playlist_name, recommendations)
    
    print(f"\nPlaylist created! You can find it here: {playlist_url}")

if __name__ == "__main__":
    main()