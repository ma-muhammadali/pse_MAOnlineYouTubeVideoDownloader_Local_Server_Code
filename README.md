## MA Online YouTube Video Downloader

## Overview
Do you Want to download any YouTube video, audio and video's transcript? No problem! Just type in the URL of the video and press the download button.

MA Online YouTube Video Downloader is a simple flask webapp to download youtube videos in high quality. It is also capable to download audio and video's transcript.

It uses pytube library for downloading videos and audio from YouTube.
It provides a simple and easy-to-use interface for extracting video URLs, stream information, and downloading YouTube videos in different resolutions. 
Pytube supports downloading videos from YouTube (a popular video sharing website). 
The library also supports extracting video information like title, author, and video length.


It uses YouTubeTranscriptApi library for accessing the automatic captions or transcripts of YouTube videos. 
The library provides a simple interface for requesting and retrieving captions from YouTube's servers in different languages and formats.
This can be useful for a variety of tasks, such as language translation, text analysis, and accessibility for the hearing-impaired. 
The library supports accessing captions for both public and private YouTube videos, making it a useful tool for researchers, developers, and anyone working with YouTube videos.


The application allows an anonymous user to download any YouTube video, audio and transcript. Instances where certain URLs are not allowed include:
- URL from a local machine ex. http://127.0.0.0:5000
- Empty URL
- URL from a non-YouTube video

The user will be shown a friendly and polite error message if the URL is not valid.

## Tools Used

- Flask and Python
- Bootstrap
- Pytube
- Youtube Transcript API

## Deployment

- http://maonlineyoutubevideodownloader.el.r.appspot.com on Google Cloud Platform (GCP)


## How to Download

Download this project from here [Download MA Online YouTube Video Downloader]

https://github.com/ma-muhammadali/pse_MAOnlineYouTubeVideoDownloader_Local_Server_Code.git

## Requirements

To install following packages :-

```bash
pip install flask
pip install flask-session
pip install pytube
pip install youtube_transcript_api
```

## Usage

* run app.py in python terminal and then goto http://127.0.0.1:5000/
* paste a youtube video url and click Start
* Click Download Video, Download will start automatically
