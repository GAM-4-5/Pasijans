from tkinter import *
import webbrowser
import random
from PIL import Image, ImageTk
from tkinter.messagebox import showinfo
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
        play=Play()

#u ovom prozoru možete odabrati opciju za vući 3 karte ili 1 kartu
class Play(Toplevel, object):
    def __init__(self):
        self.root=Toplevel()
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
        #gumb za početak igre
        self.start=Button(self.frame, text="start", command=self.start)
        self.start.pack()
    def start(self):
        #novi prozor u kojem je igra
        game=Game(self.cards, self.root)
            

#prozor za igru
class Game(Toplevel):
    def __init__(self, cards, play):
        play.destroy()
        self.master=Toplevel()
        self.cards=cards
        self.master.title("GAM Pasijans")
        self.frame=Frame(self.master, width=720, height=600, bg="green")
        self.frame.pack()
        #lista svih karata: prvoslovo označava boju, drugo slovo označava grupu, a broj broj karte od asa do kralja
        self.list=["bs01", "bs02", "bs03", "bs04", "bs05", "bs06", "bs07", "bs08", "bs09", "bs10", "bs11", "bs12", "bs13",\
                   "rh01", "rh02", "rh03", "rh04", "rh05", "rh06", "rh07", "rh08", "rh09", "rh10", "rh11", "rh12", "rh13",\
                   "rd01", "rd02", "rd03", "rd04", "rd05", "rd06", "rd07", "rd08", "rd09", "rd10", "rd11", "rd12", "rd13",\
                   "bc01", "bc02", "bc03", "bc04", "bc05", "bc06", "bc07", "bc08", "bc09", "bc10", "bc11", "bc12", "bc13"]
        #slika karte koja je okrenuta na poleđinu
        self.cardb=Image.open("cardb.png")
        self.cardb=self.cardb.resize((70,100), Image.ANTIALIAS)
        # stvaranje podloge s mjerama i točno pozicionirnim kartama
        self.rows=[[]for j in range (7)]
        y=115
        for i in range (0, 7):
            b=7-i
            y+=20
            x=490
            for j in range (0, b):
                k=random.choice(self.list)
                self.list.remove(k)
                #ime/tekst karte je povezan s nazivom slike te iste karte
                img=Image.open(k[1:]+".png")
                image=ImageTk.PhotoImage(img, master=self.frame)
                c=Button(self.frame, text=k, image=image, command=lambda l=k : self.rowcards(l))
                c.image=image
                c.place(x=x, y=y, height=100, width=70)
                self.rows[j].append(c)
                x-=80
        #isključivanje svih karata koje nisu na zadnjem mjestu
        for i in range (0, 7):
            for j in range (len(self.rows[i])):
                if self.rows[i][j]!=self.rows[i][-1]:
                    image=ImageTk.PhotoImage(self.cardb, master=self.frame)
                    self.rows[i][j].configure(state=DISABLED, image=image)
                    self.rows[i][j].image=image
                    
        #4 seta za slaganje karata
        self.sets=[[] for j in range (4)]
        #špil s okrenutim i neokrenutim kartama
        self.deck=[[], []]
        #gumb za okrenut špil
        self.re=Button(self.frame, text="reset deck", command=lambda: self.shuffle())
        self.re.place(x=570, y=10, height=100, width=70)
        self.deck[0].append(self.re)
        #postavljanje špila
        for i in range (len(self.list)):
            k=random.choice(self.list)
            self.list.remove(k)
            image=ImageTk.PhotoImage(self.cardb, master=self.frame)
            c=Button(self.frame, text=k, image=image)
            c.image=image
            c.place(x=570, y=10, height=100, width=70)
            c.lift()
            self.deck[0].append(c)
            c.configure(command=lambda : self.deckc())
            
    #naredba za neokrenute karte u špilu, okreću se i dobivaju drugu naredbu
    def deckc(self):
        #postupak će se ponoviti 1 ili 3 puta ocisno o zadanoj vrijednosti
        for i in range(self.cards.get()):
            # u slučaju da se broj vrtnji ne poklopi s brojem karti, špil će se automatski okrenuti
            if len(self.deck[0])==1:
                self.shuffle()
            c=self.deck[0][-1]
            #ovo će pomaknuti 2 prošle okrenute karte u lijevo
            for j in range(2, 0, -1):
                if len(self.deck[1])-j>=0:
                    self.deck[1][-j].place_forget()
                    self.deck[1][-j].place(x=(490-20*j), y=10, height=100, width=70)
                    self.deck[1][-j].configure(state=DISABLED)
                    self.deck[1][-j].lift()
            k=c.cget("text")
            self.deck[0].remove(c)
            self.deck[1].append(c)
            c.place_forget()
            c.place(x=490, y=10, height=100, width=70)
            img=Image.open(k[1:]+".png")
            image=ImageTk.PhotoImage(img, master=self.frame)
            c.configure(image=image, command=lambda l=c: self.deckcard(c))
            c.image=image
            c.lift()

    #naredba za okrenute karte u špilu                   
    def deckcard (self, c):
            k=c.cget("text")
    
            for i in range (4):
                if self.sets[i]==[]:
                     #ako je karta as odmah ide u prvi set složenih karata koji je prazan
                     if k[2:4]=="01":       
                        self.deck[1].remove(c)
                        self.sets[i].append(c)
                        c.configure(command=lambda l=k: self.setcards(l))
                        c.place_forget()
                        c.place(x=(10+i*80), y=10, height=100, width=70)
                        c.lift()
                        #vraćanje pozicije preokrenutih karata
                        for i in range (3, 0, -1):
                            if len(self.deck[1])-i>=0:
                                self.deck[1][-i].place_forget()
                                self.deck[1][-i].place(x=(510-20*i), y=10, height=100, width=70)
                                self.deck[1][-i].lift()
                                if i==1:
                                    self.deck[1][-i].configure(state=NORMAL, command=lambda l=self.deck[1][-i]: self.deckcard(l))
                        return

                else:
                #ako karta može biti spremljena u set
                    s=self.sets[i][0].cget("text")
                    #karte su iste vrste
                    if s[1]==k[1]:
                        s=self.sets[i][-1].cget("text")
                        #broj posljednje karte mora biti za 1 manji od trenutne karte
                        if (int(s[2:4])+1)==int(k[2:4]):
                            self.deck[1].remove(c)
                            self.sets[i].append(c)
                            c.configure(command=lambda l=k: self.setcards(l))
                            c.place_forget()
                            c.place(x=(10+i*80), y=10, height=100, width=70)
                            c.lift()
                            #vraćanje pozicije preokrenutih karata
                            for i in range (3, 0, -1):
                                if len(self.deck[1])-i>=0:
                                    self.deck[1][-i].place_forget()
                                    self.deck[1][-i].place(x=(510-20*i), y=10, height=100, width=70)
                                    self.deck[1][-i].lift()
                                    if i==1:
                                        self.deck[1][-i].configure(state=NORMAL, command=lambda l=self.deck[1][-i]: self.deckcard(l))
                            # ako je karta kralj provjera je li igra gotova
                            if k[2:4]=="13":
                                    for j in range (4):
                                        if self.sets[j]!=[]:
                                            if self.sets[j][-1].cget("text")[2:4]!="13":
                                                return
                                        else:
                                            return
                                    win=Win()
                                    exit()
                                
                            return
                        else:
                            #u slučaju da posljenja karta u setu nije za jedan manja od trenutne
                            break
                           
            #ako karta može biti stavljena u neki od redova
            for i in range (7):
                # u slučaju da je karta kralj ona ide na slobodni red
                if self.rows[i]==[]:
                    if k[2:4]=="13":
                            self.deck[1].remove(c)
                            self.rows[i].append(c)
                            c.configure(command=lambda l=k: self.rowcards(l))
                            c.place_forget()
                            c.place(x=(490-i*80), y=135, height=100, width=70)
                            c.lift()
                            #vraćanje pozicije preokrenutih karata
                            for i in range (3, 0, -1):
                                if len(self.deck[1])-i>=0:
                                    self.deck[1][-i].place_forget()
                                    self.deck[1][-i].place(x=(510-20*i), y=10, height=100, width=70)
                                    self.deck[1][-i].lift()
                                    if i==1:
                                        self.deck[1][-i].configure(state=NORMAL, command=lambda l=self.deck[1][-i]: self.deckcard(l))
                            return
                else:
                    s=self.rows[i][-1].cget("text")
                    #karta nije jednake boje kao posljednja u redu i njezin broj je za jedan veći
                    if k[0]!=s[0] and int(s[2:4])==(int(k[2:4])+1):
                        self.deck[1].remove(c)
                        self.rows[i].append(c)
                        c.configure(command=lambda l=k: self.rowcards(l))
                        c.place_forget()
                        c.place(x=(490-i*80), y=(115+len(self.rows[i])*20), height=100, width=70)
                        c.lift()
                        #vraćanje pozicije preokrenutih karata
                        for i in range (3, 0, -1):
                            if len(self.deck[1])-i>=0:
                                self.deck[1][-i].place_forget()
                                self.deck[1][-i].place(x=(510-20*i), y=10, height=100, width=70)
                                self.deck[1][-i].lift()
                                if i==1:
                                    self.deck[1][-i].configure(state=NORMAL, command=lambda l=self.deck[1][-i]: self.deckcard(l))
                        return

    #naredba za karte u redovima                
    def rowcards (self, k):
             #lociranje karte pomoću teksta
             for i in range (7):
                for j in range (len(self.rows[i])):
                    if k==self.rows[i][j].cget("text"):
                        #karta je c, a r i m koordinate
                        c=self.rows[i][j]
                        r=i
                        m=j
      
             #provjer ako karta može ići u set
             for i in range (4):
                  if self.sets[i]==[]:
                      #ako je karta as, isti princip kao i prije
                       if k[2:4]=="01":
                          self.rows[r].remove(c)
                          self.sets[i].append(c)
                          c.configure(command=lambda l=k: self.setcards(l))
                          c.place_forget()
                          c.place(x=(10+i*80), y=10, height=100, width=70)
                          c.lift()
                          #ako je karta prije isključena uključuje se i dobiva sliku
                          if self.rows[r]!=[]:
                             if self.rows[r][m-1]["state"]=="disabled":
                                 img=Image.open(self.rows[r][m-1].cget("text")[1:]+".png")
                                 image=ImageTk.PhotoImage(img, master=self.frame)
                                 self.rows[r][m-1].configure(state=NORMAL, image=image)
                                 self.rows[r][m-1].image=image
                         
                          return
                  #karta ide na set mora biti zadnja u redu, to ne treba u slučaju asa jer on mora biti na kraju reda
                  elif c==self.rows[r][-1] :
                       s=self.sets[i][0].cget("text")
                       #karte su iste vrste
                       if s[1]==k[1]:
                            s=self.sets[i][-1].cget("text")
                            #broj posljednje karte mora biti za 1 manji od trenutne karte
                            if (int(s[2:4])+1)==int(k[2:4]):
                                self.rows[r].remove(c)
                                self.sets[i].append(c)
                                c.configure(command=lambda l=k: self.setcards(l))
                                c.place_forget()
                                c.place(x=(10+i*80), y=10, height=100, width=70)
                                c.lift()
                                #ako je karta prije isključena uključuje se i dobiva sliku
                                if self.rows[r]!=[]:
                                    if self.rows[r][m-1]["state"]=="disabled":
                                         img=Image.open(self.rows[r][m-1].cget("text")[1:]+".png")
                                         image=ImageTk.PhotoImage(img, master=self.frame)
                                         self.rows[r][m-1].configure(state=NORMAL, image=image)
                                         self.rows[r][m-1].image=image
                                # ako je karta kralj provjera je li igra gotova
                                if k[2:4]=="13":
                                    for j in range (4):
                                        if self.sets[j]!=[]:
                                            if self.sets[j][-1].cget("text")[2:4]!="13":
                                                return
                                        else:
                                            return
                                    win=Win()
                                    exit()
                                return    

             #ako karta može ići u jedan od redova    
             for i in range (7):
                    if self.rows[i]==[]:
                        #ako je karta kralj
                        if k[2:4]=="13":
                            for j in self.rows[r][self.rows[r].index(c):]:
                                #ovaj dio je za slučaj da su ispod katre druge karte pa i njih treba prebaciti
                                k=j.cget("text")
                                self.rows[r].remove(j)
                                self.rows[i].append(j)
                                j.configure(command=lambda l=k: self.rowcards(l))
                                j.place_forget()
                                j.place(x=(490-i*80), y=(115+len(self.rows[i])*20), height=100, width=70)
                                j.lift()
                            #ako je karta prije isključena uključuje se i dobiva sliku
                            if self.rows[r]!=[]:
                                    if self.rows[r][m-1]["state"]=="disabled":
                                         img=Image.open(self.rows[r][m-1].cget("text")[1:]+".png")
                                         image=ImageTk.PhotoImage(img, master=self.frame)
                                         self.rows[r][m-1].configure(state=NORMAL, image=image)
                                         self.rows[r][m-1].image=image
                            return
                    
                    else :
                        s=self.rows[i][-1].cget("text")
                        #karta nije jednake boje kao posljednja u redu i njezin broj je za jedan veći
                        if k[0]!=s[0] and int(s[2:4])==(int(k[2:4])+1):
                            for j in self.rows[r][self.rows[r].index(c):]:
                                #isto kao i u slučaju kralja
                                k=j.cget("text")
                                self.rows[r].remove(j)
                                self.rows[i].append(j)
                                j.configure(command=lambda l=k: self.rowcards(l))
                                j.place_forget()
                                j.place(x=(490-i*80), y=(115+len(self.rows[i])*20), height=100, width=70)
                                j.lift()
                            #ako je karta prije isključena uključuje se i dobiva sliku
                            if self.rows[r]!=[]:
                                if self.rows[r][m-1]["state"]=="disabled":
                                    img=Image.open(self.rows[r][m-1].cget("text")[1:]+".png")
                                    image=ImageTk.PhotoImage(img, master=self.frame)
                                    self.rows[r][m-1].configure(state=NORMAL, image=image)
                                    self.rows[r][m-1].image=image
                            return
             
                                        
    def setcards(self, k):
            #lociranje karte pomoću teksta
            for i in range(4):
                if self.sets[i]!=[]:
                    if self.sets[i][0].cget("text")[1]==k[1]:
                        #isto kao i za redove, samo ovdje mi treba jedino ta karta i set u kojem je ona
                        c=self.sets[i][-1]
                        r=self.sets.index(self.sets[i])
                        break
            #karta iz seta jedino može ići u jedan od redova
            for i in range (7):
                #ako je karta kralj
                if self.rows[i]==[]:
                    if k[2:4]=="13":
                        self.sets[r].remove(c)
                        self.rows[i].append(c)
                        c.configure(command=lambda l=k: self.rowcards(l))
                        c.place_forget()
                        c.place(x=(490-i*80), y=135, height=100, width=70)
                        c.lift()
                        return
                else :
                    s=self.rows[i][-1].cget("text")
                    #karta nije jednake boje kao posljednja u redu i njezin broj je za jedan veći
                    if k[0]!=s[0] and int(s[2:4])==(int(k[2:4])+1):
                        self.sets[r].remove(c)
                        self.rows[i].append(c)
                        c.configure(command=lambda l=k: self.rowcards(l))
                        c.place_forget()
                        c.place(x=(490-i*80), y=(115+len(self.rows[i])*20), height=100, width=70)
                        c.lift()
                        return


    def shuffle (self):
        #komanda gumba za okrenut špil, vraća sve karte u nistu neokrenutih karata ponovno postaju aktive
        for i in range (1, len(self.deck[1])+1):
            c=self.deck[1][-1]
            self.deck[1].remove(c)
            self.deck[0].append(c)
            image=ImageTk.PhotoImage(self.cardb, master=self.frame)
            self.deck[0][-1].configure(command=lambda : self.deckc(), image=image, state=NORMAL)
            c.image=image
            c.place_forget()
            c.place(x=570, y=10, height=100, width=70)
            c.lift()

class Win (Tk):
    def __init__(self):
        #poruka da ste pobijdili, program se prekida
        win=showinfo("Vicroy!", "You won, congratulations")
        exit()
            
    
        
pasijans=Menu()
