#!/usr/bin/python3
# HDDNoSleep.py by Karel Dohnal
# TKinter GUI program for preventing selected drive going to sleep using simple Input operation every given second.

from tkinter import Tk
from tkinter import Frame
from tkinter import PhotoImage
from tkinter import StringVar
from tkinter import DoubleVar
from tkinter import BooleanVar
from tkinter import IntVar
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from time import sleep
import time
import os.path
import os

class HDDNoSleep():
        
    def __init__(self, master):  
        self.master = master
        master.title("HDD No Sleep")
        master.resizable(False, False)
        master.configure(background = "#e5e5e5")
        master.iconbitmap("hdd.ico")

        self.style = ttk.Style()
        self.style.configure("TFrame", background = "#e5e5e5")
        self.style.configure("TButton", background = "#e5e5e5")
        self.style.configure("TLabel", background = "#e5e5e5")
       
        self.timer = IntVar()
        self.counter = IntVar()
        self.inOperation = BooleanVar()
        self.inOperation = False  

        self.frame_select = ttk.Frame(master)
        self.frame_select.pack()
        self.frame_control = ttk.Frame(master)
        self.frame_control.pack()

        ttk.Label(self.frame_select, text = "Select drive:").grid(row = 0, column = 0, pady = 5, sticky = "w")
        ttk.Label(self.frame_select, text = "Input operation every:").grid(row = 1, column = 0, pady = 5, sticky = "w")
        ttk.Label(self.frame_select, text = "sec.").grid(row = 1, column = 2, pady = 5, sticky = "w")

        self.dl = StringVar()
        self.dl = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.drive = StringVar()
        self.drives = ['%s:\\' % d for d in self.dl if os.path.exists('%s:' % d)]
        self.comboDrive = ttk.Combobox(self.frame_select, textvariable = self.drive, width = 3)
        self.comboDrive.config(values = self.drives)
        self.comboDrive.grid(row = 0, column = 1, pady = 5)
        
        self.period = ttk.Entry(self.frame_select, width = 5)
        self.period.insert(0, "25")
        self.period.grid(row = 1, column = 1, pady = 5)
        
        self.progressVar = DoubleVar()
        self.progressbar = ttk.Progressbar(self.frame_control, length = 180, mode = 'determinate', maximum = 100.0, variable = self.progressVar)
        self.progressbar.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)

        self.startbutton = ttk.Button(self.frame_control, text = "Start", command = self.start_button)
        self.stopbutton = ttk.Button(self.frame_control, text = "Stop", command = self.stop_button, state = ["disabled"])
        self.startbutton.grid(row = 1, column = 0, padx = 5, pady = 5)
        self.stopbutton.grid(row = 1, column = 1, padx = 5, pady = 5)
    


    def start_button(self):
        try:
            self.timer = int(self.period.get())
        except:
            messagebox.showerror(title = "Error", message = "Only integer values are allowed for time period!")
            return
        if self.timer < 0: 
            messagebox.showerror(title = "Error", message = "Only positive values are allowed for time period!") 
            return
        if os.path.isdir(str(self.comboDrive.get())) is False:
            messagebox.showerror(title = "Error", message = "Invalid/unmounted drive selected.")
            return
        if os.path.isdir(str(self.comboDrive.get() + "temp\\")) is False:
            os.mkdir(str(self.comboDrive.get()) + "temp\\")
        self.counter = 0
        self.inOperation = True
        self.startbutton.state(["disabled"])
        self.stopbutton.state(["!disabled"])
        self.no_sleep_operation()
     

    def stop_button(self):
        self.progressVar.set(0.0)
        self.inOperation = False
        self.startbutton.state(["!disabled"])
        self.stopbutton.state(["disabled"])
        
    def no_sleep_operation(self):
        if (self.counter < self.timer) and self.inOperation:
            self.counter += 1
            self.progressVar.set(self.counter/self.timer*100)
            self.frame_control.update_idletasks()
            self.master.after(1000, self.no_sleep_operation)
        else:
            self.counter = 0
            if self.inOperation:
                self.input_operation()
                self.no_sleep_operation()
            else:
                return

    def input_operation(self):
        inputTime = datetime.now()
        inputPath = (str(self.comboDrive.get()) + "\\temp\\" + str(inputTime.strftime("%H-%M-%S")))
        f = open(str(inputPath) + ".txt","w+")
        f.close()
        os.remove(str(inputPath) + ".txt")

            
def main():            
    
    root = Tk()
    hddNoSleep = HDDNoSleep(root)
    root.mainloop()
    
    
if __name__ == "__main__": main()
