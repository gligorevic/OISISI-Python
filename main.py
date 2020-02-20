from trie import Trie
import os

from myparser import Parser

parser = Parser()


def unosDirektorijuma():
    while True:
        try:
            global direktorijum
            direktorijum = input(
                "Unesite absolutnu putanju do direktorijuma ili broj 1 za trenutni direktorijum: \n")
            if direktorijum == '1':
                direktorijum = os.getcwd()
                break
            elif not os.path.isdir(direktorijum):
                print("Pogresan unos. ", direktorijum, " ne postoji.\n")
            else:
                break
        except:
            print("Doslo je do greske pokusajte ponovo")


unosDirektorijuma()


def initialize():
    global trie
    trie = Trie()
    for dirpath, dirnames, filenames in os.walk(direktorijum):
        for fileName in filenames:
            extension = os.path.splitext(fileName)[1]
            if extension == ".html" or extension == ".htm":
                links, words = parser.parse(os.path.join(dirpath, fileName))
                for index, word in enumerate(words):
                    trie.__addToTrie__(
                        word, index, os.path.join(dirpath, fileName))


initialize()

while True:
    try:
        print("\n" + "Trenutni direktorijum je: " + direktorijum + "\n")
        opcija = int(input(
            "Unesite opciju: \n 0.Izlaz iz programa \n 1.Unos nove putanje do direktorijuma za pretragu \n 2.Pretraga \n  \n"))
        if opcija == 0:
            break
        elif opcija == 1:
            unosDirektorijuma()
            initialize()
        elif opcija == 2:
            reci = input("Unesite reci za pretragu:\t")
            retVal = trie.__search__(reci)
            if len(retVal) > 0:
                for val in retVal:
                    print(val)
            else:
                print("Trazene reci ne postoje")
        # elif opcija == 3:

    except:
        print("--------------------Unesite broj kao opciju.--------------------- \n")
