#!/usr/bin/env bash
cd music_consolidator && npm install
cd .. && pip install -r requirements.txt
sudo curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl
sudo chmod a+rx /usr/local/bin/youtube-dl
