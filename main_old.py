import tkinter as tk
import customtkinter as ctk 
from pytube import Playlist, YouTube 
from pytube.exceptions import VideoUnavailable 
from urllib.parse import unquote


def download_video():
    try: 
        yt_link = link.get()
        
        yt_object = YouTube(yt_link)
        yt_thumbnail = yt_object.thumbnail_url
        yt_title = yt_object.title
        yt_caption = yt_object.captions.get_by_language_code('en')
        print(yt_caption.generate_srt_captions())
        yt_object.streams.get_highest_resolution().download()
        print(yt_link)
    except VideoUnavailable:
        print(f'Video {link} is unavaialable, skipping.')
    except VideoPrivate:
        print(f'Video {link} is private, skipping.')
    except VideoRegionBlocked:
        print(f'Video {link} is region blocked, skipping.')
    except AgeRestrictedError:
        print(f'Video {link} is age restricted, skipping.')
        print("YouTube link is invalid")
    print("Download Complete!")


def download_playlist():
    try:
        yt_playlist = Playlist(unquote(str(yt_plalist_link.get())))
        for yt_playlist_video in yt_playlist.videos:
            try:
                yt_playlist_video.streams.first().download()
            except VideoUnavailable:
                print(f'Video {link} is unavaialable, skipping.')
            print("Download Complete!")
    except VideoUnavailable:
         print(f'Video {link} is unavaialable, skipping.')

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()

screen_height = root.winfo_screenheight()
window_height = screen_height // 2
screen_width = root.winfo_screenwidth()
window_width = screen_width // 4

root.geometry(f"{window_width}x{window_height}")
root.title('Youtube Video Downloader')

title = ctk.CTkLabel(root, text="Insert a youtube link")
title.pack(padx=10, pady=10)

url_var = tk.StringVar()
link = ctk.CTkEntry(root, width=350, height=40, textvariable=url_var)
link.pack(padx=10, fill="x")

download = ctk.CTkButton(root, text="Download", command=download_video)
download.pack(padx=10, pady=10)

playlist_title = ctk.CTkLabel(root, text="Insert a youtube playlist link")
playlist_title.pack(padx=10, pady=10)

playlist_url_var = tk.StringVar()
yt_plalist_link = ctk.CTkEntry(root, width=350, height=40, textvariable=playlist_url_var)
yt_plalist_link.pack(padx=10, fill="x")

playlist_download = ctk.CTkButton(root, text="Playlist Download", command=download_playlist)
playlist_download.pack(padx=10, pady=10)


        
        
root.mainloop()
