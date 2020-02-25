from trie import Trie
from myset import MySet
import AdjMatGraph
import os

from myparser import Parser

parser = Parser()
g = AdjMatGraph.AdjGraph()

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
    # E = []
    # vertices = {}
    for dirpath, dirnames, filenames in os.walk(direktorijum):
        for fileName in filenames:
            extension = os.path.splitext(fileName)[1]
            if extension == ".html" or extension == ".htm":
                links, words = parser.parse(os.path.join(dirpath, fileName))
                for link in links:
                    g.add_edge(g.add_vertex(os.path.join(dirpath, fileName)), g.add_vertex(link))
                for index, word in enumerate(words):
                    trie.__addToTrie__(
                        word, index, os.path.join(dirpath, fileName))


initialize()
g.page_rank()



# print(len(g.page_ranks))
# sortirano = sorted(g.page_ranks.values())
# print(sortirano)
# # print(g.page_ranks.keys())
# #print(g.page_ranks.values())

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
        for val in final_arr:
            val.rang = g.page_ranks[val.abspath]
        #final_arr.sort(key = lambda x: x.rang , reverse = True)
        sort_results()
        for val in final_arr[vidjeno_strana:broj_strana]:
            print(val.abspath , val.rang , val.brPonavljanja)
    else:
        print("Trazene reci ne postoje")

def sort_results():

    for i in range(len(final_arr)):
        cursor = final_arr[i]
        pos = i

        while pos > 0 and final_arr[pos - 1].rang < cursor.rang:
            # Swap the number down the list
            final_arr[pos] = final_arr[pos - 1]
            pos = pos - 1
        # Break and do the final swap
        final_arr[pos] = cursor




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
            final_arr = []
            pretrazi(reci)  # elif opcija == 3:
        elif opcija == 3:
            step = int(input("Unesite broj linkova po stranici:\t"))
            broj_strana = vidjeno_strana + step
            print_pages()
        elif opcija == 4:
            if broj_strana + step > len(final_arr):
                vidjeno_strana = len(final_arr)-step
                broj_strana = len(final_arr)
            else:
                vidjeno_strana = broj_strana
                broj_strana = broj_strana + step
            print_pages()
        elif opcija == 5:
            if vidjeno_strana - step < 0:
                vidjeno_strana = 0
                broj_strana = step
            else:
                broj_strana = vidjeno_strana
                vidjeno_strana = vidjeno_strana - step
            print_pages()
    except Exception as e:
        print(e)
        print("--------------------Unesite broj kao opciju.--------------------- \n")
