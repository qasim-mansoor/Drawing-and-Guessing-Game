#!/usr/local/bin/python
# coding: utf-8

from tkinter import *
from tkinter import messagebox
import socket
from threading import Thread
import sys
import time
import ast
import os
import platform
from textwrap import dedent
from PIL import Image
from PIL import ImageTk

def ClearScreen(): # Clears the screen.
    os.system("cls")

class GameScreen:
    def __init__(self, playerName, servPort, servIP):

        # SETTINGS:
        self.paintColor = "black"
        self.defaultColor = "black"
        self.playerName = playerName
        self.paintModeOn = False
        self.old_x = None
        self.old_y = None

        # SOCKET STUFF:
        self.servIP = servIP
        print(f"servIP from startScr: {self.servIP}\n")
        self.servPort = int(servPort)
        print(f"servPort from startScr: {self.servPort}\n")
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"Socket created: {self.sock}\n")
        except:
            print("Failed to create socket...\n")
        try:
            self.sock.connect((self.servIP, self.servPort))
            print(f"Connected to {self.servIP} on port {self.servPort}!\n")
            try:
                self.sendMsg = "SN//"+playerName
                self.sendMsgNow()
            except:
                print("Failed to send playerName...\n")
        except:
            print("Connection to server failed...\n")

        # MSG STUFF:
        self.msg = None
        self.msgParts = None
        self.msgType = None
        self.msgName = None
        self.msgValue = None
        self.counter = 71
        self.running = False

        # TKINTER STUFF:
        self.window = Tk()

        # Menu bar:
        self.menubar = Menu(self.window)
        self.window.config(menu = self.menubar)
        self.gamemenu = Menu(self.menubar)
        self.currentMenu = Menu(self.menubar)
        self.menubar.add_cascade(label = "Game", menu = self.gamemenu)
        self.gamemenu.add_cascade(label = "Current game", menu = self.currentMenu)
        self.currentMenu.add_command(label = "New word - You paint!", command = self.newWord)
        self.currentMenu.add_command(label = "Change name", command = self.changeName)
        self.currentMenu.add_command(label = "Cheat", command = self.cheat)
        self.gamemenu.add_command(label = "Quit", command = self.onExit)

        # Main window:
        self.window.title('Draw This!')
        self.window.geometry('{}x{}'.format(810, 617))
        self.top_frame = Frame(self.window, bg='grey', width=800, height=50, pady=3)
        self.center = Frame(self.window, bg='black', width=800, height=40, padx=0, pady=3)
        self.btm_frame = Frame(self.window, bg='black', width=800, height=45, pady=0)
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.top_frame.grid(row=0, sticky="ew")
        self.center.grid(row=1, sticky="nsew")
        self.btm_frame.grid(row=3, sticky="ew")
        self.center.grid_rowconfigure(0, weight=0)
        self.center.grid_columnconfigure(1, weight=0)
        self.ctr_left = Frame(self.center, bg='grey', width=500, height=500, padx=0, pady=0)
        self.ctr_right = Frame(self.center, bg='black', width=300, height=300, padx=3, pady=0)
        self.ctr_left.grid(row=0, column=0, sticky="ns")
        self.ctr_right.grid(row=0, column=2, sticky="ns")
        self.ctr_r_top = Frame(self.ctr_right, bg='grey', width=300, height=188, padx=0, pady=0, borderwidth=2, relief="groove")
        self.ctr_r_btm = Frame(self.ctr_right, bg='grey', width=300, height=318, padx=0, pady=0, borderwidth=2, relief="groove")
        self.ctr_r_top.grid_propagate(False)
        self.ctr_r_btm.grid_propagate(False)
        self.ctr_r_top.grid(row=0, column=0, sticky="ns")
        self.ctr_r_btm.grid(row=1, column=0, sticky="ns")
        self.btm_left = Frame(self.btm_frame, bg='grey', width=508, height=50, padx=0, pady=0)
        self.btm_right = Frame(self.btm_frame, bg='black', width=306, height=50, padx=0, pady=0)
        self.btm_left.grid_propagate(False)
        self.btm_left.grid(row=0, column=0, sticky="ns")
        self.btm_right.grid(row=0, column=1, sticky="ne")
        self.c = Canvas(self.ctr_left, bg='white', width=500, height=500)
        self.c.grid(row=0, rowspan=5, column=0, columnspan=5)
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)
        self.upperBox = Text(self.ctr_r_top, bg='navy blue', width=41, height=12)
        self.textbox = Text(self.ctr_r_btm, bg='white', width=41, height=21)
        self.upperBox.grid(row=0, column=0)
        self.textbox.grid(row=0, column=0)
        self.entrybox = Text(self.btm_right, bg='white', width=41, height=3, borderwidth=1, relief="sunken")
        self.entrybox.grid(row=2, column=0)
        self.entrybox.bind("<Return>", self.pressedEnter)
        self.clearButton = Button(self.btm_left, text='Clear', command=self.eraseCanvas)
        self.clearButton.grid(row=0, column=0)

        ######## For Colour Panel #############
        self.blackbutton = Button(self.ctr_r_top, height = 1, width = 3, bg = 'black', command = lambda: self.changeColour("black"), borderwidth=0, relief=SUNKEN, activebackground="black")
        self.blackbutton.place(x=5,y=5)

        self.redbutton = Button(self.ctr_r_top, height = 1, width = 3, bg = 'red', command = lambda: self.changeColour("red"), borderwidth=0, relief=SUNKEN, activebackground="red")
        self.redbutton.place(x=33,y=5)

        self.yellowbutton = Button(self.ctr_r_top, height = 1, width = 3, bg = 'yellow', command = lambda: self.changeColour("yellow"), borderwidth=0, relief=SUNKEN, activebackground="yellow")
        self.yellowbutton.place(x=61,y=5)

        self.bluebutton = Button(self.ctr_r_top, height = 1, width = 3, bg = 'blue', command = lambda: self.changeColour("blue"), borderwidth=0, relief=SUNKEN, activebackground="blue")
        self.bluebutton.place(x=89,y=5)

        self.whitebutton = Button(self.ctr_r_top, height = 1, width = 3, bg = 'white', command = lambda: self.changeColour("white"), borderwidth=0, relief=SUNKEN, activebackground="white")
        self.whitebutton.place(x=117,y=5)

        self.purplebutton = Button(self.ctr_r_top, height = 1, width = 3, bg = 'purple', command = lambda: self.changeColour("purple"), borderwidth=0, relief=SUNKEN, activebackground="purple")
        self.purplebutton.place(x=145,y=5)

        self.greybutton = Button(self.ctr_r_top, height = 1, width = 3, bg = 'grey', command = lambda: self.changeColour("grey"), borderwidth=0, relief=SUNKEN, activebackground="grey")
        self.greybutton.place(x=173,y=5)

        self.purplebutton = Button(self.ctr_r_top, height = 1, width = 3, bg = 'pink', command = lambda: self.changeColour("pink"), borderwidth=0, relief=SUNKEN, activebackground="pink")
        self.purplebutton.place(x=201,y=5)

        self.greenbutton = Button(self.ctr_r_top, height = 1, width = 3, bg = 'green', command = lambda: self.changeColour("green"), borderwidth=0, relief=SUNKEN, activebackground="green")
        self.greenbutton.place(x=229,y=5)

        ############# For timer ###############
        self.watch = Image.open("timer.png")
        self.watch = self.watch.resize((68,68), Image.ANTIALIAS)

        self.timer = ImageTk.PhotoImage(self.watch)
        
        self.img = Label(self.ctr_left, image = self.timer)
        self.img.place(x=435,y=0)

        self.lbl = Label(self.ctr_left, text = "00", fg = "black", bg = "white", font = ("Calibri",20))
        self.lbl.place(x = 453, y=20)
        # self.count()

        ######## Just for dev testing #########
        self.paintModeToggle = IntVar()
        self.paintModeBtn = Checkbutton(self.btm_left, text="Check to paint", variable=self.paintModeToggle)
        self.paintModeBtn.grid(row=0, column=1)
        #######################################

        # Start receiving data from server:
        self.receivethread = Thread(target=self.receive)
        self.receivethread.start()
        # self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    # def on_closing(self):
    #     if messagebox.askokcancel("Quit", "Do you want to quit?"):
    #         self.window.destroy()


    def counter_label(self):
        if self.running:
            if(self.counter == 71):
                display = '00'
            else:
                if self.counter < 10:
                    display = '0' + str(self.counter)
                else:
                    display = str(self.counter)

            self.lbl['text'] = display

            self.counter -= 1

            if(self.counter == -1):
                self.running = False
                self.resetTimer()
                self.paintModeBtn.deselect()
                self.paintModeOn = False
                self.inTheBox = "Time's up!\n"
                self.textbox.insert(END, self.inTheBox)
                self.textbox.see("end")
                sys.exit()

            time.sleep(0.25)
            # self.lbl.after(1000,self.counter_label())
            self.counter_label()
            

    def resetTimer(self):
        self.counter = 71
        self.lbl['text'] = "00"

    def startTimer(self):
        self.running = True
        self.countingThread = Thread(target = self.counter_label)
        self.countingThread.start()
    
    def changeColour(self, colour):
        self.paintColor = colour

    def onExit(self):
        self.window.destroy()
        sys.exit("Bye.")

    def changeName(self):
        self.inTheBox = "SN//YOUR-NAME-HERE"
        self.entrybox.insert(END, self.inTheBox)
        self.entrybox.see("end")

    def cheat(self):
        self.inTheBox = "//Ooooooh! I can see it now!"
        self.entrybox.insert(END, self.inTheBox)
        self.entrybox.see("end")

    def newWord(self):
        # self.inTheBox = "NW//"
        # self.entrybox.insert(END, self.inTheBox)
        # self.entrybox.see("end")
        # self.pressedEnter
        if(self.counter != 71):
            self.inTheBox = "Someone is already drawing.\n Wait your turn.\n"
            self.textbox.insert(END, self.inTheBox)
            self.textbox.see("end")
        else:
            self.sendMsg = "NW//"
            self.sendMsgNow()

    def receive(self):
        while True:
            try:
                self.msg = self.sock.recv(1024)
                self.msgParts = self.msg.decode('utf8').split(":")
                if len(self.msgParts) == 3:
                    self.msgType = self.msgParts[0]
                    self.msgName = self.msgParts[1]
                    self.msgValue = self.msgParts[2]
                    self.msgRouter()
                else:
                    continue
            except:
                print("Receive error")

    def pressedEnter(self, event):
        self.sendMsg = self.entrybox.get("1.0",END).strip()
        if self.sendMsg:
            self.sendMsgNow()
        self.entrybox.delete(1.0, END)

    def sendMsgNow(self):
        self.sock.send(str(self.sendMsg).encode('utf8'))

    def msgRouter(self):
        if self.msgType == "CO":
            # msgValue: Paint Coordinates
            
            if not self.paintModeOn:
                self.recreatePaint()

        if self.msgType == "GS":
            # msgValue: Word Guess
            self.inTheBox = f"{self.msgName} made a guess: {self.msgValue}\n"
            self.textbox.insert(END, self.inTheBox)
            self.textbox.see("end")

        if self.msgType == "//":
            # msgValue: Chat Comment
            self.inTheBox = f"// {self.msgName}: {self.msgValue}\n"
            self.textbox.insert(END, self.inTheBox)
            self.textbox.see("end")

        if self.msgType == "RG":
            # msgValue: Right Word Guess
            self.inTheBox = f"{self.msgName} has guessed the word!\n"
            self.textbox.insert(END, self.inTheBox)
            self.textbox.see("end")

        if self.msgType == "PT":
            # msgValue: Points
            pass # Not implemented yet.

        if self.msgType == "MS":
            # msgValue: Misc. Server Notice
            self.inTheBox = f"Server: {self.msgValue}\n"
            self.textbox.insert(END, self.inTheBox)
            self.textbox.see("end")

        if self.msgType == "CH":
            # msgValue: Cheat!
            
            if self.msgName == self.playerName:
                self.sendMsg = "SN//"+self.playerName+"(cheater)"
                self.sendMsgNow()
                self.inTheBox = self.msgValue
                self.entrybox.insert(END, self.inTheBox)
                self.entrybox.see("end")

        if self.msgType == "NW":
            # msgValue: New Word!
            # Turns off paintMode for everyone and enables it for the named player.
            self.paintColor = "black"
            self.eraseCanvas()
            self.startTimer()
            if self.msgName == self.playerName:
                self.paintModeBtn.select()
                self.inTheBox = str(self.msgName + ", it's your time to paint!\nThe word is: " + self.msgValue)
                self.textbox.insert(END, self.inTheBox)
                self.textbox.see("end")
            else:
                self.paintModeBtn.deselect()
                self.paintModeOn = False


    def paint(self, event):
        if self.paintModeToggle.get() == 1:
            self.paintModeOn = True
        else:
            self.paintModeOn = False
        if self.paintModeOn:
            if self.old_x and self.old_y:
                self.c.create_line(self.old_x, self.old_y, event.x, event.y, width=4, fill=self.paintColor)
            self.sendMsgValue = [self.old_x, self.old_y, event.x, event.y, self.paintColor]
            self.old_x = event.x
            self.old_y = event.y
            self.sendMsg = ("CO//"+str(self.sendMsgValue))
            self.sendMsgNow()

    def reset(self, event):
    # Stop painting when mouse butten is no longer pressed
        self.old_x, self.old_y = None, None

    def recreatePaint(self):
        try:
            self.coords = ast.literal_eval(self.msgValue)
        except:
            print("Unable to receive paint data")
        try:
            self.x1, self.y1, self.x2, self.y2, self.paintColor = self.coords[0], self.coords[1], self.coords[2], self.coords[3], self.coords[4]
        except:
            print("Unable to recreate paint data")
        if self.paintColor != "clear":
            self.c.create_line(self.x1, self.y1, self.x2, self.y2, width=4, fill=self.paintColor) 
        else:
            self.eraseCanvas()
            self.paintColor = "black"

    def eraseCanvas(self):
        if self.paintModeOn: # If the player is currently painting, this clears everyone else's canvas.
            self.c.delete("all") # Clear the canvas
            self.sendMsgValue = [0,0,0,0,"clear"] # I didn't want to over-complicate things, so the
                                                  # screen-clearing command pretends to be a color.
            self.sendMsg = ("CO//"+str(self.sendMsgValue)) # Telling the server it's drawing stuff with "CO"
            self.sendMsgNow()
            self.paintColor = self.defaultColor
        else:
            self.c.delete("all") # Clear the canvas

