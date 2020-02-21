
class Trie:

    def __init__(self):
        self.path = {}
        self.occurrance = {}

    def __addToTrie__(self, word, index, doc_name):
        head = word[0]
        if head in self.path.keys():
            node = self.path[head]
        else:
            node = Trie()
            self.path[head] = node

        if len(word) > 1:
            rem = word[1:]
            node.__addToTrie__(rem, index, doc_name)
        else:
            if doc_name in node.occurrance.keys():
                node.occurrance[doc_name] = node.occurrance[doc_name] + 1
            else:
                node.occurrance[doc_name] = 1

    def __search__(self, word):
        head = word[0]
        if head in self.path.keys():
            node = self.path[head]
        else:
            return {}
        if len(word) > 1:
            rem = word[1:]
            return node.__search__(rem)
        else:
            return node.occurrance
