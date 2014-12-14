import scipy.misc
import random
import math


def pasy(i, j, imagea, wsp=10):
    try:
        if (j+i)%10==0:
            for a in range(int(wsp/10)):
                imagea[i][j+a]=[255,255,255]
            #imagea[i][j+1]=[255,255,255]
            #imagea[i][j+2]=[255,255,255]
    except:
        pass

def kwadratWRogu(i, j, imagea, wsp=10):
    granica = math.sqrt(float(wsp)/100*80*80)
    if i>80-granica and j>80-granica:
        imagea[i][j]=[255,255,255]

def kwadratWSrodku(i, j, imagea, wsp=10):
    granica = math.sqrt(float(wsp)/100*80*80)*0.5
    if i>40-granica and i<40+granica and j>40-granica and j<40+granica:
        imagea[i][j]=[255,255,255]               

def szum(i, j, imagea, wsp=10):
    #print int((1.0/wsp)*100)
    if random.randint(0, 100) < wsp:
        imagea[i][j]=[255,255,255]

def zepsuj(lista_znakow, test=False, opcja=0, wsp=0, przed=''):

    if not test:
        print 'W jaki sposob chcesz zepsuc znaki?'
        print '1. Paski'
        print '2. Szum'
        print '3. Kwadrat w srodku'
        print '4. Kwdrat z rogu'
        opcja = raw_input('Podaj opcje: ')
        przed = raw_input('Podaj przedrostek do zapisu: ')
        wsp = raw_input('Podaj wspolczynnik %: ')

    for z in lista_znakow:
        imagea = (scipy.misc.imread(z))
        for i, x in enumerate(imagea):
            for j, y in enumerate(x):
                if opcja == '1':
                    pasy(i, j, imagea, float(wsp))
                elif opcja == '2':
                    szum(i, j, imagea, float(wsp))
                elif opcja == '3':
                    kwadratWSrodku(i, j, imagea, float(wsp))
                elif opcja == '4':
                    kwadratWRogu(i, j, imagea, float(wsp))

        scipy.misc.imsave('zepsute/'+str(przed)+z, imagea)


if __name__ == "__main__":

    znaki = ['a_02.png', 'a_07.png', 'a_09.png', 'a_25.png', 'a_29.png',
             'b_01.png', 'b_05.png', 'b_23.png', 'b_25.png', 'b_41.png',
             'c_05.png', 'c_08.png', 'c_12.png', 'c_14.png', 'c_16a.png',
             'd_04a.png', 'd_06.png', 'd_18.png'
             ]

    zepsuj(znaki)


