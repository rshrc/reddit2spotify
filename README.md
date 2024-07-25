# Reddit to Spotify Playlist Creator

Somehow spotify recommendations are not helping me heal anymore. 

P.S people are writing blazing-fast, memory-safe, concurrency-handling Rust programs, here I am, whipping up some kiddy Python scripts.

## Why I Created This

Every day, I saw fantastic song suggestions on Reddit that I wanted to add to my Spotify playlists. But the manual process was tedious and frustrating. I wanted a seamless way to collect these recommendations and turn them into a playlist to save time and keep the music discovery process exciting & fresh 


## What You Need

- **Python 3.12 or higher:** No exceptions.
- **Reddit Account with an App:** Yes, you'll need to create an app.
- **Spotify Account with an App:** Ditto.

## Installation

1. **Clone or Download:**
   Get the script onto your machine.

2. **Install Dependencies:**
   Open your terminal and run:
   ```
   python -m venv venv && source venv/bin/activate && pip install poetry
   ```
3. **Install Dependencies:**
    Run the following command to install all dependencies specified in the pyproject.toml file:

    ```
    poetry install
    ```


## Setting Up Your Environment

1. **Reddit API Setup:**
   - Visit [Reddit Apps](https://www.reddit.com/prefs/apps) and create a new application (select "script" type).
   - Keep your client ID and secret handy.

2. **Spotify API Setup:**
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and create a new application.
   - Note down the client ID and secret.
   - Add `http://localhost:8080` as a redirect URI in your app settings.

3. **Environment Variables:**
   - Create a `.env` file in your project directory and add the following:
     ```
     REDDIT_CLIENT_ID=your_reddit_client_id
     REDDIT_CLIENT_SECRET=your_reddit_client_secret
     REDDIT_USER_AGENT=your_user_agent (e.g., "MyRedditApp/1.0")
     SPOTIFY_CLIENT_ID=your_spotify_client_id
     SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
     SPOTIFY_REDIRECT_URI=http://localhost:8080
     ```

## How to Run

Fire up the script with:

```
python main.py
```

The first run will ask you to authorize the app to access your Spotify account. Don't worry, your data's safe.

## What It Does

1. **Scours Reddit:** Hunts down song recommendations in your specified subreddit.
2. **Extracts Songs:** Plucks out the song titles and artists from the comments.
3. **Creates a Playlist:** Generates a new private Spotify playlist.
4. **Adds Tracks:** Populates your playlist with the recommended songs.
5. **Not Fancy** Its not fancy or web based, just a normal script


Now, go ahead and get yourself some good music!