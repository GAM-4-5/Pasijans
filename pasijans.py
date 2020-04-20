from tkinter import *
import webbrowser
#stvaranje početnog izbornika
class Menu(Tk):
    def __init__(self, root):
        self.root=root
        self.root.title("Menu")
        self.frame=Frame(root)
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
        play=Play()


root=Tk()
pasijans=Menu(root)

pasijans.mainloop()

