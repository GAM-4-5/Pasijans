      from tkinter import *
import webbrowser
import random
from PIL import Image, ImageTk
#stvaranje početnog izbornika
class Menu(Tk, object):
    def __init__(self):
        self.root=Tk()
        self.root.title("Menu")
        self.frame=Frame(self.root)
        self.frame.pack()
        self.play=Button(self.frame, text="Play", command=self.play_choice)
        self.play.pack()
        self.rules=Button(self.frame, text="Rules", command=self.rules_book)
        self.rules.pack()
        self.cancel=Button(self.frame, text="Cancel", command=self.root.destroy)
        self.cancel.pack()
    def rules_book(self):
        #txt file s pravilima igre
        webbrowser.open("rules.txt")
    def play_choice(self):
        #novi prozor s odabirom načina igre
        self.new=Toplevel()
        play=Play(self.new)

#u ovom prozoru možete odabrati opciju za vući 3 karte ili 1 kartu
class Play(Toplevel, object):
    def __init__(self, root):
        self.root=root
        self.root.title("Play")
        self.cards=IntVar(self.root, value=1)
        self.frame=Frame(self.root)
        self.frame.pack()
        #3 karte
        self.cards3=Radiobutton(self.frame, text="draw 3 cards", variable=self.cards, value=3)
        self.cards3.pack()
        #1 karta
        self.card1=Radiobutton(self.frame, text="draw 1 card", variable=self.cards, value=1)
        self.card1.pack()
        self.start=Button(self.frame, text="start", command=self.start)
        self.start.pack()
    def start(self):
        # u slučaju da opcija nije odbrana start gumb nema funkciju
        if self.cards!=0:
            self.new=Toplevel()
            game=Game(self.new)
            

#prozorčić za igru
class Game(Toplevel, object):
    def __init__(self, master):
        self.master=master
        self.master.title("Pasijans")
        self.frame=Frame(self.master, width=720, height=600)
        self.frame.pack()
        #lista svih karata: slovo označava grupu,a broj broj karte od asa do kralja
        self.list=["s01", "s02", "s03", "s04", "s05", "s06", "s07", "s08", "s09", "s10", "s11", "s12", "s13",\
                   "h01", "h02", "h03", "h04", "h05", "h06", "h07", "h08", "h09", "h10", "h11", "h12", "h13",\
                   "d01", "d02", "d03", "d04", "d05", "d06", "d07", "d08", "d09", "d10", "d11", "d12", "d13",\
                   "c01", "c02", "c03", "c04", "c05", "c06", "c07", "c08", "c09", "c10", "c11", "c12", "c13"]
        # stvaranje podloge s mjerama i točno pozicionirnim kartama
        rows=[[0 for i in range (13)]for j in range (7)]
        y=140
        for i in range (0, 7):
            b=7-i
            y+=10
            x=490
            for j in range (0, b):
                k=random.choice(self.list)
                c=Button(self.frame, text=k)
                img=Image.open(k+".png")
                image=ImageTk.PhotoImage(img, master=self.master)
                c.configure(image=image)
                c.place(x=x, y=y)
                rows[j][i]=c
                x-=80
        for i in range (0, 7):
            for j in range (0, 12):
                if rows[i][j]!=0 and rows[i][j+1]!=0:
                    rows[i][j].configure(state=DISABLED)
