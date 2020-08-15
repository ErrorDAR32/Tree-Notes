Sintax_Matrix = {"create"  : ((),),  # suposed to be a simple sintax, but theres probably a better way to do this

                 "delete"  : (
                     (),
                     (int,)),

                 "edit"    : (
                     (),
                     (int,)),

                 "see"     : (
                     (),
                     (int,)),

                 "preview" : (
                     (),
                     (int,)),

                 "rpreview": ((),),

                 "load"    : (
                     (),
                     (str,)),

                 "save"    : (
                     (),
                     (str,)),

                 "csave"   : (
                     (),
                     (str,))}


def check_sintax(sintax_matrix: dict, command, args):
    command_sintax = sintax_matrix.get(command, None)
    if command_sintax is None:
        return False


    for schema in command_sintax:
        valid = True
        if len(schema) == 0:
            schema = (type(None),)
        for scheme_element, arg in zip(schema, args):  # extra arguments are tottaly ignored

            if isinstance(arg, scheme_element):
                continue
            else:
                valid = False
                break

        if valid:
            return True

    return False


class Node:
    def __init__(self, text="", childs=None):
        if childs is None:
            childs = []
        self.childs = childs
        self.text = text
        self.alias = ""  # for the future


def editor(string=""):  # coming soon
    return input(">->")


def save(node, file, inden=0):
    res = " " * inden + '{"'
    res += node.text
    res += '"'
    res += "\n" + " " * inden + "["
    for child in node.childs:
        res += "\n" + save(child, None , inden + 4)
    res += "]"
    res += "}"
    if file is not None:
        with open(file, "wt") as f:
            f.write(res)
    else:
        return res


def csave(node, file):
    res = '{"'
    res += node.text
    res += '"'
    res += "["
    for child in node.childs:
        res += csave(child, None)
    res += "]"
    res += "}"

    if file is not None:
        with open(file, "wt") as f:
            f.write(res)
    else:
        return res


def load(node, file, recursive = False):
    if recursive is False:
        with open(file, "rt") as f:
            file = f.read()

    first = False
    if node is None:
        first = True
        node = Node()
    pointer = 0

    while True:
        if file[pointer] == "{":
            pointer += 1
            while True:
                if file[pointer] == '"':
                    pointer += 1
                    while (file[pointer] != '"') and (file[pointer - 1] != '\ '[0]):
                        node.text += file[pointer]

                        pointer += 1

                if file[pointer] == "[":
                    if file[pointer + 1] != "]":
                        while file[pointer + 1] != "]":
                            child, delta = load(Node(), file[pointer + 1:],True)
                            pointer += delta
                            node.childs.append(child)
                    pointer += 1

                if file[pointer] == "}":
                    if first is True:
                        return node
                    else:
                        return node, pointer + 1
                pointer += 1

        pointer += 1


def create(node, text=""):
    if text is None:
        text = ""
    node.childs.append(Node(text))


def delete(node, child):
    if child == None:
        return
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
            print("  ", _child, " ", preview_text(node.childs[_child].text), sep="")


def rpreview(node, space=0):
    if space is None:
        space = 0
    number = 0
    print(node.text, sep="")
    for child in node.childs:
        print(" " * space, number , end=" ")
        rpreview(child, space + 2)
        number += 1
    return


def str_list_to_string(lista):
    res = ""
    for word in lista:
        res = res + word
    return res


functions = {"save": save, "csave": csave, "load": load, "create": create, "delete": delete, "edit": edit,
             "see": see, "preview": preview, "rpreview": rpreview}


def commands(node, is_subnode=False):
    current_file = None
    while True:
        args = input(node.text + " >: ").split()
        cmd = args.pop(0)

        # argument_preparation
        if len(args) == 0:
            args.append(None)

        for arg in range(len(args)):
            if args[arg] is not None:
                if args[arg].isnumeric() is True:
                    args[arg] = int(args[arg])
        # argument checking

        # commands

        if cmd == "browse":
            commands(node.childs[args[0]], is_subnode=True)
        elif cmd == "goup":
            if is_subnode is True:
                print("can't go further up!")
            return
        elif cmd == "exit":
            raise SystemExit

        if check_sintax(Sintax_Matrix, cmd, args):
            lul = functions.get(cmd, None)
            lul(node, args[0])
        else:
            print("unknown command")


commands(Node())






