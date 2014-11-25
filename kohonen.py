"""

"""
from PIL import Image

import math
import random
import os

OUTPUT_NEURONS = 3
INPUT_SIZE = 80*80

def losujWagi(filename):
        '''Losuje wagi i zapisuje do pliku'''
        with open(filename, 'w') as wagi:
            for i in range(OUTPUT_NEURONS):
                wagi.write('NONE;{}\n'.format(
                    ';'.join([str(random.randint(0,255)) for x in range(INPUT_SIZE)])
                ))

class Kohonen(object):
    '''Szukanie wektora, ktory wygral'''

    def __init__(self, vector, filename):
        self.filename = filename
        self.lista_wag  = []
        self.vector = vector #lista pixeli
        self.norm = 1
        self.forced = False

    def normalizuj(self, vlist):
        '''Zwraca wartosc normalizacyjna'''
        self.norm = 1/math.sqrt(sum([int(x)*int(x) for x in vlist]))

    def pobierzWagi(self):
        '''Pobiera wagi z pliku wraz z przypisanym neuronem'''
        with open(self.filename, 'r') as wagi:
            self.lista_wag = [line.rstrip().split(';') for line in wagi]
            #print self.lista_wag

    def rozstrzygnij(self):
        '''Rozstrzyga, ktory neuron wygral i oznacza w tablicy wag'''
        winner = [-1, 'brak'] #wynik, id
        
        for i, n in enumerate(self.lista_wag):
            #print n[1:], self.vector
            roznica = sum([abs(float(a) - float(b)) for a, b in zip(n[1:], self.vector)])
            print roznica

            if (roznica < winner[0] or winner[0] < 0) and (not self.forced or self.lista_wag[i][0] == 'NONE'):
                winner = [roznica, i]

        print winner, self.lista_wag[winner[1]][0]
        return self.lista_wag[winner[1]], winner[1]


class Trening(Kohonen):
    '''Uczenie sieci. Podajemy wektor uczacy oraz nazwe'''
    
    def __init__(self, vector, name, wspolczynnik = 0.3, filename='wagi', forcedWin = True):
        super(Trening, self).__init__(vector, filename)
        self.tlist = [] #lista wag do trenowania
        self.name = name
        self.alfa = wspolczynnik
        self.forced = forcedWin
        
    def trenuj(self):
        self.tlist, neuron_id = self.rozstrzygnij()
        for i, x in enumerate(self.tlist[1:]):
            self.tlist[i+1] = str(float(x) + self.alfa*(float(self.vector[i])-float(x)))
        self.tlist[0]=self.name
        self.lista_wag[neuron_id] = self.tlist
        self.zapisz()
        #w(i+1) = wi + alfa*(vector-wi)

    def zapisz(self):
        #print self.lista_wag
        with open(self.filename, 'w') as wagi:
            for i in range(OUTPUT_NEURONS):
                wagi.write('{}\n'.format(
                    ';'.join(self.lista_wag[i])
                ))



class Obraz(object):

    def __init__(self, filename):
        self.filename = filename
        self.im = Image.open(os.getcwd()+'//'+filename)

    def resize(self, x=80, y=80):
        if self.im.mode != 'RGB':
            self.im = self.im.convert('RGB')
        self.im = self.im.resize((x,y), Image.ANTIALIAS)
        self.im.save(os.getcwd()+"//"+self.filename, "PNG")

    def topixel(self): 
        pixels = list(self.im.getdata())
        lista = []
        #print type(pixels)
        for x in pixels:
            lista.extend(x)
            
        print len(lista)
        return lista
        
if __name__ == '__main__':
    #losujWagi('wagi')
    znaki = ['b_41.png','c_14.png','a_29.png',]
    #for i in range(10):
    for i in znaki:
    
        znak = Obraz(i)
        znak.resize()
        pix = znak.topixel()

        a=Kohonen(pix, 'wagi')
    
        a.pobierzWagi()
        a.rozstrzygnij()
    
        #b = Trening(pix, i, forcedWin=False, filename='wagi')
        #b.pobierzWagi()
        #b.trenuj()

    
        #print len(pix)
        #print pix[15000]
