
import tkinter as tk
import pygame

track = False

playing = False

pygame.mixer.init()


if(track == False):
    pygame.mixer.music.load('UIpackage/Audio1.wav')
else:
    pygame.mixer.music.load('UIpackage/Audio2.wav')
root = tk.Tk()


root.geometry("900x600")
root.title("Listen to what your brain tells ya")
root.configure(bg='#191414')

label = tk.Label(root, text="Brainify", font= ('Comic Sans MS', 36), fg='white', bg='#191414')

def playandPause():
    global playing
    if playing:
        pygame.mixer.music.pause()
        playButton.config(text="PLAY",command=playandPause)
    else:
        pygame.mixer.music.play()
        playButton.config(text="PAUSE",command=playandPause)

    playing = not playing
    


def stop():
    global playing
    pygame.mixer.music.stop()
    playing = False
    playButton.config(text="PLAY",command=playandPause)


def status():
    global playing
    if pygame.mixer.music.get_busy() == False:
        playing = False
        playButton.config(text="PLAY",command=playandPause)
    root.after(1000, status)


label.pack()
buttonFrame = tk.Frame(root)

buttonFrame.pack(side=tk.BOTTOM, pady=40)

playButton = tk.Button(buttonFrame, text = "PLAY", command= playandPause, height = 5, width = 20)
stopButton = tk.Button(buttonFrame, text = "STOP", command= stop, height = 5, width = 20)


playButton.pack(side=tk.LEFT, padx=10)  
stopButton.pack(side=tk.LEFT, padx=10)

left = tk.Frame(root)
left.pack(side=tk.LEFT, padx=10)

leftText = tk.Label(left,text="Choose Key",font = ('Comic Sans MS',24))
leftText.pack()

buttonLabels = ('A','B','C','D','E','F','G','A#/Bb','F#/Gb','C#/Db','G#/Ab')

for key in buttonLabels:
    button = tk.Button(left,text = key,height=1,width=10)
    button.pack(pady=1)

status()
track = not track
root.mainloop()






