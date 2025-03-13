import json
import os
import sys
from functools import cmp_to_key


class FilterFiles:
    def __init__(self, file_path):
        self.__file_path = file_path
        self.__sorted_jsons = []

    # +ive return = file1 bigger than file2
    def __sort_jsons(self, file1, file2):
        file1 = self.__get_filtered_filename(file1)
        file2 = self.__get_filtered_filename(file2)

        if file1[-1] > file2[-1]:
            return 1

        return -1

    def __get_filtered_filename(self, file_name):
        return file_name.replace(".json", "")

    def __is_json_file(self, file_name):
        return file_name[-5:] == ".json"

    def __is_audio_file(self, file_name):
        return file_name[18:23] == "Audio"

    def __filter_files(self):
        jsons = []
        files = os.listdir(self.__file_path)

        for file in files:
            if self.__is_json_file(file) and self.__is_audio_file(file):
                jsons.append(file)

        self.sorted_jsons = sorted(jsons, key=cmp_to_key(self.__sort_jsons))

    def get_sorted_jsons(self):
        self.__filter_files()
        return self.sorted_jsons


class SpotifyJsonStats:
    def __init__(self, file_path):
        self.__listening_data = {}

        self.__json_files = FilterFiles(file_path).get_sorted_jsons()

    def __count_all_stats(self):
        for json_file in self.__json_files:
            self.__count_json_stats(json_file)
        return

    def __count_json_stats(self, json_file):
        with open(get_absolute_resources_path() + "\\" + json_file, encoding="utf-8") as f:
            song_data = json.load(f)

            for song in song_data:
                self.__count_stats(song)

        return

    def __count_stats(self, song):
        # was not skipped and listened for 1 minute or more
        if self.__is_valid_listen(song):
            self.__listening_data[song["ts"]] = {
                "track_name": song["master_metadata_track_name"],
                "artist_name": song["master_metadata_album_artist_name"],
                "album_name": song["master_metadata_album_album_name"],
                "spotify_track_uri": song["spotify_track_uri"]
            }

    def __is_valid_listen(self, song):
        return (song["skipped"] is not (None or False) and
                song["ms_played"] >= 60000 and
                song["spotify_track_uri"] is not None)

    def get_artist_count(self):
        artist_count = {}
        for song in self.__listening_data.values():
            artist_count[song["artist_name"]] = artist_count.get(song["artist_name"], 0) + 1

        return sorted(artist_count.items(), key=lambda x: x[1], reverse=True)

    def run(self):
        self.__count_all_stats()


def get_absolute_resources_path():
    return os.path.dirname(os.path.abspath(sys.argv[0])) + "\\resources\\my_spotify_data_stream_history\\MyData"


if __name__ == "__main__":
    stats = SpotifyJsonStats(get_absolute_resources_path())
    stats.run()

    artist_count = stats.get_artist_count()

    for artist in artist_count:
        print(artist)
