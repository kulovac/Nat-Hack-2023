import numpy as np
import tkinter as tk
import pygame
import threading
import os

track = False
flag = False

playing = False
keyspressedArray = []
pygame.mixer.init()

SONG_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(SONG_END)

if(track == False):
    pygame.mixer.music.load('Audio1.wav')
else:
    pygame.mixer.music.load('Audio2.wav')
root = tk.Tk()


root.geometry("900x600")
root.title("Listen to what your brain tells ya")
root.configure(bg='#191414')

label = tk.Label(root, text="Brainify", font= ('Comic Sans MS', 36), fg='white', bg='#191414')

def playandPause(switcher = 0):
    global playing

    #if switcher == 0:
    if playing:
            #play(True)
            pygame.mixer.music.pause()
            playButton.config(text="PLAY",command=playandPause)
    else:
            #play(False)
            pygame.mixer.music.play()
            playButton.config(text="PAUSE",command=playandPause)

    playing = not playing
    #else:
        #if playing:
            
    
# def play(flag):
#     while not flag:
#         startTime = time.time()
#         synthesizer.main('Audio1.wav', keyspressedArray)
#         synthesizer.main('Audio2.wav', keyspressedArray)
#         endTime = time.time()
#         if endTime - startTime > 20:
#             time.sleep(20-endTime+startTime)

        

#def stop()````
    #global playing
    #pygame.mixer.music.stop()
    #playing = False
    #playButton.config(text="PLAY",command=playandPause)


def status():
    global playing
    if pygame.mixer.music.get_busy() == False:
        playing = False
        playButton.config(text="PLAY",command=playandPause)
    root.after(1000, status)

def insertelm(key):
    keyspressedArray.append(key)
    with open('keys.txt', 'w') as f:
        for item in keyspressedArray:
            f.write("%s\n" % item)

label.pack()
buttonFrame = tk.Frame(root)

buttonFrame.pack(side=tk.BOTTOM, pady=40)

playButton = tk.Button(buttonFrame, text = "PLAY", command= playandPause, height = 5, width = 20)
#stopButton = tk.Button(buttonFrame, text = "STOP", command= stop, height = 5, width = 20)


playButton.pack(side=tk.LEFT, padx=10)  
#stopButton.pack(side=tk.LEFT, padx=10)

piano = tk.Frame(root)
piano.pack(side=tk.BOTTOM, padx=10)

leftText = tk.Label(piano,text="Choose Key",font = ('Comic Sans MS',24))
leftText.grid(row=0, column=0, columnspan=7)

buttonLabels = ('A','B','C','D','E','F','G','A#/Bb','F#/Gb','C#/Db','G#/Ab')

for i,key in enumerate (buttonLabels):
    button = tk.Button(piano,text = key,command= lambda key=key: insertelm(key), height=1,width=10)
    button.grid(row=1, column=i, padx=1, pady=1)

status()

def check_music():
    while True:
        for event in pygame.event.get():
            if event.type == SONG_END:
                # Switch track when a song ends
                track = not track
                if(track == False):
                    pygame.mixer.music.load('Audio1.wav')
                else:
                    pygame.mixer.music.load('Audio2.wav')
                pygame.mixer.music.play()
                keyspressedArray.clear()
                with open('keys.txt', 'w') as f:
                    f.write('')

music_thread = threading.Thread(target=check_music)
music_thread.start()

root.mainloop()









