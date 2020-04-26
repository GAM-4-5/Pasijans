from tkinter import *
import webbrowser
import random
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
        self.cards=IntVar(self.root, value=0)
    def rules_book(self):
        #txt file s pravilima igre
        webbrowser.open("rules.txt")
    def play_choice(self):
        #novi prozor s odabirom načina igre
        play=Play(self.cards)

#u ovom prozoru možete odabrati opciju za vući 3 karte ili 1 kartu
class Play(Tk, object):
    def __init__(self, cards):
        self.root=Tk()
        self.root.title("Play")
        self.cards=cards
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
            game=Game()

#prozorčić za igru
class Game(Tk, object):
    def __init__(self):
        self.root=Tk()
        self.root.title("Pasijans")
        self.frame=Frame(self.root, width=720, height=600)
        self.frame.pack()
        #lista svih karata: slovo označava grupu,a broj broj karte od asa do kralja
        self.list=["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "s12", "s13"\
                   "h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9", "h10", "h11", "h12", "h13"\
                   "d1", "d2", "d3", "d4", "d5", "d6", "d7", "d8", "d9", "d10", "d11", "d12", "d13"\
                   "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11", "c12", "c13"]
        # stvaranje podloge s mjerama i točno pozicionirnim kartama
        y=130
        for i in range (0, 7):
            b=7-i
            y+=5
            x=490
            for j in range (0, b):
                k=random.choice(self.list)
                self.list.remove(k)
                c=Button(self.root, text=k)
                c.place(x=x, y=y, height=125, width=70)
                x-=80
                
        
            
   

pasijans=Menu()
