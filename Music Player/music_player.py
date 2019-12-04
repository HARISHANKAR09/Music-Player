from tkinter import *
import glob
from pygame import mixer
from pygame import *
import pygame

pygame.mixer.pre_init()
mixer.init()
pygame.init()
#-----------------------------------
win = Tk()
win.geometry("500x500")
win.title("Music Player...")
index = 0
top_frame = Frame(win)
top_frame.pack(side=TOP, expand=1, fill=BOTH)
play_icon = PhotoImage(file='images/play_round.png')
pause_icon = PhotoImage(file='images/pause_round.png')
next_icon = PhotoImage(file='images/next.png')
previous_icon = PhotoImage(file='images/previous.png')
listbox = Listbox(top_frame, selectmode=SINGLE, activestyle=NONE, relief=FLAT)
for file in glob.iglob('E:*\*.mp3'):
    listbox.insert(END, file)
y_scrollbar = Scrollbar(top_frame, orient=VERTICAL)
y_scrollbar.config(command=listbox.yview)
y_scrollbar.pack(side=RIGHT, fill=Y)
listbox.config(yscrollcommand=y_scrollbar.set)
x_scrollbar = Scrollbar(top_frame, orient=HORIZONTAL)
x_scrollbar.config(command=listbox.xview)
listbox.config(xscrollcommand=x_scrollbar.set)
x_scrollbar.pack(side=BOTTOM, fill=X)
mixer.music.set_volume(0.2)
listbox.pack(expand=1, fill=BOTH)
isClicked = 1
def state_of_button():
    global isClicked
    if isClicked == 1 :
        if not mixer.music.get_busy() :
            try :
                mixer.music.load(listbox.get(ACTIVE))
                mixer.music.play()
                play_pause.config(image=pause_icon)
            except:
                print("can't play this audio...")
        else:
            mixer.music.unpause()
            play_pause.config(image=pause_icon)
            isClicked = 0
        isClicked=0
    elif isClicked == 0:
        play_pause.config(image=play_icon)
        mixer.music.pause()
        isClicked = 1
play_pause = Button(win, image=play_icon, width=60, height=50,command=state_of_button, border="0")

# ------------------------------------------------------------------------
def play_next(event=None):
    next = listbox.index(ACTIVE)
    next += 1
    listbox.selection_clear(0, END)
    listbox.select_set(next)
    listbox.activate(next)
    # try:
    mixer.music.load(listbox.get(ACTIVE))
    mixer.music.play()
    # s = pygame.mixer.Sound(listbox.get(ACTIVE))
    play_pause.config(image=pause_icon)
    listbox.yview(listbox.index(ACTIVE))
    print(mixer.music.get_pos())
    # except:
    #     print("can't play this audio...")
next_button = Button(win, image=previous_icon, width=60, height=50,command=play_next, border="0")

#--------------------------------------------------------------------------
def play_previous(event=None):
    previous = listbox.index(ACTIVE)
    previous -= 1
    listbox.selection_clear(0, END)
    listbox.select_set(previous)
    listbox.activate(previous)
    mixer.music.load(listbox.get(ACTIVE))
    mixer.music.play()
    play_pause.config(image=pause_icon)
    listbox.yview(listbox.index(ACTIVE))
previous_button = Button(win, image=next_icon, width=60, height=50,command=play_previous, border="0")
def hello(event=None):
    try:
        global index
        index = int(listbox.curselection()[0])
        mixer.music.load(listbox.get(listbox.index(index)))
        mixer.music.play()
        play_pause.config(image=pause_icon)
        # mixer.music.queue(listbox.get(index + 1))
        global isClicked
        isClicked = 0
    except:
        print("can't play this audio...")
listbox.bind("<<ListboxSelect>>", hello)
frame_bottom = Frame(win, width=100)
frame_bottom.pack(side=BOTTOM)
#--------------------------
slider = Scale(frame_bottom, orient=HORIZONTAL, showvalue=50, label="Volume", relief=FLAT, from_=10, to=100, length=300, resolution=10, tickinterval=10, fg="red")
previous_button.pack(side=LEFT, expand=YES)
play_pause.pack(side=LEFT, expand=YES)
next_button.pack(side=LEFT, expand=YES)

def volume(event=None):
    # print((slider.get())/100)
    mixer.music.set_volume((slider.get())/100)
slider.bind("<ButtonRelease>", volume)
def scrolldown(event=None):
    next = listbox.index(ACTIVE)
    next += 1
    listbox.selection_clear(0, END)
    listbox.select_set(next)
    listbox.activate(next)
    listbox.yview(listbox.index(ACTIVE))
listbox.bind("<Down>", scrolldown)
def scrollup(event=None):
    previous = listbox.index(ACTIVE)
    previous -= 1
    listbox.selection_clear(0, END)
    listbox.select_set(previous)
    listbox.activate(previous)
    listbox.yview(listbox.index(ACTIVE))
listbox.bind("<Up>", scrollup)
slider.set(50)
mixer.music.queue(listbox.get(index + 1))
print(index)
slider.pack()
win.mainloop()