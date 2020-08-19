# suposed to be a simple sintax, but theres probably a better way to do this
Sintax_Matrix = {
    "create": (
        (),
        (str,)),

    "delete": (
        (),
        (int,),
        (str,),),

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

    "load": (
        (),
        (str,),),

    "save": (
        (),
        (str,),),

    "csave": (
        (),
        (str,),),

    "search": ((str,),),

    "alias": (
        (str,),
        (int, str),
        (str, str))}


class Node:
    def __init__(self, text="", alias="", childs=None):
        if childs is None:
            childs = []
        self.childs = childs
        self.text = text
        self.alias = alias

    def reset(self):
        self.childs = []
        self.text = ""
        self.alias = ""

    def has_alias(self):
        if (self.alias == "") or (not isinstance(self.alias, str)):
            return False
        else:
            return True


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

# command parsing and sintax checks

def tokenizer(string):
    if (not isinstance(string,str) or (len(string) <= 1)):
        return [None,None]
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
    global root
    if function in ["save","csave","load"]:
        lul = functions.get(function, None)  # yeah, lul, i know, im creative
        lul(root, arguments)
    else:
        lul = functions.get(function, None)  # yeah, lul, i know, im creative
        lul(node, arguments)

# utility functions

def preview_text(text):
    if len(text) <= 30:
        return text
    else:
        return text[:30] + "..."


def descision(prompt:str,options=[["Y","y"],["N","n"]]):
    while True:
        choice = input(prompt)
        for option in options:
            if isinstance(option,list):
                for version in option:
                    if version == choice:
                        return option
            elif isinstance(option,str):
                if option == choice:
                    return option


def alias_to_index(node, args):
    for child in range(len(node.childs)):
        if node.childs[child].alias == args:
            return child
    return False

# commands

def editor(string=""):  # TODO implement this 'fore 1.0
    return input(">->")


def save(node: Node, args, inden=0):
    """save <filename>
        used to store human readable version of the current note structure, if no argument is given it will try to use
        the last file name used by save, csave, or load """
    global recent_file

    if args is not None:
        if args[0] is None:
            if recent_file == "":
                print("argument missing, and no recent file detected")
                return
            if descision(f"do you want to save to {recent_file}? (Y/N)") == 1:
                return
        else:
            recent_file = args[0]

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
    if args is not None:
        try:
            with open(recent_file, "wt") as f:
                f.write(res)
            print("Save successful")
        except:
            print("filename error")
            return
    else:
        return res


def csave(node, args):
    """csave <filename>
    used to store a more compact version of the current note structure, if no argument is given it will try to use
    the last file name used by save, csave, or load """
    global recent_file
    if args is not None:
        if args[0] is None:
            if recent_file == "":
                print("argument missing, and no recent file detected")
                return
            if descision(f"do you want to save to {recent_file}? (Y/N)") == 1:
                return
        else:
            recent_file = args[0]

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

    if args is not None:
        try:
            with open(recent_file, "wt") as f:
                f.write(res)
            print("Save successful")
        except:
            print("Filename error")
            return
    else:
        return res


def load(node, args, recursive=False):
    """load <filename>
    used to load a note tree from storage, if no argument is given it will try to use the last file name used by
    save, csave, or load"""
    global recent_file
    file = ""
    if recursive is False:
        if args[0] is None:
            if recent_file == "":
                print("argument missing, and no recent file detected")
                return
            if descision(f"do you want to load {recent_file}? (Y/N)") == 1:
                return
        else:
            recent_file = args[0]

        try:
            with open(recent_file, "rt") as f:
                file = f.read()
        except:
            print(f"Error while reading {recent_file}")
            return
    else:
        file = args

    pointer = 0

    node.reset()

    try:
        while True:
            if file[pointer] == "{":
                pointer += 1

                while True:
                    if file[pointer] == '(':
                        pointer += 1
                        while file[pointer] != ')':
                            node.alias += file[pointer]

                            pointer += 1

                    if file[pointer] == '"':
                        pointer += 1
                        while (file[pointer] != '"') and (file[pointer - 1] != '\ '[0]):
                            node.text += file[pointer]

                            pointer += 1

                    if file[pointer] == "[":
                        if file[pointer + 1] != "]":
                            while file[pointer + 1] != "]":
                                child, delta = load(Node(), file[pointer + 1:], True)
                                pointer += delta
                                node.childs.append(child)
                        pointer += 1

                    if file[pointer] == "}":
                        if recursive is False:
                            print(f"Loaded {recent_file} succesfully")
                            return
                        else:
                            return node, pointer + 1

                    pointer += 1

            pointer += 1
    except:
        print(f"Error while parsing {recent_file}")
        return

def create(node, args):
    """create <alias>
    used to create a new node as a child of the current node, if no argument is given it wors just fine"""
    if args[0] is None:
        args[0] = ""
    if isinstance(args[0], str):
        node.childs.append(Node(alias=args[0]))


def delete(node, args):
    """delete <node>
    used to delete a child of the current node"""
    if isinstance(args[0], str):
        args[0] = alias_to_index(node, args[0])
    if args[0] is not False:
        node.childs.pop(args[0])


def edit(node, args):
    """edit <node>
    used to edit the text of a node"""
    child = args[0]
    if isinstance(child, str):
        child = alias_to_index(node, child)
    if child is not False:
        if child is None:
            node.text = editor()
            return
        if child >= len(node.childs):
            print("wrong index")
            return
        else:
            node.childs[child].text = editor(node.childs[child].text)


