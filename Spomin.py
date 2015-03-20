from tkinter import *
from random import *
import random
from functools import partial
import time

images=["piratebay.png", "torbrowser.png", "duck.gif", "batman.png",
        "allstar.png", "peace.png", "dn.png", "owl.png",
        "bender.png", "btc.png", "kava.gif", "moon.png",
        "kyle.png", "charizard.png", "stark.gif", "nutella.gif",
        "pizza.gif", "burek.gif"]
imgPath = "C:\\Users\\Lucija\\Desktop\\Spomin\\images\\"
cards = []
pics = {}



class Memory(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")   
        self.parent = parent
        self.initUI()
        
                
        menu = Menu(self.parent)
        self.parent.config(menu=menu)
        podmenu = Menu(menu)
        podmenu.add_command(label='Nova igra', command=self.nova_igra)
        podmenu.add_command(label='Izhod', command=self.parent.destroy)
        menu.add_cascade(label='Igra', menu=podmenu)


    def init_karte(self):
        turned = [[False for x in range(6)] for x in range(6)]
        table = [[0 for x in range(6)] for x in range(6)]
        buttons = [[0 for x in range(6)] for x in range(6)]
        back = PhotoImage(file="C:\\Users\\Lucija\\Desktop\\Spomin\\images\\back.png")
        tocke = [0, 0]
        self.igralec = 0
        self.prejsnja = []

        Label(self, text='Igralec 1:').grid(row=6, column=0)
        
        self.tocke1 = StringVar()
        Label(self, textvariable=self.tocke1).grid(row=6, column=1)
        self.tocke1.set('0')
        
        Label(self, text='Igralec 2:').grid(row=6, column=2)

        self.tocke2 = StringVar()
        Label(self, textvariable=self.tocke2).grid(row=6, column=3)
        self.tocke2.set('0')
        
        self.status = StringVar()
        Label(self, textvariable=self.status).grid(row=6, column=4)
        self.status.set('Na vrsti:')
        
        self.naVrsti = StringVar()
        Label(self, textvariable=self.naVrsti).grid(row=6, column=5)
        self.naVrsti.set('Igralec 1:')

        def callback(i, j):
            turned[i][j] = not turned[i][j];
            if turned[i][j]:
                buttons[i][j].config(image=pics[table[i][j]], state=DISABLED)
                if len(self.prejsnja) > 0:
                    if table[i][j] == table[self.prejsnja[0]][self.prejsnja[1]]:
                        tocke[self.igralec] = tocke[self.igralec] + 1
                    else:
                        self.update()
                        time.sleep(3)
                        self.igralec = (self.igralec + 1) % 2
                        buttons[i][j].config(image=back, state=NORMAL)
                        buttons[self.prejsnja[0]][self.prejsnja[1]].config(image=back, state=NORMAL)
                        turned[i][j] = False
                        turned[self.prejsnja[0]][self.prejsnja[1]] = False
                    self.prejsnja = []
                else:
                    self.prejsnja = [i, j]
                self.tocke1.set(tocke[0])
                self.tocke2.set(tocke[1])
                if tocke[0] + tocke[1] == 18:
                    if tocke[0] == tocke[1]:
                        self.status.set('Izenačeno')
                        self.naVrsti.set('')
                    else:
                        self.status.set('Zmagal:')
                        if tocke[0] > tocke[1]:
                            self.naVrsti.set('Igralec 1')
                        else:
                            self.naVrsti.set('Igralec 2')
                else:
                    if self.igralec == 0:
                        self.naVrsti.set('Igralec 1')
                    else:
                        self.naVrsti.set('Igralec 2')
                
            else:
                buttons[i][j].config(image=back)
            print(str(i)+" "+str(j) + " " + table[i][j] + " igralec: " + str(self.igralec))
        
        for i in range(18):
            cards.append(images[i])
            cards.append(images[i])
            if not images[i] in pics:
                pics[images[i]] = PhotoImage(file=imgPath + images[i])

        for i in range(6):
            for j in range(6):
                rand = random.randint(0, len(cards)-1)
                table[i][j] = cards[rand]
                cards.remove(cards[rand])
                buttons[i][j] = Button(self, command=partial(callback, i, j))
                buttons[i][j].config(image=back,width="85",height="85")
                buttons[i][j].grid(row=i, column=j)

        
    def initUI(self):
      
        self.parent.title("Spomin")
        self.pack(fill=BOTH, expand=1)

        self.init_karte()

           
        

    def nova_igra(self):
        self.init_karte()
        

        
        # izberemo če za dva igralca ali proti računalniku...
        
        # seznam že obrnjenih
        # pozabljanje
        

def main():
  
    root = Tk()
    root.geometry("546x576")
    app = Memory(root)
    root.mainloop()


if __name__ == '__main__':
    main()  

