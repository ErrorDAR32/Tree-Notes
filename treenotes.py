#!/usr/bin/python3
# suposed to be a simple sintax, but theres probably a better way to do this
import curses


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

    "oldload": (
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
        while len(schema) > len(args):
            args.append(None)

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
    thingys = ('"',"'")
    for arg in range(len(args)):
        if args[arg] is not None:

            if (args[arg][0] in thingys) and (args[arg][-1] in thingys):
                args[arg] = str(args[arg][1:-1])
                continue
            if args[arg].isnumeric() is True:
                args[arg] = int(args[arg])
                continue

    return cmd, args


def execute(node, function, arguments):
    global root
    global gotoroot
    if function in ["save","load"]:
        gotoroot = True
        lul = functions.get(function, None)  # yeah, lul, i know, im creative
        lul(root, arguments)
    else:
        lul = functions.get(function, None)  # yeah, lul, i know, im creative
        lul(node, arguments)

# utility functions

class filewrapper:
    def __init__(self, string: str):
        self.string = string
        self.charptr = 0
        self.char = string[0]

    def checkcharptr(self):
        if self.charptr == len(self.string):
            return False
        return True
    def nextchar(self):
        if self.checkcharptr():
            self.charptr += 1
            self.char = self.string[self.charptr]
            return self.string[self.charptr]
        return None

    def currchar(self):
        return self.string[self.charptr]

    def lastchar(self):
        return self.string[self.charptr - 1]


def parsenode(file: filewrapper):
    node = Node()
    props = ("a","t","c")
    while True:
        if file.nextchar() in props:
            if file.currchar() == "a":
                node.alias = parseproperty(file)
            elif file.currchar() == "t":
                node.text = parseproperty(file)
            elif file.currchar() == "c":
                node.childs = parseproperty(file)
        elif file.currchar() == "}":
            return node


def parsearray(file: filewrapper):
    array = []
    while True:
        if file.nextchar() == "]":
            return array
        elif file.currchar() == "{":
            array.append(parsenode(file))


def parsestring(file: filewrapper):
    string = ""
    while True:
        file.nextchar()
        if (file.currchar() == '"') and (file.lastchar() != '\ '[0]):
            return string
        string += file.currchar()


def parseproperty(file: filewrapper):
    while True:
        if file.nextchar() == '"':
            return parsestring(file)
        elif file.currchar() == '[':
            return parsearray(file)


def preview_text(text,iden=0):
    res = ""
    for char in range(len(text)):
        res += text[char]
        if text[char] == "\n":
            for space in range(iden):
                res += " "

    if len(res) <= 64:
        return text
    else:
        return res[:64] + "..."


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

def editor(string: str,toptext = "press crtl + x to exit"):
    # util
    class textwrapper:
        text = [[], ]
        y = 0
        x = 0

        def __init__(self, text: str):
            if text is None:
                return
            self.text = []
            temp = text.split("\n")
            for line in temp:
                self.text.append(list(line))

        def __len__(self):
            return len(self.text)

        def __iter__(self):
            return self.text.__iter__()

        def splitline(self):
            self.text.insert(self.y + 1, self.text[self.y][self.x:])
            self.text[self.y] = self.text[self.y][:self.x]
            self.y += 1
            self.x = 0

        def unite_lines(self,): # only to use when cursor is at x == 0
            if self.y != len(self.text) - 1:
                self.text[self.y] += self.text[self.y + 1]
                self.text.pop(self.y + 1)

        def insert_char(self, char, y=None, x=None, ):
            if x is None:
                x = self.x
            if y is None:
                y = self.y

            if char == "\n":
                self.splitline()
            else:
                self.text[y].insert(x, char)
                self.x += 1

        def delete_backspace(self):
            if self.x != 0:
                self.text[self.y].pop(self.x - 1)
                self.move_left()
            elif self.y != 0: # when deleteing a line
                self.move_up() # unite_lines is always the current line with the next line
                self.x = len(self.text[self.y])
                self.unite_lines()

        def delete_supr(self):
            if self.x != len(self.text[self.y]):
                self.text[self.y].pop(self.x)
            elif self.y != len(self.text) - 1:  # when deleteing a line
                self.x = len(self.text[self.y])
                self.unite_lines()

        def adjust_x(self):
            if self.x > len(self.text[self.y]):
                self.x = len(self.text[self.y])

        def move_left(self):
            if self.x != 0:
                self.x -= 1
            elif self.y != 0:
                self.move_up()
                self.x = len(self.text[self.y])

        def move_right(self):
            if not (self.x >= len(self.text[self.y])):
                self.x += 1
            elif self.y != len(self.text) - 1:
                self.move_down()
                self.x = 0

        def move_up(self):
            if self.y != 0:
                self.y -= 1
                self.adjust_x()

        def move_down(self):
            if not (self.y >= len(self.text) - 1):
                self.y += 1
                self.adjust_x()

        def flush(self):
            res = ""
            for line in range(len(self.text)):
                for char in range(len(self.text[line])):
                    res += self.text[line][char]

                if line != len(self.text) - 1:
                    res+= "\n"
            return res


    class text_renderer:

        text = textwrapper("")
        x_txt_offset = 0
        y_txt_offset = 0

        def __init__(self,stdscr: curses.window, text: textwrapper):
            self.text = text
            self.stdscr = stdscr

        def render(self,yfst=0, xfst=0,key="",stdscr=None):
            if stdscr is None:
                stdscr = self.stdscr
            stdscr.clear()
            stdscr.refresh()
            stdscr.move(0, 0)

            lines = curses.LINES - yfst
            columns = curses.COLS - xfst

            if self.text.x > self.x_txt_offset + columns - 1:
                self.x_txt_offset = self.text.x - columns + 1
            elif self.text.x < self.x_txt_offset:
                self.x_txt_offset = self.x_txt_offset - (self.x_txt_offset - self.text.x)

            if self.text.y > self.y_txt_offset + lines - 1:
                self.y_txt_offset = self.text.y - lines + 1
            elif self.text.y < self.y_txt_offset:
                self.y_txt_offset = self.y_txt_offset - (self.y_txt_offset - self.text.y)

            # rendering the text:
            for line in range(len(self.text.text)):
                if (line < self.y_txt_offset) or (line > self.y_txt_offset + lines - yfst):
                    continue
                stdscr.move(line - self.y_txt_offset + yfst, 0 + xfst)

                for char in range(len(self.text.text[line])):
                    if (char < self.x_txt_offset) or (char > self.x_txt_offset + columns - 1) :
                        continue
                    stdscr.addch(self.text.text[line][char])

            # position cursos to where user is editing
            stdscr.move(self.text.y + yfst - self.y_txt_offset, self.text.x + xfst - self.x_txt_offset)
            stdscr.refresh()


    # main function
    def main(stdscr: curses.window):
        # initialization
        curses.curs_set(True)
        curses.noecho()
        text = textwrapper(string)
        renderer = text_renderer(stdscr,text)

        # main_loop
        key = ""
        while True:
            renderer.render(1, 1, key)
            coords = stdscr.getyx()
            stdscr.move(0,0)
            stdscr.addstr(toptext)
            stdscr.move(coords[0], coords[1])


            key = stdscr.getkey()

            if key == "KEY_LEFT":
                text.move_left()
            elif key == "KEY_RIGHT":
                text.move_right()
            elif key == "KEY_UP":
                text.move_up()
            elif key == "KEY_DOWN":
                text.move_down()
            elif key == "KEY_BACKSPACE":
                text.delete_backspace()
            elif key == "KEY_DC":
                text.delete_supr()
            elif key == "\x18":
                stdscr.move(0,0)
                stdscr.addstr(" do you want to save? y/n")
                while True:
                    key = stdscr.getkey()
                    if key == "y":
                        return text.flush()
                    elif key == "n":
                        return False

            elif len(key) == 1:
                text.insert_char(key)

    saved = curses.wrapper(main)
    if saved == False:
        return False
    else:
        return saved


def save(node, args):
    """save <filename>
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
    res += 'a'
    res += '"' + node.alias + '"'
    res += ','
    res += 't'
    res += '"' + node.text + '"'
    res += ','
    res += 'c'
    res += "["
    for child in node.childs:
        res += save(child, None)
        res += ","
    res += "]"
    res += "}"

    if args is not None:
        try:
            with open(recent_file, "wt") as f:
                f.write(res)
            print("Save successful")
        except:
            print("error while reading file")
            return
    else:
        return res


def oldload(node, args, recursive=False):
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
                                child, delta = oldload(Node(), file[pointer + 1:], True)
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


def load(node, args):
    """load <filename>
    used to load a note tree from storage, if no argument is given it will try to use the last file name used by
    save, csave, or load"""
    global recent_file
    if args[0] is None:
        if recent_file == "":
            print("argument missing, and no recent file detected")
            return
        elif descision(f"do you want to load {recent_file}? (Y/N)") == 1:
            return
    else:
        recent_file = args[0]

    try:
        with open(recent_file, "rt") as f:
            file = filewrapper(f.read())
    except:
        print(f"Error while reading {recent_file}")
        return


    while True:
        if file.currchar() == "{":
            newnode = parsenode(file)
            node.reset()
            node.text = newnode.text
            node.childs = newnode.childs
            node.alias = newnode.alias

            break
        file.nextchar()


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
            node.text = editor(node.text)
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
            name = "node"

        print(name, ":", preview_text(node.text,len(name) + 3))

        for child in range(len(node.childs)):
            name = ""
            if node.childs[child].has_alias():
                name = node.childs[child].alias
            else:
                name = child

            print(" ", name, ":", preview_text(node.childs[child].text,len(name) + 5))


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


        print(" " * space, name,":", preview_text(node.childs[child].text,len(name) + space + 4))
        rpreview(node.childs[child], space + 4)

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
        print(node.alias)
    place = node.alias.find(term)
    if place != -1:
        print(f"{term} found in alias of {route} in char {place}")

    for child in range(len(node.childs)):
        if node.childs[child].has_alias():
            name = node.childs[child].alias
        else:
            name = str(child)

        search(node.childs[child], term, route + name + "/")


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


functions = {"save": save, "load": load,"oldload": oldload, "create": create, "delete": delete, "edit": edit,
             "see": see, "preview": preview, "rpreview": rpreview, "search": search, "alias": alias_node}


recent_file = ""
gotoroot = False
multibrowse = []
# main function and loop

def main(node, is_subnode=False):
    global root
    global gotoroot
    global multibrowse
    current_file = None
    cmd = ""
    args = [None]
    while True:
        if gotoroot is True:
            if is_subnode is True:
                return
            else:
                gotoroot = False

        if len(multibrowse) == 0:
            cmd, args = tokenizer(input(str(node.alias) + " >: "))
        else:
            if isinstance(multibrowse[0], str):
                multibrowse[0] = alias_to_index(node,multibrowse[0])

            if multibrowse[0] is not None:
                if multibrowse[0] is not False:
                    if multibrowse[0] < len(node.childs):
                        main(node.childs[multibrowse.pop(0)], is_subnode=True)
                    else:
                        print("unknown alias/node")
                        multibrowse = []
            continue

        # primordial commands
        if cmd == "browse":
            if len(args) > 1:
                multibrowse = args
                continue

            if isinstance(args[0], str):
                args[0] = alias_to_index(node,args[0])

            if args[0] is not None:
                if args[0] is not False:
                    if args[0] < len(node.childs):
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
                    save(root,recent_file)
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
    print("see github.com/ErrorDAR32/Tree-Notes for the source")
    print("type help for help for a list of commands or help <command> for more detailed help")

    main(root)
