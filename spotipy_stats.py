import os

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth


class SpotifyFunctions:
    def __init__(self):
        load_dotenv()

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
            scope="user-top-read"   # "user-library-read"
        ))

    def get_current_user_profile(self):
        user_info = self.sp.current_user()
        print(user_info)

    def get_user_top_artists(self):
        top_artists = self.sp.current_user_top_artists(time_range="long_term")
        for i in top_artists["items"]:
            print(i["name"])

    def get_user_top_songs(self):
        top_songs = self.sp.current_user_top_tracks(time_range="long_term")
        for i in top_songs["items"]:
            print(i["name"])

    def get_song_data(self, id):
        self.sp.track(track_id=id)


if __name__ == "__main__":
    spot_func = SpotifyFunctions()
    # spot_func.get_current_user_profile()
    spot_func.get_user_top_artists()
