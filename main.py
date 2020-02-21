from trie import Trie
from myset import MySet
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


def addWordsToSets(reci):
    list1 = trie.__search__(reci[0])
    list2 = trie.__search__(reci[1])
    set1 = MySet()
    set2 = MySet()

    for key, val in list1.items():
        set1.__addToSet__(key, val)
    for key, val in list2.items():
        set2.__addToSet__(key, val)
    return set1, set2


def pretrazi(reci):
    reci = reci.strip()
    if " OR " in reci:
        reci = reci.split(" OR ")
        set1, set2 = addWordsToSets(reci)
        final_arr = set1.__union__(set2)

    elif " AND " in reci:
        reci = reci.split(" AND ")
        set1, set2 = addWordsToSets(reci)
        final_arr = set1.__intersection__(set2)

    elif " NOT " in reci:
        reci = reci.split(" NOT ")
        set1, set2 = addWordsToSets(reci)
        final_arr = set1.__complement__(set2)

    else:
        reci = reci.split(" ")
        print(reci)
        final_set = MySet()
        for rec in reci:
            lista = trie.__search__(rec)
            for key, val in lista.items():
                final_set.__addToSet__(key, val)
        final_arr = final_set.list

    if len(final_arr) > 0:
        for val in final_arr:
            print(val.abspath)
    else:
        print("Trazene reci ne postoje")


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
            pretrazi(reci)  # elif opcija == 3:

    except Exception as e:
        print(e)
        print("--------------------Unesite broj kao opciju.--------------------- \n")
