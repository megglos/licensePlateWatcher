import sys
import time
import logging
import csv
import re
from tkinter import *
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from collections import deque
from datetime import datetime
import time
import os
from apscheduler.schedulers.background import BackgroundScheduler

class LastRowReader():

    @staticmethod
    def get_last_row():
        with open(self.fileName, 'rt') as f:
            return deque(csv.reader(f, delimiter=";"), 1)[0]

    def readFirstRow(self):
        print(self.fileName)
        self.last_pos = 0
        with open(self.fileName, 'rt') as f:
            for line in f:
                self.last_pos+=1
        with open(self.fileName, 'rt') as f:
            value = deque(csv.reader(f, delimiter=";"), 1)[0]
            self.plateVar.set(value[2])

    def readNewRow(self):
        count = 0
        with open(self.fileName, 'rt') as f:
            for line in f:
                count+=1
        if count > self.last_pos:
            self.last_pos = count
        with open(self.fileName, 'rt') as f:
            value = deque(csv.reader(f, delimiter=";"), 1)[0]
            self.plateVar.set(value[2])

    def __call__(self):
        self.readNewRow()
        self.countVar.set(self.last_pos)

    def __init__(self, fileName, plateVar, countVar):
        self.fileName = fileName
        self.plateVar = plateVar
        self.countVar = countVar
        self.readFirstRow()
        self.countVar.set(self.last_pos)

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    width, height = 1000, 1000
    bg, fg= "#E20074", "#FFFFFF"

    root = Tk()
    canvas = Canvas(root, width=width, height=height, bg=bg)
    canvas.pack(expand=YES, fill=BOTH) 
    countText = StringVar()
    plateText = StringVar()
    plateLabel = Label(canvas, text="Nummernschild", font = "Arial 44 bold", justify="center", bg=bg, fg=fg)
    plateLabel.pack()
    plateValue = Label(canvas, textvariable=plateText, font = "Arial 56", justify="center", bg=bg, fg=fg)
    plateValue.pack()
    countValue = Label(canvas, textvariable=countText, font = "Arial 56", justify="center", bg=bg, fg=fg)
    countValue.pack()
    canvas.create_window(width/2, height-160, window=plateLabel)
    canvas.create_window(width/2, height-88, window=plateValue)
    canvas.create_window(50, 50, window=countValue)

    reader = LastRowReader("csv.csv", plateText, countText)

    scheduler = BackgroundScheduler()
    scheduler.add_job(reader, 'interval', seconds=3)
    scheduler.start()

    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        root.mainloop()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()  # Not strictly necessary if daemonic mode is enabled but should be done if possible