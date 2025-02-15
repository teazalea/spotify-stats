import os
import sys


class SpotStats:
    def __init__(self):
        self.file_path = os.path.dirname(
            os.path.abspath(sys.argv[0])) + "\\resources\\my_spotify_data_stream_history\\MyData"
        self.audio_jsons = []

    def sort_jsons(self, file1, file2):
        file1 = self.get_filtered_filename(file1)
        file2 = self.get_filtered_filename(file2)
        if "-" in file1:
            f1_start_year = file1[:4]
            f2_end_year = file1[5:9]

    def get_filtered_filename(self, file_name):
        return file_name.replace("Streaming_History_Audio_", "").replace(".json", "")

    def run(self):
        self.audio_jsons = os.listdir(self.file_path)
        self.sort_jsons(self.audio_jsons[1], self.audio_jsons[2])


if __name__ == "__main__":
    stats = SpotStats()
    stats.run()
