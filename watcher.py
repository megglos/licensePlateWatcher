import sys
import time
import logging
import csv
import re
from tkinter import *
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from collections import deque

class ReadLastRowOnModified(FileSystemEventHandler):
    def __init__(self, pattern, stringVar):
        self.prog = re.compile(pattern);
        self.stringVar = stringVar;

    @staticmethod
    def get_last_row(csv_filename):
        with open(csv_filename, 'rt') as f:
            return deque(csv.reader(f, delimiter=";"), 1)[0]

    def on_modified(self, event):
        if self.prog.match(event.src_path):
            newEntry = self.get_last_row(event.src_path)[2];
            print(newEntry)
            self.stringVar.set(newEntry);

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    width, height = 1000, 1000
    bg, fg= "#E20074", "#FFFFFF"

    root = Tk()
    canvas = Canvas(root, width=width, height=height, bg=bg)
    canvas.pack(expand=YES, fill=BOTH) 

    plateText = StringVar()
    #plateText.set("test")
    event_handler = ReadLastRowOnModified(".*\.csv", plateText)

    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    plateLabel = Label(canvas, text="Nummernschild", font = "Arial 44 bold", justify="center", bg=bg, fg=fg)
    plateLabel.pack()
    plateValue = Label(canvas, textvariable=plateText, font = "Arial 56", justify="center", bg=bg, fg=fg)
    plateValue.pack()
    canvas.create_window(width/2, height-160, window=plateLabel)
    canvas.create_window(width/2, height-88, window=plateValue)
    root.mainloop()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()