def see(node, args):
    """see <node>
    used to see the text of the current node or a child of it"""
    child = args[0]

    if isinstance(child, str):
        child = alias_to_index(node, child)
    if child is not False:
        if child is None:
            print(node.text)
        else:
            if child > len(node.childs) - 1:
                print("Invalid number")
            else:
                child = int(child)
                print(node.childs[child].text)


def preview(node, args):
    """preview <node>
    used to visualize al chids from current node, or assigned node in argument"""
    if args[0] is not None:
        child = args[0]
        if isinstance(child, str):
            child = alias_to_index(node, child)
        if child is not False:
            preview(node.childs[child],[None])
            return
    else:
        if node.has_alias():
            name = node.alias
        else:
            if node.text == "":
                name = "Node"
        print(name, ":", preview_text(node.text))

        for child in range(len(node.childs)):
            name = ""
            if node.childs[child].has_alias():
                name = node.childs[child].alias
            else:
                name = child

            print(" ", name, ":", preview_text(node.childs[child].text))


def rpreview(node, space=0):
    """ rpreview
    used to recursively display all subnodes, to visualize the structure"""
    if not isinstance(space,int):
        space = 0
        if node.has_alias():
            print(node.alias)
        else:
            if node.text == "":
                print("Node")
            else:
                print(preview_text(node.text))


    for child in range(len(node.childs)):

        if node.childs[child].has_alias():
            name = node.childs[child].alias
        else:
            name = child


        print(" " * space, name,":", preview_text(node.childs[child].text))
        rpreview(node.childs[child], space + 2)

    return


def search(node: Node, args, route=None):
    """search <search term>
        recursive search for search term"""
    if route is None:
        if node.has_alias():
            route = node.alias + "/"
        else:
            route = "node" + "/"

    if isinstance(args, list):
        term = args[0]
    else:
        term = args

    place = node.text.find(term)
    if place != -1:
        print(f"{term} found in text of {route} in char {place}")

    place = node.alias.find(term)
    if place != -1:
        print(f"{term} found in alias of {route} in char {place}")

    for child in range(len(node.childs)):
        if node.childs[child].has_alias:
            name = node.childs[child].alias
        else:
            name = child

        search(node.childs[child], term, route + name)


def alias_node(node, args):
    """alias <alias> / <index> <alias> / <old alias> <new alias>
        used to alias a note, to avoid using its index and remembering it easier"""
    if len(args) == 1:
        node.alias = args[0]
        return

    oldalias = args[0]
    newalias = args[1]

    if len(args) == 2:
        if isinstance(oldalias, int):
            node.childs[oldalias].alias = newalias
        elif isinstance(oldalias, str):
            index = alias_to_index(node, oldalias)
            if index != False:
                node.childs[index].alias = newalias
    else:
        print("incorrect number/alias")

def help(command):
    if command is None:
        print("list of commands:")
        print("help\nbrowse\ngoup\nexit")
        for command in functions.keys():
            print(command)
        return

    if command == "help":
        print(
        """help <command>
        used to display help""")
        return
    elif command == "browse":
        print(
            """browse <node>
            used to navigate down the structure"""
        )
        return
    elif command == "goup":
        print("""
        goup
        the contrary to browse, to go back up the structure""")
        return
    elif command == "exit":
        print("exit\nused to exit the program, it prompts a save question before leaving")
        return

    elif isinstance(command,str):
        function = functions.get(command,None)
        if function is None:
            print("Unknown command")
        else:
            print(function.__doc__)


functions = {"save": save, "csave": csave, "load": load, "create": create, "delete": delete, "edit": edit,
             "see": see, "preview": preview, "rpreview": rpreview, "search": search, "alias": alias_node}


recent_file = ""

# main function and loop

def main(node, is_subnode=False):
    global root
    current_file = None
    while True:
        cmd, args = tokenizer(input(str(node.alias) + " >: "))

        # primordial commands
        if cmd == "browse":
            if isinstance(args[0], str):
                args[0] = alias_to_index(node,args[0])

            if args[0] is not None:
                if args[0] is not False:
                    main(node.childs[args[0]], is_subnode=True)

                elif args[0] < node.childs:
                    main(node.childs[args[0]], is_subnode=True)
                else:
                    print("unknown alias/node")
            continue

        elif cmd == "goup":
            if is_subnode is True:
                return
            else:
                print("can't go further up!")
            continue

        elif cmd == "exit":
            if recent_file != "":
                if descision(f"do you want to save to {recent_file}? (Y/N)") == 0:
                    csave(root,recent_file)
            raise SystemExit

        elif cmd == "help":
            help(args[0])
            continue

        # the rest of the commands
        check = check_sintax(Sintax_Matrix, cmd, args)

        if check is True:
            execute(node, cmd, args)
        elif not check:
            print("unknown command")
        elif check == "sintax":
            print("incorrect sintax")

# for the lols
if __name__ == "__main__":
    from sys import argv

    root = Node(alias="notes")
    if len(argv) > 1:
        print("CLI args detected. Executing...")
        execute(root, argv[1], argv[2:])

    print("Tree-notes v0.95")
    print("type help for help for a list of commands or help <command> for more detailed help")

    main(root)
