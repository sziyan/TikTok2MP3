import yt_dlp
import os

def download(url):
    ydl_opts = {
        # 'format': 'bestaudio',
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'outtmpl': 'song'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        clean_info = ydl.sanitize_info(info)
        title = clean_info['title']
        track = clean_info['track']
        filename = track + '.mp3'
        print('Downloading {} from TikTok'.format(title))
        ydl.download(url)
        os.rename('song.mp3', filename)
        return title, filename