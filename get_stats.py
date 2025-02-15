import os
import sys
import json
from functools import cmp_to_key

class FilterFiles:
    def __init__(self, file_path):
        self.file_path = file_path
        self.sorted_jsons = []

    # +ive return = file1 bigger than file2
    def sort_jsons(self, file1, file2):
        file1 = self.get_filtered_filename(file1)
        file2 = self.get_filtered_filename(file2)

        if file1[-1] > file2[-1]:
            return 1

        return -1

    def get_filtered_filename(self, file_name):
        return file_name.replace(".json", "")

    def is_json_file(self, file_name):
        return file_name[-5:] == ".json"

    def is_audio_file(self, file_name):
        return file_name[18:23] == "Audio"

    def filter_files(self):
        jsons = []
        files = os.listdir(self.file_path)

        for file in files:
            if self.is_json_file(file) and self.is_audio_file(file):
                jsons.append(file)

        self.sorted_jsons = sorted(jsons,key=cmp_to_key(self.sort_jsons))

    def get_sorted_jsons(self):
        self.filter_files()
        return self.sorted_jsons


class GetStats:
    def __init__(self, file_path):
        self.artist_count_year = {}
        self.scrobble_count = 0

        self.json_files = FilterFiles(file_path).get_sorted_jsons()

    def count_all_stats(self):
        for json_file in self.json_files:
            self.count_json_stats(json_file)
        return

    def count_json_stats(self, json_file):
        with open(get_absolute_resources_path() + "\\" + json_file, encoding="utf-8") as f:
            listening_data = json.load(f)

        for song in listening_data:
            print(song["master_metadata_track_name"])

    def run(self):
        self.count_all_stats()

def get_absolute_resources_path():
    return os.path.dirname(os.path.abspath(sys.argv[0])) + "\\resources\\my_spotify_data_stream_history\\MyData"

if __name__ == "__main__":
    stats = GetStats(get_absolute_resources_path())
    stats.run()
