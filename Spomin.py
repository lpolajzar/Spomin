from tkinter import *
import random
from functools import partial
import time

images=["piratebay", "torbrowser", "duck", "batman", "allstar", "peace",
        "dn", "owl", "bender", "btc", "kava", "moon",
        "kyle", "charizard", "stark", "nutella", "pizza", "burek"]
imgPath = "./images/"
imgFormat = ".gif"
cards = []
pics = {}
racunalnik = False



class Memory(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")   
        self.parent = parent
        self.initUI()

        menu = Menu(self.parent)
        self.parent.config(menu=menu)
        podmenu = Menu(menu)
        podmenu.add_command(label='2 igralca', command=self.nova_igra)
        podmenu.add_command(label='Proti računalniku', command = self.nova_igra_racunalnik)
        menu.add_cascade(label='Nova igra', menu=podmenu)
        menu.add_cascade(label='Izhod', command=self.parent.destroy)

    def dodajOdkrite(self, x, y, karta):
        self.odkrite[0].append(karta)
        self.odkrite[1].append(x)
        self.odkrite[2].append(y)

    def jeOdkrita(self, x, y):
        prvi = len(self.odkrite[0]) - self.globinaClovek
        if prvi < 0:
            prvi = 0
        for i in range(prvi, len(self.odkrite[0])):
            if self.odkrite[1][i] == x and self.odkrite[2][i] == y:
                return True
        return False

    def pozitivnaGlobina(self, karta):
        for i in range(len(self.odkrite[0])):
            if self.odkrite[0][i] == karta and len(self.odkrite[0]) - i > self.globinaClovek:
                self.globinaClovek += len(self.odkrite[0]) - i
                self.globinaClovek = int(self.globinaClovek/2)
                return

    def negativnaGlobina(self, karta):
        print(karta)
        pari = []
        for i in range(len(self.odkrite[0])-1, len(self.odkrite[0]) - self.globinaClovek - 1, -1):
            if self.odkrite[0][i] == karta and [self.odkrite[1][i], self.odkrite[2][i]] not in pari:
                pari.append([self.odkrite[1][i], self.odkrite[2][i]])
            if len(pari) == 2:
                self.globinaClovek += len(self.odkrite[0]) - i - 1
                self.globinaClovek = int(self.globinaClovek/2)
                print(self.globinaClovek)
                print(len(self.odkrite[0]))
                print(i)
                return

    def odkritiPari(self):
        karte = []
        pari = []
        start = len(self.odkrite[0]) - self.globinaClovek
        if start < 0:
            start = 0
        for i in range(start, len(self.odkrite[0])):
            if self.odkrite[0][i] not in karte and len(self.odkrite[0]) - i <= self.globinaClovek:
                par = [[self.odkrite[1][i], self.odkrite[2][i]]]
                for j in range(i, len(self.odkrite[0])):
                    if self.odkrite[0][i] == self.odkrite[0][j] and not( self.odkrite[1][j] == self.odkrite[1][i] and self.odkrite[2][j] == self.odkrite[2][i]):
                        par.append([self.odkrite[1][j], self.odkrite[2][j]])
                karte.append(self.odkrite[0][i])
                if len(par) == 2:
                    pari.append(par)
        return pari

    def pariVsebujejo(self, pari, par):
        for i in range(len(pari)):
            if par in pari[i]:
                return True
        return False

    def callback(self, i, j):
        self.turned[i][j] = not self.turned[i][j]
        if self.turned[i][j]:
            self.buttons[i][j].config(image=pics[self.table[i][j]], state=DISABLED)
            if len(self.prejsnja) > 0:
                if self.table[i][j] == self.table[self.prejsnja[0]][self.prejsnja[1]]:
                    self.tocke[self.igralec] = self.tocke[self.igralec] + 1
                    if self.igralec == 0:
                        self.pozitivnaGlobina(self.table[i][j])
                    self.prejsnja = []
                else:
                    self.update()
                    time.sleep(2)
                    self.igralec = (self.igralec + 1) % 2
                    self.buttons[i][j].config(image=self.back, state=NORMAL)
                    self.buttons[self.prejsnja[0]][self.prejsnja[1]].config(image=self.back, state=NORMAL)
                    self.turned[i][j] = False
                    self.turned[self.prejsnja[0]][self.prejsnja[1]] = False
                    if len(self.odkritiPari()) > 0 and self.igralec == 0:
                        self.negativnaGlobina(self.table[i][j])
                    self.prejsnja = []
                    self.dodajOdkrite(i, j, self.table[i][j])
            else:
                self.prejsnja = [i, j]
                pari = self.odkritiPari()
                if len(pari) > 0 and self.pariVsebujejo(pari, [i, j]) and self.igralec == 0:
                    self.negativnaGlobina(self.table[i][j])
                self.dodajOdkrite(i, j, self.table[i][j])
            self.tocke1.set(self.tocke[0])
            self.tocke2.set(self.tocke[1])
            if self.tocke[0] + self.tocke[1] == 18:
                if self.tocke[0] == self.tocke[1]:
                    self.status.set('Izenačeno')
                    self.naVrsti.set('')
                else:
                    self.status.set('Zmagal:')
                    if self.tocke[0] > self.tocke[1]:
                        self.naVrsti.set('Igralec 1')
                    elif self.racunalnik:
                        self.naVrsti.set('Računalnik')
                    else:
                        self.naVrsti.set('Igralec 2')
            else:
                if self.igralec == 0:
                    self.naVrsti.set('Igralec 1')
                elif self.racunalnik:
                    self.naVrsti.set('Računalnik')
                else:
                    self.naVrsti.set('Igralec 2')

        else:
            self.buttons[i][j].config(image=self.back)

        print('')
        print(str(i)+" "+str(j) + " " + self.table[i][j] + " igralec: " + str(self.igralec) + " globina " + str(self.globinaClovek))
        print(self.odkrite)
        if len(self.prejsnja) == 0 and self.racunalnik and self.igralec == 1 and self.tocke[0] + self.tocke[1] < 18:
            self.igraRacunalnik()
        


    def init_karte(self):
        self.turned = [[False for x in range(6)] for x in range(6)]
        self.table = [[0 for x in range(6)] for x in range(6)]
        self.buttons = [[0 for x in range(6)] for x in range(6)]
        self.back = PhotoImage(file="./images/back.gif")
        self.tocke = [0, 0]
        self.igralec = 0
        self.prejsnja = []

        Label(self, text='Igralec 1:').grid(row=6, column=0)
        
        self.tocke1 = StringVar()
        Label(self, textvariable=self.tocke1).grid(row=6, column=1)
        self.tocke1.set('0')

        try:
            foo = self.igralec2
        except AttributeError:
            self.igralec2 = StringVar()
            Label(self, textvariable=self.igralec2).grid(row=6, column=2)
        if self.racunalnik:
            self.igralec2.set('Računalnik:')
        else:
            self.igralec2.set('Igralec 2:')

        self.tocke2 = StringVar()
        Label(self, textvariable=self.tocke2).grid(row=6, column=3)
        self.tocke2.set('0')
        
        self.status = StringVar()
        Label(self, textvariable=self.status).grid(row=6, column=4)
        self.status.set('Na vrsti:')
        
        self.naVrsti = StringVar()
        Label(self, textvariable=self.naVrsti).grid(row=6, column=5)
        self.naVrsti.set('Igralec 1')
        
        for i in range(18):
            cards.append(images[i])
            cards.append(images[i])
            if not images[i] in pics:
                pics[images[i]] = PhotoImage(file=imgPath + images[i] + imgFormat)

        for i in range(6):
            for j in range(6):
                rand = random.randint(0, len(cards)-1)
                self.table[i][j] = cards[rand]
                cards.remove(cards[rand])
                self.buttons[i][j] = Button(self, command=partial(self.callback, i, j))
                self.buttons[i][j].config(image=self.back,width="85",height="85")
                self.buttons[i][j].grid(row=i, column=j)

        
    def initUI(self):
      
        self.parent.title("Spomin")
        self.pack(fill=BOTH, expand=1)
        self.globinaClovek = 4

        self.nova_igra_racunalnik()

           
        

    def nova_igra(self):
        self.racunalnik = False
        self.init_karte()

    def nova_igra_racunalnik(self):
        self.racunalnik = True
        self.odkrite = [[], [], []]
        self.init_karte()
        

    def igraRacunalnik(self):
        self.update()
        time.sleep(1)

        pari = self.odkritiPari()
        isRandom = True

        if len(pari) > 0:
            i=pari[0][0][0]
            j=pari[0][0][1]
            isRandom = False
        else:
            i=random.randint(0, len(self.turned)-1)
            j=random.randint(0, len(self.turned[i])-1)

        while self.turned[i][j] or isRandom and self.jeOdkrita(i, j):
            i=random.randint(0, len(self.turned)-1)
            j=random.randint(0, len(self.turned[i])-1)

        self.callback(i, j)

        self.update()
        time.sleep(1)
        
        if len(pari) > 0:
            i=pari[0][1][0]
            j=pari[0][1][1]
            isRandom = False
        else:
            i=random.randint(0, len(self.turned)-1)
            j=random.randint(0, len(self.turned[i])-1)

        if len(pari) == 0:
            pari = self.odkritiPari()
            if len(pari) > 0:
                i=pari[0][0][0]
                j=pari[0][0][1]
                isRandom = False

        while self.turned[i][j] or isRandom and self.jeOdkrita(i, j):
            i=random.randint(0, len(self.turned)-1)
            j=random.randint(0, len(self.turned[i])-1)

        self.callback(i, j)
        

def main():
  
    root = Tk()
    root.geometry("546x576")
    app = Memory(root)
    root.mainloop()


if __name__ == '__main__':
    main()  

