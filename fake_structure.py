class Node:
    def __init__(self, text, childs=None):
        if childs is None:
            childs = []
        self.childs = childs
        self.text = text

def test_struct():
    return Node("notes",
               [Node("homeworks",
                     [Node("do the dishes"),
                      Node("clean the bedroom"),
                      Node("clean da dust")]),
                Node("Interesting Stuff",
                     [Node("river notes",
                           [Node("check under de rocks"),
                            Node("check house voltages")])]),
                Node("Stranges",
                     [Node("Strangest",
                           [Node("childs are werid"),
                            Node("no one loves me :'v"),
                            Node("Remember to make the note")]),
                      Node("normal strange",
                           [Node("the calculators always give diferent answers"),
                            Node("the dogs whatch  me strangly"),
                            Node("wtf with those shoes?")])])])