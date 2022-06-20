import music
import tkinter as tk
from tkinter import *
from tkVideoPlayer import TkinterVideo

def play_video():

    global videoplayer
    videoplayer = TkinterVideo(master=window, scaled=True, pre_load=False)
    videoplayer.load(r"{}".format("video2.avi"))
    videoplayer.pack(expand=True, fill="both")
    videoplayer.play()

window = tk.Tk()
window.geometry("700x620")
window.title("Astronify")
Label(window, text= "Astronify - Sonification Software for Astronomical Images", font= ('Aerial 17 bold italic')).pack(pady= 30)
button = tk.Button(window, text="Select Image", command=music.get_music, bg="skyblue").pack(pady=20)
#video_button = tk.Button(window, text="Play Video", command=play_video(), bg="skyblue").pack(pady=10)

window.mainloop()