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


def goup(*args, **kwargs):
    """Go to the note above in the tree, until you are on the root note"""
    global current
    if current.father is not None:
        current = current.father
    else:
        print("at the root already!")


def goto(*args, **kwargs):
    """Go to <name> note in the subnotes of the current note."""
    name = args[0]
    global current
    for sub in current.subnotes:
        if sub.name == name:
            current = sub
            break
    else:
        print("invalid name!")


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


def create(*args, **kwargs):
    """Create a subnote on the current note named <name>"""
    if args:
        name = args[0]
    else:
        print("name required")
        return
    if name == '':
        print("invalid name!")
        return

    for sub in current.subnotes:
        if sub.name == name:
            print("name already used!")
            return
    current.addchild(name=name)


def delete(*args, **kwargs):
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

    serialized = utils.note_to_sss(utils.getroot(current))
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
        note = utils.getroot(current)
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
    if args:
        name = args[0]
        for f in funcs:
            if f.__name__ == name:
                print(f.__doc__)
                break
        else:
            print("Unknown command")
    else:
        print(" list of commands:", *[f.__name__ for f in funcs], sep=" ")
        print("type help <command> for more info.")



funcs = [create, delete, see, goto, goup, ls, save, load, edit, exit, search, prev, rls, help]


