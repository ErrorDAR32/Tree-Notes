import curses


class Node:
    def __init__(self, text="", childs=None):
        if childs is None:
            childs = []
        self.childs = childs
        self.text = text


def editor(string=""):
    return input()


def save(node, inden=0):
    res = " " * inden + '{"'
    res += node.text
    res += '"'
    res += "\n" + " " * inden + "["
    for child in node.childs:
        res += "\n" + save(child, inden + 4)
    res += "]"
    res += "}"
    return res


def csave(node): # for
    res ='{"'
    res += node.text
    res += '"'
    res += "["
    for child in node.childs:
        res += csave(child)
    res += "]"
    res += "}"
    return res


def load(string, node=None, ):
    first = False
    if node is None:
        first = True
        node = Node()
    pointer = 0

    while True:
        if string[pointer] == "{":
                pointer += 1
                while True:
                    if string[pointer] == '"':
                        pointer += 1
                        while (string[pointer] != '"') and (string[pointer - 1] != '\ '[0]):
                            node.text += string[pointer]

                            pointer += 1

                    if string[pointer] == "[":
                        if string[pointer + 1] != "]":
                            while string[pointer + 1] != "]":
                                child, delta = load(string[pointer + 1:], Node())
                                pointer += delta
                                node.childs.append(child)
                        pointer += 1

                    if string[pointer] == "}":
                        if first == True:
                            return node
                        else:
                            return node, pointer + 1
                    pointer += 1

        pointer += 1


def create(node, text=""):
    node.childs.append(Node(text))


def delete(node, child):
    node.childs.pop(child)


def edit(node, child):
    if child is None:
        node.text = editor()
    else:
        node.childs[child].text = editor(node.childs[child].text)


def see(node, child=None):
    if child is None:
        print(node.text)
    else:
        if child > len(node.childs) - 1:
            print("invalid number")
        else:
            child = int(child)
            print(node.childs[child].text)


def preview_text(text):
    if len(text) <= 30:
        return text
    else:
        return text[:30] + "..."


def preview(node, child=None):
    if child is not None:
        print(preview_text(node.childs[child].text))
    else:
        print(node.text)
        for _child in range(len(node.childs)):
            print("  ", _child + 1, " ", preview_text(node.childs[_child].text), sep="")


def rpreview(node, space=0,):
    number = 1
    print(node.text, sep="")
    for child in node.childs:
        print(" " * space,number ,end=" ")
        rpreview(child, space + 2)
        number += 1
    return


def str_list_to_string(lista):
    res = ""
    for word in lista:
        res = res + word
    return res


def node_navigator(node):
    while True:
        args = input("notes >: ").split()
        cmd = args.pop(0)

        # argument_preparation
        if len(args) == 0:
            args.append(None)

        for arg in range(len(args)):
            if args[arg] is not None:
                if args[arg].isnumeric() is True:
                    args[arg] = int(args[arg])
        # commands

        if cmd == "browse":
            node_navigator(node.childs[args[0]-1])

        elif cmd == "goup":
            return

        elif cmd == "create":
            create(node, editor())

        elif cmd == "delete":
            delete(node, args[0])

        elif cmd == "edit":
            edit(node, args[0])

        elif cmd == "see":
            see(node, args[0])
        elif cmd == "preview":
            preview(node, args[0])

        elif cmd == "rpreview":
            rpreview(node)

        elif cmd == "load":
            try:
                with open(args[0],"rt") as file:
                    node = load(file.read())
            except:
                print("Error loading file")

        elif cmd == "save":
            with open(args[0], "wt") as file:
                file.write(save(node))

        elif cmd == "csave":
            with open(args[0], "wt") as file:
                file.write(csave(node))

        elif cmd == "exit":
            raise SystemExit
        else:
            print("unknown command")


node_navigator(Node())

