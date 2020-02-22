from trie import Trie
from myset import MySet
from graph import Graph
# from AdjMatGraph import Graph
# from AdjMatGraph import Vertex
import os

from myparser import Parser

parser = Parser()
g = Graph(True)

V = set()
# vertices = {}

vidjeno_strana = 0
step = 5
broj_strana = step

poslednja_pretraga = ''
direktorijum = ''
trie = Trie()

final_arr = []


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
    E = []
    for dirpath, dirnames, filenames in os.walk(direktorijum):
        for fileName in filenames:
            extension = os.path.splitext(fileName)[1]
            if extension == ".html" or extension == ".htm":
                links, words = parser.parse(os.path.join(dirpath, fileName))
                for link in links:
                    g.insert_edge(g.insert_vertex(os.path.join(dirpath, fileName)), g.insert_vertex(link))
                for index, word in enumerate(words):
                    trie.__addToTrie__(
                        word, index, os.path.join(dirpath, fileName))
    # for e in E:
    #     V.add(e[0])
    #     V.add(e[1])
    # for v in V:
    #     vertices[v] = g.insert_vertex(v)
    # for e in E:
    #     src = e[0]
    #     dest=e[1]
    #     g.insert_edge(vertices[src] , vertices[dest])


initialize()


def addWordsToSets(reci):
    list1 = trie.__search__(reci[0])
    list2 = trie.__search__(reci[1])
    set1 = MySet()
    set2 = MySet()

    for key, val in list1.items():
        set1.__addToSet__(key, val)
       # print(key, val)
    for key, val in list2.items():
        set2.__addToSet__(key, val)
    return set1, set2


def pretrazi(reci):
    global final_arr
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
    print_pages()

def print_pages():
    if len(final_arr) > 0:
        for val in final_arr[vidjeno_strana:broj_strana]:
            print(val.abspath)
    else:
        print("Trazene reci ne postoje")


while True:
    try:
        print("\n" + "Trenutni direktorijum je: " + direktorijum + "\n")
        opcija = int(input(
            "Unesite opciju: \n 0.Izlaz iz programa \n 1.Unos nove putanje do direktorijuma za pretragu  \n "
            "2.Pretraga \n 3.Promijeni broj linkova za prikazivanje \n "
            "4.Sledeca stranica\n 5.Prethodna stranica \n"))
        if opcija == 0:
            break
        elif opcija == 1:
            unosDirektorijuma()
            initialize()
        elif opcija == 2:
            reci = input("Unesite reci za pretragu:\t")
            poslednja_pretraga = reci
            pretrazi(reci)  # elif opcija == 3:
        elif opcija == 3:
            step = int(input("Unesite broj linkova po stranici:\t"))
            broj_strana = vidjeno_strana +step
            print_pages()
        elif opcija == 4:
            vidjeno_strana = broj_strana
            broj_strana = broj_strana + step
            print_pages()
        elif opcija == 5:
            broj_strana = vidjeno_strana
            vidjeno_strana = vidjeno_strana - step
            print_pages()


    except Exception as e:
        print(e)
        print("--------------------Unesite broj kao opciju.--------------------- \n")
