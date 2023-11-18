
import tkinter as tk
import pygame

playing = False

pygame.mixer.init()

pygame.mixer.music.load('UIpackage/Audio1.wav')
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
    
# def play():
#     music.play()

def stop():
    global playing
    pygame.mixer.music.stop()
    playing = False

# def pause():
#     music.pause()


label.pack()
buttonFrame = tk.Frame(root)

buttonFrame.pack(side=tk.BOTTOM, pady=40)

playButton = tk.Button(buttonFrame, text = "PLAY", command= playandPause, height = 5, width = 20)
#pauseButton = tk.Button(buttonFrame, text = "PAUSE", command= pause, height = 5, width = 20)
stopButton = tk.Button(buttonFrame, text = "STOP", command= stop, height = 5, width = 20)


playButton.pack(side=tk.LEFT, padx=10)  
#pauseButton.pack(side=tk.LEFT, padx=10)
stopButton.pack(side=tk.LEFT, padx=10)


root.mainloop()






