#!/usr/bin/python
# -*- coding: utf-8 -*-

import youtube_dl
from gmusicapi import Musicmanager
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--link', dest="link", help='A link to port', required=True)
#parser.add_argument('--artist', dest="artist", help='Name of artist of song', required=True)
#parser.add_argument('--title', dest="title", help='Name of song', required=True)
config = parser.parse_args()

class Youtube:
    def __init__(self, savepath):
        self.savepath = savepath
        ydl_opts = {
            "outtmpl": "{}/%(title)s.%(ext)s".format(savepath),
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            "extractaudio": True
        }
        self.ydl = youtube_dl.YoutubeDL(ydl_opts)

#TODO extract metadata for song automagically?

    def download_audio(self, link):
        info = self.ydl.extract_info(link, download=False)
        self.ydl.download([link])
        #TODO because skråstrek i navnet. fix
        return "{}/{}.mp3".format(self.savepath, info['title'])


class GoogleMusic:
    def __init__(self):
        self.api = Musicmanager()
        self.api.perform_oauth(storage_filepath="test.cred", open_browser=True)
        self.api.login(oauth_credentials="test.cred")

    def upload_audio(self, filepath, transcode_quality='320k'):
        self.api.upload(filepath, enable_matching=False, transcode_quality=transcode_quality)
        print("Upload finished")


def main():
    yt = Youtube(".")
    gm = GoogleMusic()
    filename = yt.download_audio(config.link)
    gm.upload_audio(filename)


if __name__ == "__main__":
    main()