import tkinter
from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import filedialog
import customtkinter
import pygame
from PIL import Image,ImageTk
from threading import *
import time
import math
import os

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

root = customtkinter.CTk()
root.title("Music Player")
root.geometry('300x400')
pygame.mixer.init()

list_of_songs=['music/Insomnia.mp3','music/Intentions.mp3','music/High on Life.mp3','music/Different World.mp3','music/Beautiful People.mp3','music/Is There Someone Else.mp3','music/Let Me Down Slowly.mp3','music/Light Switch.mp3','music/No Shame.mp3','music/Sunflower.mp3','music/Vulnerable.mp3','music/Wrecked.mp3']
list_of_covers=['img/cvr (6).jpg','img/cvr (9).jpg','img/cvr (10).jpg','img/cvr (1).jpg','img/cvr (11).jpg','img/cvr (4).jpg','img/cvr (7).jpg','img/cvr (3).jpg','img/cvr (8).jpg','img/cvr (13).jpg','img/cvr (12).jpg','img/cvr (2).jpg']

n = 0

def get_album_cover(song_name,n):
    image1 = Image.open(list_of_covers[n])
    image2 = image1.resize((250,250))
    load = ImageTk.PhotoImage(image2)
    label1 = tkinter.Label(root,image=load)
    label1.image = load
    label1.place(relx=.19,rely=.06)

    stripped_string = song_name[6:-4]
    song_name_label = tkinter.Label(text = stripped_string, bg = '#222222', fg = 'white' )
    song_name_label.place(relx=0.4,rely=0.6)

def progress():
    a = pygame.mixer.Sound(f'{list_of_songs[n]}')
    song_length = a.get_length() * 3
    for i in range(0, math.ceil(song_length)):
        time.sleep(.3)
        progress_bar.set(pygame.mixer.music.get_pos()/1000000)

def threading():
    t1 = Thread(target=progress)
    t1.start

def play_music():
    threading()
    global n
    current_song = n
    if n>2:
        n=0
    song_name = list_of_songs[n]
    pygame.mixer.music.load(song_name)
    pygame.mixer.music.play(loops=0)
    pygame.mixer.music.set_volume(1)
    get_album_cover(song_name,n)
    n += 1

def skip_forward():
    play_music()

def skip_backward():
    global n
    n -= 2
    play_music()

def volume(value):
    pygame.mixer.music.set_volume(value)


def open_folder():
    filename = filedialog.askopenfilename(initialdir="D:/",title="Select a file",filetypes=("*.mp3"))


#Buttons
play_button = customtkinter.CTkButton(master=root,text='Play',command=play_music)
play_button.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)


skip_fwd = customtkinter.CTkButton(master=root,text='>>',command=skip_backward,width=2)
skip_fwd.place(relx=0.7, rely=0.7, anchor=tkinter.CENTER)

skip_bwd = customtkinter.CTkButton(master=root,text='<<',command=skip_forward,width=2)
skip_bwd.place(relx=0.3, rely=0.7, anchor=tkinter.CENTER)

slider = customtkinter.CTkSlider(master=root,from_=0,to=1,command=volume,width=210)
slider.place(relx=0.5, rely=.78, anchor=tkinter.CENTER)

progress_bar = customtkinter.CTkProgressBar(master=root,progress_color='purple',width=250)
progress_bar.place(relx=0.5, rely=0.85, anchor=tkinter.CENTER)

select_folder = customtkinter.CTkButton(master=root,text='🔗',command=open_folder,width=2)
select_folder.place(relx=0.1, rely=0.10, anchor=tkinter.CENTER)

scrollbox = customtkinter.CTkScrollbar(master=root, width=10)
scrollbox.place(relx=0.10, rely=0.100, anchor=tkinter.CENTER)

frame = customtkinter.CTkFrame(master=root, width=250, height=380, corner_radius=20)
frame.place(relx=.6, rely=.50, anchor=tkinter.W)

root.mainloop()