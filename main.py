from tkinter import *
from tkinter import filedialog
import pygame
from pygame import mixer
import os

cwd = os.getcwd()
FONT = ("Consolas", 14)

root = Tk()
root.title("MP3 Player")
root.geometry("500x300")

# init the mixer
pygame.mixer.__init__


def add_song():
    song = filedialog.askopenfilename(initialdir='audio/', title="Choose a song", filetypes=(("mp3 Files", "*.mp3"), ))
    print(song)
    song = song.replace(os.getcwd() + '/audio/', '')
    song = song.replace(".mp3", "")
    song_box.insert(END, song)


def play_song():
    song = song_box.get(ACTIVE)
    song = cwd + '/' + song + ".mp3"
    pygame.mixer.music.load(song)


# drawing the box which contains a list of songs
song_box = Listbox(root, bg="black", fg="green", width=60, selectbackground="gray", selectforeground="black")
song_box.pack(pady=20)

# create image buttons
btn_previous_img = PhotoImage(file="icons/previous.png")
btn_next_img = PhotoImage(file="icons/next.png")
btn_pause_img = PhotoImage(file="icons/pause.png")
btn_stop_img = PhotoImage(file="icons/stop.png")
btn_play_img = PhotoImage(file="icons/play.png")


#create player control frame
control_frame = Frame(root)
control_frame.pack()

#create player control button
btn_previous = Button(control_frame, image=btn_previous_img, borderwidth=0)
btn_next = Button(control_frame, image=btn_next_img, borderwidth=0)
btn_pause = Button(control_frame, image=btn_pause_img, borderwidth=0)
btn_play = Button(control_frame, image=btn_play_img, borderwidth=0, command=play_song)
btn_stop = Button(control_frame, image=btn_stop_img, borderwidth=0)

#set position
btn_previous.grid(row=0, column=0, padx=10)
btn_play.grid(row=0, column=1, padx=10)
btn_pause.grid(row=0, column=2, padx=10)
btn_stop.grid(row=0, column=3, padx=10)
btn_next.grid(row=0, column=4,padx=10)

# create menu
my_menu = Menu(root)
root.config(menu=my_menu)

add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add songs", menu=add_song_menu, font=FONT)
add_song_menu.add_command(label="Add one song to playlist", command=add_song, font=FONT)
root.mainloop()