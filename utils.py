import SSS


class Note:
    def __init__(self, text="", name="", subnotes=None, father=None):
        if subnotes is None:
            subnotes = []
            subnotes: list[Note]
        self.text = text
        self.name = name
        self.subnotes = subnotes
        self.father = father

    def addchild(self, *args, **kwargs):
        self.subnotes.append(Note(*args, father=self, **kwargs))

    def __repr__(self):
        return f"note {self.name}"


tag_text = "text".encode("UTF-8")
tag_name = "name".encode("UTF-8")


def getupper(note: Note, depth=-1):
    if depth == 0:
        return note
    if note.father is None:
        return note
    else:
        return getupper(note.father,depth - 1)


def note_to_sss(note: Note):
    SSSObj = SSS.SSSObject()
    SSSObj.named_fields[tag_text] = note.text.encode("UTF-8")
    SSSObj.named_fields[tag_name] = note.name.encode("UTF-8")

    for sub in note.subnotes:
        SSSObj.fields.append(note_to_sss(sub))
    return SSSObj


def sss_to_note(sssobj: SSS.SSSObject, father=None):
    n = sssobj.named_fields
    note = Note(
        name=n[tag_name].decode("UTF-8"),
        text=n[tag_text].decode("UTF-8"),
        father=father
    )
    note.subnotes = [sss_to_note(sub, note) for sub in sssobj.fields]
    return note


def get_from_name(current, name):
    for sub in current.subnotes:
        if sub.name == name:
            return sub
    else:
        return None


def escape_name_string(string: str):
    string = string.replace('/', "")
    string = string.replace(" ", "\\ ")
    return string


def descape_name_string(string: str):
    string = string.replace("\\ ", " ")
    return string


def get_route(note: Note, address: str):
    """gets an address and returns a list containing the route to it"""
    if len(address) == 0:
        print("Route required")
        return []
    if address[0] == "/":
        note = getupper(note)
        address = address[1:]

    elif address[:2] == "./":
        # note referenced is current note
        address = address[2:]

    elif address == "..":
        if note.father is None:
            print("Can't go further up.")
            return []
        return [getupper(note, 1), ]

    elif address[:3] == "../":
        if note.father is None:
            print("Can't go further up.")
            return []
        note = getupper(note, 1)
        address = address[3:]

    names = address.split("/")
    route = [note, ]
    if names[0] == '':
        return route

    for name in names:
        for subnote in (name for name in note.subnotes):
            if subnote.name == name:
                note = subnote
                route.append(note)
                break
        else:
            print(f"Invalid name {name}")
    return route
