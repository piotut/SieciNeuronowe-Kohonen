import szum
import kohonen
import os

if __name__ == '__main__':

    znaki = ['a_02.png', 'a_07.png', 'a_09.png', 'a_25.png', 'a_29.png',
             'b_01.png', 'b_05.png', 'b_23.png', 'b_25.png', 'b_41.png',
             'c_05.png', 'c_08.png', 'c_12.png', 'c_14.png', 'c_16a.png',
             'd_04a.png', 'd_06.png', 'd_18.png'
             ]
    opcja = ['1', '2', '3', '4']
    poprawne = 0
    procent = [10, 20, 30, 40, 50, 60, 70, 80, 90]#[10, 20, 30, 40, 50, 60, 70, 80]
    for o in opcja:
        for p in procent:
            szum.zepsuj(znaki, True, o, p, '{}_{}'.format(o,p))

            for i in znaki:
                i = '{}_{}'.format(o,p) + i
                path = os.getcwd() + '//zepsute/' + i
                znak = kohonen.Obraz(i, path)
                pix = znak.topixel()

                a=kohonen.Kohonen(kohonen.normalizuj(pix), 'wagi')
                a.pobierzWagi()
                r, _, _ = a.rozstrzygnij()

                #print 'Procent: {}, Podano: {}, Rozpoznano: {}'.format(p, i, r[0])
                if i[len('{}_{}'.format(o,p)):] == r[0]:
                    poprawne += 1

            #print poprawne, len(znaki)
            print "Opcja: %s, Procent: %d, Rozpoznano %.2f%% znakow" %(o, p, float(poprawne)/float(len(znaki))*100)
            with open('results_saisad.txt', 'a') as fh:
                fh.write('{};{};{}\n'.format(o, p, float(poprawne)/float(len(znaki))*100))
            poprawne = 0