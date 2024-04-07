from tkinter import *
import Image, ImageTk
root= Tk()
a= Label(text="Welcome to python")
a.pack()
root.title("yo")
root.minsize(100,100)
root.maxsize(900,600)
root.geometry("730x360")

img = Image.open("D:\Downloads\296882115_558454152670556_1234961282825972431_n.jpg")
test= ImageTk.PhotoImage(img)

imag_label =tkinter.Label(img=test)
imag_label.image= text
root.mainloop()