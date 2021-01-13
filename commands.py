import utils
import SSS
import editor

# this have to be defined in order for most commands to work
current = utils.Note()

# this one is used by save and load to "use" the "last filename"
lastfile = None


def exit(*args, **kwargs):
    """Exit the program. Warning: saving is not automatic!"""
    raise


def see(*args, **kwargs):
    """See the contents of <name> note.
    If no arguments are provided the current note will be used."""
    if args:
        name = args[0]
        for sub in current.subnotes:
            if sub.name == name:
                note = sub
                break
        else:
            print("invalid name")
            return
    else:
        note = current
    print(note.text)


def add(*args, **kwargs):
    """Adds a subnote on the current note named <name>"""
    if args:
        name: str
        name = args[0]
        if name.find(" ") != -1:
            print("name can't have spaces!")
            return
    else:
        print("Name required.")
        return
    if name == '':
        print("Invalid name.")
        return

    for sub in current.subnotes:
        if sub.name == name:
            print("name already used.")
            return
    current.addchild(name=name)


def rem(*args, **kwargs):
    """Delete <name> note.
    Warning: This action cannot be undone!"""
    name = args[0]
    for sub in range(len(current.subnotes)):
        if current.subnotes[sub].name == name:
            current.subnotes.pop(sub)
            return
    else:
        print("Invalid name")


def ls(*args, **kwargs):
    """See the names of the subnotes of the current note or the <name> note."""
    if len(current.subnotes) == 0:
        print("None!")
    for sub in current.subnotes:
        print(sub.name)


def save(*args, **kwargs):
    global current
    """Saves the current notes structure into a <name> file.
     If no arguments are provided the last filename will be used.
     Preferably use ".trnts" as file extension!"""
    global lastfile

    serialized = utils.note_to_sss(utils.getupper(current))
    serialized = SSS.serialize(serialized)

    if args:
        lastfile = open(args[0], "wb+")

    if lastfile is not None:
        lastfile.seek(0)
        lastfile.write(serialized)
        lastfile.flush()
    else:
        print("filename required")


def load(*args, **kwargs):
    """Loads <name> notes file into the program
    If no arguments are provided the last filename will be used.
    """
    global lastfile
    global current

    if args:
        lastfile = open(args[0], "rb+")
    if lastfile is not None:
        notes = SSS.parse(lastfile)
        notes = utils.sss_to_note(notes)
        current = notes
    else:
        print("filename required")


def edit(*args, **kwargs):
    """enters an interactive text editor to edit the text of <name>"""
    if args:
        name = args[0]
        for sub in current.subnotes:
            if sub.name == name:
                note = sub
                break
        else:
            print("invalid name")
            return
    else:
        note = current

    note.text = editor.editor(note.text)


def search(*args, note=None, route="", **kwargs):
    """search"""
    if note is None:
        note = utils.getupper(current)
    route += "/" + note.name
    for arg in args:
        if note.text.find(arg) != (-1):
            print(f"match of {arg} found in text of {route}")
        if note.name.find(arg) != (-1):
            print(f"match of {arg} found at {route}")
    for sub in note.subnotes:
        search(*args, note=sub, route=route)


def prev(*args, **kwargs):
    """Preview the contents of a file, displaying the first 30 characters of the note."""
    note = utils.get_from_name(current, args)
    if note is None:
        note = current
    print(note.text[:30])


def rls(*args, **kwargs):
    """dysplay recursively from the current note the names of each note."""
    def _rls(node, iden=0):
        print(" "*iden, node.name, sep="")
        for sub in node.subnotes:
            _rls(sub, iden + 4)
    _rls(current)


def help(*args, **kwargs):
    """Displays a help text for each function, gives a list of commands if no arguments are given."""
    if args:
        name = args[0]
        if name == "help":
            print(
                "Wellcome To TreeNotes 2.0",
                "This Program is designed to store and manage",
                "named texts structured in a n-tree fashion. called \"notes\".",
                "to interact with the notes, you use the commands provided.",
                "commands can also take arguments to change their functionality.",

                "\nThe next lines will describe a normal use case example as",
                "typed commands and their function, note that when the program",
                "starts, it is already at the Root note.",
                
                "\n>>>: add food.",
                "This command will add a note called \"food\" as a subnote",
                "(a child note of the current note).",
                
                "\n>>>: edit food",
                "This command will edit the text of the note named \"food\" created previously",
                "by entering a simple text editor.",

                "\n>>>: goto food",
                "This will navigate to \"food\", setting it as the current note.",

                "\n>>>: add groceries_list",
                "This will add a subnote of \"food\" called \"groceries_list\", ",
                "note that this note is the grand child of the Root Note.",
                sep="\n")
        for f in functions:
            if f.__name__ == name:
                print(f.__doc__)
                break
        else:
            print("Unknown command.")
    else:
        print("List of commands:", *[f.__name__ for f in functions], sep=" ")
        print("type help <command> for more info.\n"
              "or help help for more help.")


def cn(*args, **kwargs):
    """Navigate trough the notes structure using a cd like syntax.
    You can use / for absolute routes (from Root),
    ./ for relative route from the current Note or
    .. for referring to the upper directory."""
    global current
    full = "".join(args)

    res = utils.get_route(current, full)
    if res:
        current = res[-1]


functions = [
    add,  rem,    see,
    ls,   save, load,
    edit, exit, search,
    prev, rls,  help,
    cn,
]
