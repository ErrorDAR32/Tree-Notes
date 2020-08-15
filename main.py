Sintax_Matrix = {"create":   ((),),  # suposed to be a simple sintax, but theres probably a better way to do this

                 "delete": (
                     (),
                     (int,),
                     (str),),

                 "edit": (
                     (),
                     (int,),
                     (str,),),

                 "see": (
                     (),
                     (int,),
                     (str,),),

                 "preview": (
                     (),
                     (int,),
                     (str,),),

                 "rpreview": ((),),

                 "load":     ((str,)),

                 "save":     ((str,)),

                 "csave":    ((str,)),

                 "search":   ((str,)),

                 "alias": (
                     (str,),
                     (int, str),
                     (str, str))}


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

    return "sintax"


def tokenizer(string):
    args = string.split()
    cmd = args.pop(0)

    # argument_preparation
    if len(args) == 0:
        args.append(None)

    for arg in range(len(args)):
        if args[arg] is not None:
            if args[arg].isnumeric() is True:
                args[arg] = int(args[arg])
    return cmd, args

def execute(node, function, arguments):
    try:
        lul = functions.get(function, None)
        if function == "alias":  # band aid before fixing rest of functions
            lul(node, arguments)
        else:
            lul(node, arguments[0])
    except:
        print("Error while executing command")


class Node:
    def __init__(self, text="", childs=None):
        if childs is None:
            childs = []
        self.childs = childs
        self.text = text
        self.alias = ""

    def reset(self):
        self.childs = []
        self.text = ""
        self.alias = ""


def editor(string=""):  # coming soon
    return input(">->")


def save(node: Node, file, inden=0):
    res = " " * inden + '{'
    res += "("
    res += node.alias
    res += ")"
    res += '"'
    res += node.text
    res += '"'
    res += "\n" + " " * inden + "["
    for child in node.childs:
        res += "\n" + save(child, None, inden + 4)
    res += "]"
    res += "}"
    if file is not None:
        with open(file, "wt") as f:
            f.write(res)
    else:
        return res


def csave(node, file):
    res = '{'
    res += "("
    res += node.alias
    res += ")"
    res += '"'
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


def load(node, file, recursive=False):
    if recursive is False:
        with open(file, "rt") as f:
            file = f.read()

    if recursive is False:
        node.reset()
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

                if file[pointer] == '(':
                    pointer += 1
                    while file[pointer] != ')':
                        node.alias += file[pointer]

                        pointer += 1
                if file[pointer] == "[":
                    if file[pointer + 1] != "]":
                        while file[pointer + 1] != "]":
                            child, delta = load(Node(), file[pointer + 1:], True)
                            pointer += delta
                            node.childs.append(child)
                    pointer += 1

                if file[pointer] == "}":
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
        print(" " * space, number, end=" ")
        rpreview(child, space + 2)
        number += 1
    return


def search(node: Node, search_term, route=None):
    result = ""
    if route is None:
        route = preview_text(node.text)

    place = node.text.find(search_term)
    if place != -1:
        result = f"'{search_term}' located at char {place} in {route}\n"

    for child in range(len(node.childs)):
        find = search(node.childs[child], search_term, route + "/" + str(child))
        if find is not None:
            result += find

    if route == preview_text(node.text):
        print(result)

    return result


def alias(node, args):
    if len(args) == 1:
        node.alias = args[0]
        return
    if len(args) == 2:
        if isinstance(args[0],int):
            node.childs[args[0]].alias = args[1]
        elif isinstance(args[0],str):
            for child in node.childs:
                if child.alias == args[0]:
                    child.alias = args[1]
    else:
        print("incorrect number/alias")


def str_list_to_string(lista):
    res = ""
    for word in lista:
        res = res + word
    return res


functions = {"save": save, "load": load, "create": create, "delete": delete, "edit": edit, # removed csave for now
             "see": see, "preview": preview, "rpreview": rpreview, "search": search, "alias": alias}


def main(node, is_subnode=False):
    current_file = None
    while True:
        cmd, args = tokenizer(input(node.alias + " >:"))


        # primordial commands

        if cmd == "browse":
            main(node.childs[args[0]], is_subnode=True)
            continue

        elif cmd == "goup":
            if is_subnode is True:
                return
            else:
                print("can't go further up!")
            continue

        elif cmd == "exit":
            raise SystemExit

        # the rest of the commands
        check = check_sintax(Sintax_Matrix, cmd, args)

        if check is True:
            execute(node, cmd, args)
        elif not check:
            print("unknown command")
        elif check == "sintax":
            print("incorrect sintax")



if __name__ == "__main__":
    import sys

    main(Node())