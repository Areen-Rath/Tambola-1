import socket
from tkinter import *
from threading import Thread
import random
from PIL import ImageTk, Image

SERVER = None
IP_ADDRESS = None
PORT = None

player_name = None

name_window = None
name_entry = None

canvas1 = None

def setup():
    global SERVER
    global IP_ADDRESS
    global PORT

    IP_ADDRESS = "127.0.0.1"
    PORT = 6000

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    thread = Thread(target = received_msg)
    thread.start()

def received_msg():
    global SERVER

    while True:
        msg = SERVER.recv(2048).decode()

        if "player_type" in msg:
            recv_msg = eval(msg)
            playerType = recv_msg["player_type"]
        elif "player_names" in msg:
            players = eval(msg)
            players = players["player_names"]
            for p in players:
                if(p["type"] == 'player1'):
                    player1Name = p['name']
                if(p["type"] == 'player2'):
                    player2Name = p['name']

def ask_player_name():
    global player_name
    global name_window
    global name_entry
    global canvas1

    name_window = Tk()
    name_window.title("Tambola Family Fun")
    name_window.geometry("800x600")

    screen_width = name_window.winfo_screenwidth()
    screen_height = name_window.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas1 = Canvas(name_window, width = 500, height = 500)
    canvas1.pack(fill = "both", expand = True)
    canvas1.create_image(0, 0, image = bg, anchor = "nw")
    canvas1.create_text(
        screen_width/4.5,
        screen_height/8,
        text = "Enter Name",
        font = ("Chalkboard SE", 60),
        fill = "black"
    )
    
    name_entry = Entry(
        name_window,
        width = 15,
        justify = "center",
        font = ("Chalkboard SE", 30),
        bd = 5,
        bg = "white"
    )
    name_entry.place(x = screen_width/7, y = screen_height/5.5)

    button = Button(
        name_window,
        text = "Save",
        font = ("Chalkboard SE", 30),
        width = 11,
        command = save_name,
        height = 2,
        bg = "#80deea",
        bd = 3
    )
    button.place(x = screen_width/6, y = screen_height/4)

    name_window.resizable(True, True)
    name_window.mainloop()

def save_name():
    global SERVER
    global player_name
    global name_window
    global name_entry

    player_name = name_entry.get()
    name_entry.delete(0, END)
    name_window.destroy()

    SERVER.send(player_name.encode())