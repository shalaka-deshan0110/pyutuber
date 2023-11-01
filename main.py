import tkinter as tk
import tkinter.filedialog as filedialog
import customtkinter as ctk
from pytube import Playlist, YouTube
from pytube.exceptions import VideoUnavailable, VideoPrivate, VideoRegionBlocked, AgeRestrictedError
from urllib.parse import unquote
import os

user_home = os.path.expanduser("~")
default_download_path = os.path.join(user_home, "Downloads")

class YouTubeDownloaderApp:
    """Youtube video and playlist downloader with pytube."""
    def __init__(self, root):
        self.root = root
        self.download_path = default_download_path
        self.setup_gui()



    def setup_gui(self):
        """base GUI setup and widget creation."""
        screen_height = self.root.winfo_screenheight()
        window_height = screen_height // 2
        screen_width = self.root.winfo_screenwidth()
        window_width = screen_width // 4

        self.root.geometry(f"{window_width}x{window_height}")
        self.root.title("YouTube Video Downloader")

        self.create_widgets()

    def create_widgets(self):
        """Create labels, entries and buttons."""
        self.create_label("Insert a YouTube video link")
        self.link_entry = self.create_entry(350)
        self.create_button("Video Download", self.download_video)
        self.create_button("Select Download Path", self.select_download_path)


        self.create_label("Insert a YouTube playlist link")
        self.playlist_entry = self.create_entry(350)
        self.create_button("Playlist Download", self.download_playlist)
        self.create_button("Select Download Path", self.select_download_path)


    def create_label(self, text):
        """Create and place labels on the GUI."""
        label = ctk.CTkLabel(self.root, text=text)
        label.pack(padx=10, pady=10)

    def create_entry(self, width):
        """Create and place entries on the GUI."""
        entry = ctk.CTkEntry(self.root, width=width)
        entry.pack(padx=10, fill="x")
        return entry

    def create_button(self, text, command):
        """Create and place buttons on the GUI."""
        button = ctk.CTkButton(self.root, text=text, command=command)
        button.pack(padx=10, pady=10)
        

    def select_download_path(self):
        """Get user defined download path."""
        download_path = filedialog.askdirectory()
        if download_path:
            self.download_path = download_path
            print(f"Download path selected: {download_path}")

    def download_video(self):
        """Start downloading process for single video."""
        try:
            yt_link = self.link_entry.get()
            yt_object = YouTube(yt_link)
            yt_thumbnail = yt_object.thumbnail_url
            yt_title = yt_object.title
            yt_caption = yt_object.captions.get_by_language_code('en')
            if yt_caption:
                srt_captions = yt_caption.generate_srt_captions()
                print(srt_captions)
            else:
                print("No captions available for this video.")
                
            download_path = self.download_path 
            """Get the highest resolution video available."""
            yt_object.streams.get_highest_resolution().download(output_path=download_path)
            print(yt_link)
        except (VideoUnavailable, VideoPrivate, VideoRegionBlocked, AgeRestrictedError) as e:
            print(f"Video {yt_link} is unavailable, skipping.")
        print("Download Complete!")

    def download_playlist(self):
        """Start downloading process for playlists of videos."""
        try:
            yt_playlist = Playlist(unquote(str(self.playlist_entry.get())))
            download_path = self.download_path 
            for yt_playlist_video in yt_playlist.videos:
                try:
                    """Get the highest resolution video available."""
                    yt_playlist_video.streams.get_highest_resolution().download(output_path=download_path)
                except VideoUnavailable:
                    print(f"Video {yt_link} is unavailable, skipping.")
            print("Download Complete!")
        except VideoUnavailable:
            print(f"Video {yt_link} is unavailable, skipping.")

def main():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()