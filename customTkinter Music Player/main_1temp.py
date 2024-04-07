import tkinter
from tkinter.ttk import Progressbar
from tkinter import *
from tkinter import Listbox
from tkinter import filedialog
from tkinter import messagebox
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
root.geometry('575x380')
root.resizable(False,False)
pygame.mixer.init()



def get_music_name(music_name):
    stripped_string = music_name[:-4]
    music_name_label = tkinter.Label(text = stripped_string, bg = '#222222', fg = 'white' )
    music_name_label.place(relx=0.25,rely=0.65)


def loadimg(image1):
    image2 = image1.resize((250,250))
    load = ImageTk.PhotoImage(image2)
    label1 = tkinter.Label(root,image=load)
    label1.image = load
    label1.place(relx=.14,rely=.08)

def get_album_cover(music_name):
    if music_name.startswith("Ins"):
        image1 = Image.open('D:\Python Project\img\cvr (6).jpg')
        loadimg(image1)
    elif music_name.startswith("Bea"):
        image1 = Image.open('D:\Python Project\img\cvr (11).jpg')
        loadimg(image1)
    elif music_name.startswith("Di"):
        image1 = Image.open('D:\Python Project\img\cvr (1).jpg')
        loadimg(image1)
    elif music_name.startswith("Su"):
        image1 = Image.open('D:\Python Project\img\cvr (13).jpg')
        loadimg(image1)
    elif music_name.startswith("We"):
        image1 = Image.open('D:\Python Project\img\cvr (2).jpg')
        loadimg(image1)
    elif music_name.startswith("Li"):
        image1 = Image.open('D:\Python Project\img\cvr (3).jpg')
        loadimg(image1)
    elif music_name.startswith("No"):
        image1 = Image.open('D:\Python Project\img\cvr (8).jpg')
        loadimg(image1)
    elif music_name.startswith("Hi"):
        image1 = Image.open('D:\Python Project\img\cvr (10).jpg')
        loadimg(image1)
    elif music_name.startswith("Vu"):
        image1 = Image.open('D:\Python Project\img\cvr (12).jpg')
        loadimg(image1)
    elif music_name.startswith("Int"):
        image1 = Image.open('D:\Python Project\img\cvr (9).jpg')
        loadimg(image1)
    elif music_name.startswith("Let"):
        image1 = Image.open('D:\Python Project\img\cvr (7).jpg')
        loadimg(image1)
    elif music_name.startswith("Is"):
        image1 = Image.open('D:\Python Project\img\cvr (4).jpg')
        loadimg(image1)     



def play_music():
    try:
        music_name = Playlist.get(ACTIVE)
        pygame.mixer.music.load(Playlist.get(ACTIVE))
        pygame.mixer.music.play()

        progress_bar.start()
        get_music_name(music_name)
        get_album_cover(music_name)
    except:
        messagebox.showinfo('Error', 'Please select the folder first')


def pause_song():
    pygame.mixer.music.pause()
    progress_bar.stop()

def resume_song():
    pygame.mixer.music.unpause()
    progress_bar.start()


def repeat():
    pygame.mixer.music.rewind()
    progress_bar.start()

def volume(value):
    pygame.mixer.music.set_volume(value)

def open_folder():
    path=filedialog.askdirectory()
    if path:
        os.chdir(path)
        songs=os.listdir(path)
        for song in songs:
            if song.endswith(".mp3"):
                Playlist.insert(END,song)



#Buttons

play_button = customtkinter.CTkButton(master=root, text='Play', command=play_music, width=75)
play_button.place(relx=0.27, rely=0.78, anchor=tkinter.CENTER)

pause_button = customtkinter.CTkButton(master=root, text='⏹',command=pause_song, width=2)
pause_button.place(relx=0.44, rely=0.78, anchor=tkinter.CENTER)

resume_button = customtkinter.CTkButton(master=root, text='⏯', command=resume_song, width=2)
resume_button.place(relx=0.37, rely=0.78, anchor=tkinter.CENTER)

rep = customtkinter.CTkButton(master=root, text='🔁', command=repeat, width=2)
rep.place(relx=0.17, rely=0.78, anchor=tkinter.CENTER)

slider = customtkinter.CTkSlider(master=root, from_=0, to=.99, orient=VERTICAL, command=volume, height=100)
slider.place(relx=0.04, rely=.68, anchor=tkinter.W)
slider.set(.2)

progress_bar = customtkinter.CTkProgressBar(master=root, progress_color='green', width=340, mode='determinate', determinate_speed=.005)
progress_bar.place(relx=0.3, rely=0.955, anchor=tkinter.CENTER)
progress_bar.set(0)

frame = customtkinter.CTkFrame(master=root, width=250, height=380, corner_radius=20)
frame.place(relx=.6, rely=.50, anchor=tkinter.W)

Volume_label = tkinter.Label(text = "Volume", bg = '#222222', fg = 'white',)
Volume_label.place(relx=0.01, rely=0.83,anchor=tkinter.W)

select_folder = customtkinter.CTkButton(master=root, text='🔗', command=open_folder, width=2)
select_folder.place(relx=0, rely=0, anchor=tkinter.NW)


Playlist = Listbox(master=root, selectmode=SINGLE, font=("Arial 9 bold"), width=30, height=22, bg='black', fg="grey",borderwidth=12,
highlightcolor='green')
Playlist.place(relx=.8, rely=.508, anchor=tkinter.CENTER)




root.mainloop()