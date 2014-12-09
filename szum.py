#import numpy
import scipy.misc
#import sys
#import qrcode
#from PIL import Image
#from scipy import stats
import random


def pasy(i, j, imagea):
    try:
        if (j+i)%10==0:
            imagea[i][j]=[255,255,255]
            imagea[i][j+1]=[255,255,255]
            imagea[i][j+2]=[255,255,255]
    except:
        pass

def kwadratWRogu(i, j, imagea):
    if i>40 and j>40:
        imagea[i][j]=[255,255,255]

def kwadratWSrodku(i, j, imagea):
    if i>20 and i<60 and j>20 and j<60:
        imagea[i][j]=[255,255,255]
                        

def szum(i, j, imagea, wsp=10):
    if random.randint(0, wsp) == 0:
        imagea[i][j]=[255,255,255]

def zepsuj(lista_znakow):
    print 'W jaki sposob chcesz zepsuc znaki?'
    print '1. Paski'
    print '2. Szum'
    print '3. Kwadrat w srodku'
    print '4. Kwdrat z rogu'
    opcja = raw_input('Podaj opcje: ')
    przed = raw_input('Podaj przedrostek do zapisu: ')
    wsp = opcja == '2' and raw_input('Podaj wspolczynnik (wiekszy = mniejszy szum): ')

    for z in lista_znakow:
        imagea = (scipy.misc.imread(z))
        for i, x in enumerate(imagea):
            for j, y in enumerate(x):
                if opcja == '1':
                    pasy(i, j, imagea)
                elif opcja == '2':
                    szum(i, j, imagea, int(wsp))
                elif opcja == '3':
                    kwadratWSrodku(i, j, imagea)
                elif opcja == '4':
                    kwadratWRogu(i, j, imagea)

        scipy.misc.imsave(str(przed)+z, imagea)


if __name__ == "__main__":

    znaki = ['a_02.png', 'a_07.png', 'a_09.png', 'a_25.png', 'a_29.png',
             'b_01.png', 'b_05.png', 'b_23.png', 'b_25.png', 'b_41.png',
             'c_05.png', 'c_08.png', 'c_12.png', 'c_14.png', 'c_16a.png',
             'd_04a.png', 'd_06.png', 'd_18.png'
             ]

    zepsuj(znaki)


