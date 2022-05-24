import music
import tkinter as tk, threading
from tkinter import *
from tkvideo import tkvideo
import imageio
from PIL import Image, ImageTk

def stream(label):
    video = imageio.get_reader("video2.avi")
    for image in video.iter_data():
        frame_image = ImageTk.PhotoImage(Image.fromarray(image))
        label.config(image=frame_image)
        label.image = frame_image

def play_video(window):
    
    video_label = Label(window)
    video_label.pack()
    # read video to display on label
    thread = threading.Thread(target=stream, args=(video_label,))
    thread.daemon = 1
    thread.start()
    player = tkvideo("video2.avi", video_label, loop = 1, size = (500, 500))
    player.play()

window = tk.Tk()
window.geometry("700x620")
window.title("Astronify")
Label(window, text= "Astronify - Sonification Software for Astronomical Images", font= ('Aerial 17 bold italic')).pack(pady= 30)
button = tk.Button(window, text="Select Image", command=music.get_music, bg="skyblue").pack(pady=20)
video_button = tk.Button(window, text="Play Video", command=play_video(window), bg="skyblue").pack(pady=10)

window.mainloop()