#!/usr/bin/python
import tkinter
import mpd
import time
import os
import subprocess
from tkinter import *
from tkinter.dialog import Dialog
from tkinter import commondialog
import tkinter as tk

from tkinter import Tk, Text, BOTH, W, N, E, S, RAISED, StringVar, Scale, Listbox
from ttk import Frame, Button, Label, Style, LabelFrame


class Example(Frame):

    #global rpi
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
        

    
        
        
    def initUI(self):

        self.MPDInitialize()
        self.parent.title("RaspiPlayer")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        #self.columnconfigure(1, weight=1)
        #self.columnconfigure(3, pad=7)
        #self.rowconfigure(3, weight=1)
        #self.rowconfigure(5, pad=7)
        
        #self.CurrentSongInfo()
        self.poll()
        
        titleframe=LabelFrame(self, width=200, height=70)
        titleframe.grid(row=0, column=0, columnspan=2)
        titleframe.grid_propagate(0)
        titlelbl = Label(titleframe, text="RaspPi Player", font=('Garamond',(20),'bold'))
        titlelbl.grid(row=0, column=0)
                
        
        PreviousButton = Button(self, text="Previous", command=self.PreviousClick)
        PreviousButton.grid(row=2, column=0)

        PlayButton = Button(self, text="Play", command=self.PlayClick)
        PlayButton.grid(row=2, column=1, padx=4)

        StopButton = Button(self, text="Stop", command=self.StopClick)
        StopButton.grid(row=2, column=2)

        PauseButton = Button(self, text="Pause", command=self.PauseClick)
        PauseButton.grid(row=2, column=3, padx=4)
        
        NextButton = Button(self, text="Next", command=self.NextClick)
        NextButton.grid(row=2, column=4)

        UploadButton = Button(self, text="Upload", command=self.UploadClick)
        UploadButton.grid(row=2, column=5, padx=4)

        VolumeBar = Scale(self, from_=0, to=100, orient="horizontal", label="Volume", command=self.VolumeBar)
        VolumeBar.grid(row=2, column=6, padx=5)
        VolumeBar.set(50)

        
    def VolumeBar(self, val):
        rpi.setvol(val)
 
    def CurrentSongInfo(self):

        def OnPlayListClick(event):
            newsongtitle=PlayList.get(PlayList.curselection())
            for i in range(0,int(length)):
                try:
                    if (songlist[i]['title']==newsongtitle):
                        newsongindex=i;
                        break
                except KeyError:
                    if (songlist[i]['artist']==newsongtitle):
                        newsongindex=i;
                        break
            
            rpi.playid(songlist[newsongindex]['id'])
            rpi.update()

        
        def ftime(time):
            time = int(time)
            return str(int(time/60)) + ':' + '%.2d' % int(time%60)

        self.currentsong = StringVar(self)
        rpi.update()
        cs = rpi.currentsong()
        ss = rpi.status()
        try:
            artist = cs['artist']
        except KeyError:
            artist = '**'
        try:
            album = cs['album']
        except KeyError:
            album = '**'
        try:
            title = cs['title']
        except KeyError:
            title = '**'
        #track = cs['track']
        try:
            num = str(int(ss['song'])+1)
        except KeyError:
            num = ''
        length = ss['playlistlength']
        try:
            cur_time = ftime(ss['time'].split(':')[0])
        except KeyError:
            cur_time = "0:00"
        # total time
        try:
            total_time = ftime(cs['time'])
        except KeyError:
            total_time = "0:00"
        self.currentsong.set(artist + ' - ' + title + '\n' + album + '\n' + num + '/' + length + '\n\n' + cur_time + '/' + total_time)
        lblframe=LabelFrame(self, text="Now Playing", width=600, height=100)
        lblframe.grid(row=1, column=0, columnspan=7, pady=40)
        #lblframe.grid(row=0, column=1)
        lblframe.grid_propagate(0)
        lbl = Label(lblframe, textvariable=self.currentsong, font=('Tahoma',(9)))
        lbl.grid(row=1, column=0)
        lbl.grid_propagate(0)
        
        
        PlayList = Listbox(self, width=80)
        PlayList.grid(row=3,column=1, columnspan=5, padx=20)
        

        songlist = rpi.playlistid()
        for i in range(0,int(length)):
            try:
                PlayList.insert(i,songlist[i]['title'])
            except KeyError:
                PlayList.insert(i,songlist[i]['artist'])
            if (len(cs)!=0):
                if (cs['id']==songlist[i]['id']):
                    PlayList.itemconfig(i,background='blue',foreground='white')

        PlayList.bind('<<ListboxSelect>>', OnPlayListClick)
                    


    def MPDInitialize(self):
        global rpi
        rpi = mpd.MPDClient()
        rpi.connect('10.184.2.31', 6600)
        time.sleep(2)
        print('Correct')
        print(rpi.playlist())

    def PreviousClick(self):
        rpi.previous()
        rpi.play()
        

    def PlayClick(self):
        rpi.play()
        
    def StopClick(self):
        rpi.stop()

    def PauseClick(self):
        rpi.pause()

    def NextClick(self):
        rpi.next()
        rpi.play()
        

    def UploadClick(self):
        #rpi.stop()
        filename = filedialog.askopenfilename(title='Select an audio file')
        #print(filename.split('/'))
        separator='\\'
        filepath = separator.join(filename.split('/'))
        print(filepath)
        #NewSongName='Ondonde.mp3'
        subprocess.call('pscp -pw raspberry "' + filepath + '" pi@10.184.2.31:/home/pi/music', shell=True)
        print(filename.split('/')[len(filename.split('/'))-1])
        songtobeplayed = filename.split('/')[len(filename.split('/'))-1]
        #Id=rpi.addid(filename.split('/')[len(filename.split('/'))-1])
        dabang= str(filename.split('/')[len(filename.split('/'))-1])
        Id=rpi.addid(dabang)
        #Id=rpi.addid(songtobeplayed)
        print(Id)
        rpi.update()
        rpi.playid(Id)
        

    def poll(self):
        self.CurrentSongInfo()
        #print(self.counter)
        self.after(500, self.poll)
              

def main():
  
    root = Tk()
    root.geometry("750x580")
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  
