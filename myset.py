from data import MyData


class MySet:

    def __init__(self):
        self.list = []

    def __addToSet__(self, filepath, occ):
        for item in self.list:
            if item.abspath == filepath:
                item.brPonavljanja = item.brPonavljanja + occ
                return
        self.list.append(MyData(filepath, occ))

    def __intersection__(self, other):
        intersection_array = []
        for item in self.list:
            for item1 in other.list:
                if item.abspath == item1.abspath:
                    intersection_array.append(item)
        return intersection_array

    def __union__(self, other):
        intersection_array = self.list
        for item in other.list:
            flag = True
            for item1 in intersection_array:
                if item.abspath == item1.abspath:
                    flag = False
            if flag == True:
                intersection_array.append(item)
        return intersection_array

    def __complement__(self, other):
        intersection_array = self.list
        for item in other.list:
            for item1 in intersection_array[:]:
                if item.abspath == item1.abspath:
                    intersection_array.remove(item1)
        return intersection_array