class ShowStartScreen():
    def __init__(self):
        ClearScreen()
        self.startScreen = Tk()
        self.label1 = Label(self.startScreen, text="Welcome to Draw This!\n\n To connect to a game server, "
                                                   "fill in the fields and press [Join Game]:\n\nServer IP:")
        self.label1.grid(row=1, column=1)
        self.defaultIP = StringVar(self.startScreen, value='')
        self.entryIP = Entry(self.startScreen, textvariable=self.defaultIP)
        self.entryIP.grid(row=2, column=1)

        self.label2 = Label(self.startScreen, text="Server Port:")
        self.label2.grid(row=3, column=1)
        self.entryPort = Entry(self.startScreen)
        self.entryPort.grid(row=4, column=1)

        self.label3 = Label(self.startScreen, text="Your Name:")
        self.label3.grid(row=5, column=1)
        self.entryName = Entry(self.startScreen)
        self.entryName.grid(row=6, column=1)

        self.joinBtn = Button(self.startScreen, text='Join Game', command=self.onJoin)
        self.joinBtn.grid(row=7, column=1)

        self.startScreen.mainloop()

    def onJoin(self):
        self.servIP = self.entryIP.get()
        self.servPort = self.entryPort.get()
        self.playerName = self.entryName.get()
        self.startScreen.destroy()
        newGameScr = GameScreen(servIP=self.servIP, servPort=self.servPort, playerName=self.playerName)

startScr = ShowStartScreen()