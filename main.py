import argparse
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
            recommendations.extend(extract_song_recommendations_2(comment.body))
    
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

@Halo(text='Searching for song recommendations from post', spinner='dots')
def search_reddit_post_for_recommendations(post_url):
    submission = reddit.submission(url=post_url)
    submission.comments.replace_more(limit=None)
    
    recommendations = []
    for comment in submission.comments.list():
        recommendations.extend(extract_song_recommendations_2(comment.body))
    
    return recommendations

def extract_song_recommendations_2(text):
    # Update the regex to be more flexible
    pattern = re.compile(r'"([^"]+)" by ([^,\n]+)|([^"]+)\s-\s([^,\n]+)')
    matches = pattern.findall(text)
    recommendations = []
    for match in matches:
        if match[0] and match[1]:
            recommendations.append((match[0], match[1]))
        elif match[2] and match[3]:
            recommendations.append((match[2], match[3]))
    return recommendations

def extract_song_recommendations(text):
    return re.findall(r'"([^"]*)" by ([^,\n]+)', text)

def clean_query(text):
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode()
    text = re.sub(r'[^\w\s-]', '', text)
    text = ' '.join(text.split())
    return text[:20]

@Halo(text='Creating Spotify Playlist', spinner='growVertical')
def create_spotify_playlist(name, tracks, search_limit=100):
    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user_id, name, public=False)
    
    track_ids = []
    for i, (track, artist) in enumerate(tracks):

        if i >= search_limit:
            break

        query = clean_query(f'{track} {artist}')
        try:
            results = sp.search(q=query, type='track', limit=1)
            if results['tracks']['items']:
                track_ids.append(results['tracks']['items'][0]['id'])
        except Exception as e:
            print(f"Error searching for {track} by {artist}: {e}")
    
    if track_ids:
        sp.playlist_add_items(playlist['id'], track_ids)
    
    return playlist['external_urls']['spotify']

def main():
    parser = argparse.ArgumentParser(description='Create a Spotify playlist from Reddit song recommendations.')
    parser.add_argument('-p', '--post', type=str, help='URL of the Reddit post to extract song recommendations from')
    args = parser.parse_args()

    if args.post:
        post_url = args.post
        recommendations = search_reddit_post_for_recommendations(post_url)

        print(f"No of songs recommended : {len(recommendations)}")
        submission = reddit.submission(url=post_url)
        playlist_name = submission.title.replace('_', ' ').title()
    else:
        subreddit_name = "spotify" 
        query = "song recommendations OR favorite songs"
        
        recommendations = search_reddit_for_recommendations(subreddit_name, query)
        playlist_name = f"Reddit Song Recommendations from r/{subreddit_name}"
    
    for track, artist in recommendations:
        print(f'"{track}" by {artist}')

    recommendations = list(filter(lambda x: x[0] and x[1], recommendations))

    
    playlist_url = create_spotify_playlist(playlist_name, recommendations)
    
    print(f"\nPlaylist created! You can find it here: {playlist_url}")

if __name__ == "__main__":
    main()