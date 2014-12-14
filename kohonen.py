"""

"""
from PIL import Image

import math
import random
import os

OUTPUT_NEURONS = 18
INPUT_SIZE = 80*80

def normalizuj(vlist):
    '''Zwraca wartosc normalizacyjna'''
    norm = 1/math.sqrt(sum([float(x)*float(x) for x in vlist]))
    return [float(x)*float(norm) for x in vlist]
    #return norm

def suma_euklidesowa(a,b):
    suma = 0
    for i,x in enumerate(a):
        suma = suma + (float(x)-float(b[i]))*(float(x)-float(b[i]))

    return math.sqrt(suma)

def losujWagi(filename):
        '''Losuje wagi i zapisuje do pliku'''
        wagi = normalizuj([random.randint(0,255) for x in range(INPUT_SIZE)])
        
        with open(filename, 'w') as fileh:
            for i in range(OUTPUT_NEURONS):
                fileh.write('NONE;{}\n'.format(
                    ';'.join([str(x) for x in wagi])
                ))

class Kohonen(object):
    '''Szukanie wektora, ktory wygral'''

    def __init__(self, vector, filename):
        self.filename = filename
        self.lista_wag  = []
        self.vector = vector #lista pixeli
        self.forced = False

    def pobierzWagi(self):
        '''Pobiera wagi z pliku wraz z przypisanym neuronem'''
        with open(self.filename, 'r') as wagi:
            self.lista_wag = [line.rstrip().split(';') for line in wagi]
            #print self.lista_wag

    def rozstrzygnij(self, name = 'NONE'):
        '''Rozstrzyga, ktory neuron wygral i oznacza w tablicy wag'''
        winner = [-1, 'brak'] #wynik, id
        
        sasiedztwo = []

        for i, n in enumerate(self.lista_wag):
            roznica = suma_euklidesowa(n[1:], self.vector)

            if (roznica < winner[0] or winner[0] < 0) and (not self.forced or self.lista_wag[i][0] in ['NONE', name] ):
                winner = [roznica, i]
            elif (len(sasiedztwo) < 2 or roznica < sasiedztwo[1]):
                try:
                    del sasiedztwo[1]
                except:
                    pass
                finally:
                    sasiedztwo.append([roznica, i])
                    sasiedztwo.sort()


        return self.lista_wag[winner[1]], winner[1], sasiedztwo


class Trening(Kohonen):
    '''Uczenie sieci. Podajemy wektor uczacy oraz nazwe'''
    
    def __init__(self, vector, name, wspolczynnik = 0.5, filename='wagi', forcedWin = True):
        super(Trening, self).__init__(vector, filename)
        self.tlist = [] #lista wag do trenowania
        self.name = name
        self.alfa = wspolczynnik
        self.forced = forcedWin

    def trenuj(self):

        self.tlist, neuron_id, sasiedztwo = self.rozstrzygnij(self.name)
        petla = 30

        for licz in range(petla):   #####dobrac alpha i warunek konca uczenia
            for i, x in enumerate(self.tlist[1:]):
                self.tlist[i+1] = str(float(x) + (self.alfa/(licz+1))*(float(self.vector[i])-float(x)))
                
                #wykona sie jesli sasiedztwo nie jest pusta lista
                for s in sasiedztwo:
                    self.lista_wag[s[1]][i+1] = str(float(x) + (self.alfa/(licz+1))*(1/(licz+1))*(float(self.vector[i])-float(x)))

        self.tlist[0]=self.name
        self.lista_wag[neuron_id] = self.tlist
        self.zapisz()

    def zapisz(self):
        #print self.lista_wag
        with open(self.filename, 'w') as fileh:
            for i in range(OUTPUT_NEURONS):
                wagi = normalizuj(self.lista_wag[i][1:])
                fileh.write('{};{}\n'.format(self.lista_wag[i][0],
                    ';'.join([str(x) for x in wagi])
                ))



class Obraz(object):

    def __init__(self, filename, path):
        self.filename = filename
        self.path = path
        self.im = Image.open(path)

    def resize(self, x=80, y=80):
        if self.im.mode != 'RGB':
            self.im = self.im.convert('RGB')
        self.im = self.im.resize((x,y), Image.ANTIALIAS)
        self.im.save(path, "PNG")

    def topixel(self): 
        pixels = list(self.im.getdata())
        lista = []
        #print type(pixels)
        for x in pixels:
            lista.extend(x)
            
        #print len(lista)
        return lista

        
if __name__ == '__main__':

    znaki = ['a_02.png', 'a_07.png', 'a_09.png', 'a_25.png', 'a_29.png',
             'b_01.png', 'b_05.png', 'b_23.png', 'b_25.png', 'b_41.png',
             'c_05.png', 'c_08.png', 'c_12.png', 'c_14.png', 'c_16a.png',
             'd_04a.png', 'd_06.png', 'd_18.png'
             ]

    poprawne = 0

    print 'Co chcesz zrobic? (Wybierz numer)'
    print '1. Losuj wagi'
    print '2. Trenuj z wymuszeniem zwyciezcy'
    print '3. Trenuj bez wymuszenia zwyciezcy'
    print '4. Rozpoznaj znaki'
    opcja = raw_input()

    if opcja == '1':

        losujWagi('wagi')

    elif opcja == '2':

        for i in znaki:
            path = os.getcwd() + '//' + i
            znak = Obraz(i, path)
            pix = znak.topixel()

            b = Trening(pix, i, forcedWin=True, filename='wagi')
            b.pobierzWagi()
            b.trenuj()

    elif opcja == '3':

        for i in znaki:
            path = os.getcwd() + '//' + i
            znak = Obraz(i, path)
            pix = znak.topixel()

            b = Trening(pix, i, forcedWin=False, filename='wagi')
            b.pobierzWagi()
            b.trenuj()

    elif opcja == '4':

        przed = raw_input('Podaj przedrostek: ')
        for i in znaki:
            i = przed + i
            path = os.getcwd() + '//' + i
            znak = Obraz(i, path)
            pix = znak.topixel()

            a=Kohonen(normalizuj(pix), 'wagi')
            a.pobierzWagi()
            r, _, _ = a.rozstrzygnij()

            print 'Podano: {}, Rozpoznano: {}'.format(i, r[0])
            if i[len(przed):] == r[0]:
                poprawne += 1

        print poprawne, len(znaki)
        print "Rozpoznano %.2f%% znakow" %(float(poprawne)/float(len(znaki))*100)
        poprawne = 0

    else:
        print 'nie wybrales poprawnej opcji'    
        #print len(pix)
        #print pix[15000]
