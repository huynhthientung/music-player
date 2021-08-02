from tkinter import *
from tkinter import filedialog
import pygame
import os
import time
from mutagen.mp3 import MP3

cwd = os.getcwd()
cwd = cwd.replace("\\", "/")
FONT = ("Arial", 14)

root = Tk()
root.title("MP3 Player")
root.geometry("500x350")

# drawing the box which contains a list of songs
song_box = Listbox(root, bg="black", fg="green", width=60, selectbackground="gray", selectforeground="black")
song_box.pack(pady=20)

# init the mixer
pygame.mixer.init()


def play_by_time():
    current_time = pygame.mixer.music.get_pos() / 1000
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

    current_song = song_box.curselection()
    song = song_box.get(current_song)
    song = cwd + "/audio/" + song + ".mp3"

    song_mutagen = MP3(song)  # load song

    song_length = song_mutagen.info.length  # get length with mutagen
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    status_bar.config(text=f"Time elapsed: {converted_current_time} of {converted_song_length}")
    status_bar.after(1000, play_by_time)


def add_song():
    song = filedialog.askopenfilename(initialdir='audio/', title="Choose a song", filetypes=(("mp3 Files", "*.mp3"),))
    song = song.replace(cwd + "/audio/", '')
    song = song.replace(".mp3", "")
    song_box.insert(END, song)
    song_box.select_set(0)


def add_many_song():
    songs = filedialog.askopenfilenames(initialdir='audio/', title="Choose a song", filetypes=(("mp3 Files", "*.mp3"),))
    for song in songs:
        song = song.replace(cwd + "/audio/", '')
        song = song.replace(".mp3", "")
        song_box.insert(END, song)
    song_box.select_set(0)


def play_song():
    global paused
    paused = False
    song = song_box.get(ACTIVE)
    song = cwd + "/audio/" + song + ".mp3"
    print(song)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # call the play_by_time function to get song's length
    play_by_time()


global paused
paused = False


def pause_song(is_paused):
    global paused
    paused = is_paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True


def stop_song():
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)


def next_song():
    current = song_box.curselection()
    current_one = current[0]  # get current position of the song
    song_box.select_clear(current_one)
    next_one = current[0] + 1
    song = song_box.get(next_one)
    song = cwd + "/audio/" + song + ".mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    song_box.activate(next_one)
    song_box.select_set(next_one, last=None)


def previous_song():
    current = song_box.curselection()
    current_one = current[0]  # get current position of the song
    song_box.select_clear(current_one)
    prev_one = current[0] - 1
    song = song_box.get(prev_one)
    song = cwd + "/audio/" + song + ".mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    song_box.activate(prev_one)
    song_box.select_set(prev_one, last=None)


def remove_one_song():
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()
    status_bar.config(text="Select a song to play")


def remove_all_song():
    song_box.delete(0, END)
    pygame.mixer.music.stop()
    status_bar.config(text="Select a song to play")



# create image buttons
btn_previous_img = PhotoImage(file="icons/previous.png")
btn_next_img = PhotoImage(file="icons/next.png")
btn_pause_img = PhotoImage(file="icons/pause.png")
btn_stop_img = PhotoImage(file="icons/stop.png")
btn_play_img = PhotoImage(file="icons/play.png")

# create player control frame
control_frame = Frame(root)
control_frame.pack()

# create player control button
btn_previous = Button(control_frame, image=btn_previous_img, borderwidth=0, command=previous_song)
btn_next = Button(control_frame, image=btn_next_img, borderwidth=0, command=next_song)
btn_pause = Button(control_frame, image=btn_pause_img, borderwidth=0, command=lambda: pause_song(paused))
btn_play = Button(control_frame, image=btn_play_img, borderwidth=0, command=play_song)
btn_stop = Button(control_frame, image=btn_stop_img, borderwidth=0, command=stop_song)

# set position
btn_previous.grid(row=0, column=0, padx=10)
btn_play.grid(row=0, column=1, padx=10)
btn_pause.grid(row=0, column=2, padx=10)
btn_stop.grid(row=0, column=3, padx=10)
btn_next.grid(row=0, column=4, padx=10)

# create menu
my_menu = Menu(root)
root.config(menu=my_menu)

add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add song", menu=add_song_menu, font=FONT)
add_song_menu.add_command(label="Add one song to playlist", command=add_song, font=FONT)
add_song_menu.add_command(label="Add many songs to playlist", command=add_many_song, font=FONT)

remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove song", menu=remove_song_menu, font=FONT)
remove_song_menu.add_command(label="Remove one song from playlist", command=remove_one_song, font=FONT)
remove_song_menu.add_command(label="Remove all songs from playlist", command=remove_all_song, font=FONT)

status_bar = Label(root, text='Add song to playlist to play', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)
root.mainloop()
