#!/usr/bin/python3
# -*- coding: utf-8 -*-
import youtube_dl
from gmusicapi import Musicmanager
import argparse
import eyed3
import os

parser = argparse.ArgumentParser()
parser.add_argument('--link', dest="link", help='A link to port', required=True)
parser.add_argument('--auth', dest="auth", default="gmusic.cred", help='Path to oauth-file')
parser.add_argument('--artist', dest="artist", help='Name of artist of song', required=True)
parser.add_argument('--title', dest="title", help='Name of song', required=True)
config = parser.parse_args()

class Youtube:
    def __init__(self, savepath):
        self.savepath = savepath
        ydl_opts = {
            "outtmpl": "{}/single.%(ext)s".format(savepath),
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
        self.ydl.download([link])


class GoogleMusic:
    def __init__(self):
        self.api = Musicmanager()
        try:
            if not self.api.login(oauth_credentials=config.auth):
                self.api.perform_oauth(storage_filepath=config.auth, open_browser=True)
                self.api.login(oauth_credentials=config.auth)
        except:
            pass

    def upload_audio(self, filepath, transcode_quality='320k'):
        self.api.upload(filepath, enable_matching=False, transcode_quality=transcode_quality)
        print("Upload finished")


def main():
    savepath = "."
    yt = Youtube(savepath)
    gm = GoogleMusic()
    yt.download_audio(config.link)
    add_audio_metadata("{}/single.mp3".format(savepath), config.artist, config.title)
    gm.upload_audio("{}/single.mp3".format(savepath))
    os.remove("{}/single.mp3".format(savepath))


def add_audio_metadata(filename, artist, title):
    audiofile = eyed3.load(filename)
    audiofile.tag.artist = artist
    audiofile.tag.title = title
    audiofile.tag.save()


if __name__ == "__main__":
    main()