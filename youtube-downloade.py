import re
import time
import pytube
import threading
import tkinter as tk
from pathlib import Path
from tkinter.ttk import *
from pytube import YouTube
from tkinter import messagebox


class Youtube(object):
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Youtube Downloader")
        self.window.geometry("850x400+320+200")
        self.window.resizable(False, False)
        self.window.configure(padx=30, pady=20)
        self.textvariables()
        self.icon()
        self.addInputWidgets()
        self.addButton()
        self.table()

    def textvariables(self):
        self.fileVar = tk.StringVar()
        self.itemsVar = tk.StringVar()
        self.fileDirVar = tk.StringVar()

    def getstrings(self):
        self.items['title'] = Label(self.tableframe, text="-", font=("calibri", 12), borderwidth=2,  width=25)
        self.items['format'] = Label(self.tableframe, text=self.formatList.get(), font=("calibri", 12),
                                     borderwidth=2, width=14)
        self.items['size'] = Label(self.tableframe, text="-", font=("calibri", 12))
        self.items['resolution'] = Label(
            self.tableframe, text=self.resolution.get(),
            font=("calibri", 12),
            borderwidth=2, width=14)
        self.items['progress'] = Progressbar(self.tableframe, orient="horizontal", length=250, mode='determinate')
        num = 0
        if self.fileEntry.get() != '' and self.match(self.fileEntry.get()) != False:
            for itemkeys in self.items.values():
                itemkeys.grid(column=num, row=1)
                itemkeys.update_idletasks()
                num += 1
            print(self.items['title'].winfo_ismapped())
            self.createThread()

        else:
            messagebox.showerror("Invalid url!", "Please provide a valid url")

    def match(self, caller):
        match = re.compile(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*")
        match = match.search(caller)
        if match == None:
            return False
        else:
            return True

    def addInputWidgets(self):
        makeLabel = Label(self.window, text='Enter Video url:', font=("calibri", 19))
        makeLabel.grid(column=0, row=0, sticky=tk.W, pady=10)
        homeDir = Path.home()
        downloadsDir = homeDir / 'Downloads'
        self.fileEntry = Entry(self.window, textvariable=self.fileVar, width=63, font=("calibri", 17))
        self.fileEntry.grid(column=0, row=1, pady=5, ipady=20, sticky=tk.W, columnspan=2)
        self.fileEntry.focus()
        self.fileDirectory = Combobox(self.frame, values=[homeDir, downloadsDir], width=50)
        self.fileDirectory.grid(column=1, row=0, ipady=5, padx=20)
        self.fileDirectory.current(1)
        self.formatList = Combobox(self.frame, width=15, values=['mp4', 'mp3'])
        self.formatList.grid(column=2, row=0, ipady=5, padx=(28, 25), stick=tk.E)
        self.formatList.current(0)
        self.resolution = Combobox(self.frame, width=15, values=["1080p", "720p", "480p", "360p"])
        self.resolution.grid(column=3, row=0, ipady=5, padx=(0, 10), stick=tk.E)
        self.resolution.current(1)

    def icon(self):
        self.frame = tk.LabelFrame(self.window, highlightthickness=0, borderwidth=0)
        self.frame.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        self.fileIcon = tk.PhotoImage(
            file="C:/Users/Dell/Desktop/youtube gui/icons8-folder-48.png", width=37, height=35)
        Label(self.frame, image=self.fileIcon).grid(column=0, row=0, sticky=tk.W, columnspan=1)

    def addButton(self):
        self.addfiles = Button(self.frame, text="add", command=self.getstrings)
        self.addfiles.grid(column=4, row=0, ipady=5)

    def table(self):
        self.tableframe = tk.LabelFrame(self.window, text='Download list', width=800, height=30, borderwidth=0, font=15)
        self.tableframe.grid(column=0, row=3, columnspan=2, sticky=tk.W, pady=10)
        itemNames = ("Title", "Extention", "Size", "resolution", "Percentage")
        for i in range(len(itemNames)):
            if i == 0:
                heading = Label(self.tableframe, text=itemNames[i], font=(
                    "Calibri", 12), borderwidth=2, relief="solid", width=10)
                heading.grid(column=i, row=0, ipadx=60)
            elif i == 1:
                heading = Label(self.tableframe, text=itemNames[i], font=("Calibri", 12), borderwidth=2, relief="solid")
                heading.grid(column=i, row=0, ipadx=26)
            elif i > 1 and i != (len(itemNames) - 1):
                heading = Label(self.tableframe, text=itemNames[i], font=("Calibri", 12), borderwidth=2, relief="solid")
                heading.grid(column=i, row=0, ipadx=26)
            else:
                heading = Label(self.tableframe, text=itemNames[i], font=("Calibri", 12), borderwidth=2, relief="solid")
                heading.grid(column=i, row=0, ipadx=85)
        self.items = {}

    def download(self):
        self.yVideo = YouTube(self.fileEntry.get(), on_progress_callback=self.progress,
                              on_complete_callback=self.downloaded)
        self.yVideoStream = self.yVideo.streams.filter(progressive=True, resolution=self.resolution.get())[0]
        print(type(self.yVideoStream), self.resolution.get())
        print(self.yVideoStream, self.resolution.get())
        self.videoSizeInBytes = self.yVideo.streams.filter(
            progressive=True, resolution=self.resolution.get())[0].filesize
        self.videoSize = self.videoSizeInBytes // 1000000
        print(self.yVideoStream.title[:12])
        self.items['title'].configure(text=self.yVideoStream.title[:5])
        self.items["size"].configure(text=(str(self.videoSize) + "MB"))
        self.fileEntry.delete(0, 'end')
        # print(type(Path(self.fileDirectory.get())))
        self.yVideoStream.download(Path(self.fileDirectory.get()))

    def progress(self, chunk=None, file_handler=None, bytes_remaining=None):
        progress_bar = self.items['progress']
        progress_bar['maximum'] = 100
        percent = (100 * (self.videoSizeInBytes - bytes_remaining)) / self.videoSizeInBytes
        progress_bar.start()
        for i in range(1):
            progress_bar['value'] = percent
            progress_bar.update()
            if percent == 100:
                progress_bar.stop()
                break
        print(percent)

    def downloaded(self):
        messagebox.showinfo('Download completed', f"Youtube video downloaded sucessfully!")

    def createThread(self):
        self.run_thread = threading.Thread(target=self.download)
        self.run_thread.setDaemon(True)
        self.run_thread.start()


youtube = Youtube()
youtube.window.mainloop()
