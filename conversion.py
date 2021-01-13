import utils
import commands
import SSS
current = utils.Note()
links = {}
# lastfile = None


def save(*args, **kwargs):
    global current
    """Saves the current notes structure into a <name> file.
     If no arguments are provided the last filename will be used.
     Preferably use ".trnts" as file extension!"""
    global lastfile
    global links

    serialized = utils.note_to_sss(utils.getupper(current))
    serialized = SSS.SSSObject(
        named_fields={
            "ver": "2.0",
            "links": SSS.SSSObject(named_fields=links),
            "Notes": serialized})

    serialized = SSS.serialize(serialized)
    print(serialized)
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
    global links

    if args:
        lastfile = open(args[0], "rb+")
    if lastfile is not None:
        notes = SSS.parse(lastfile)
        notes = utils.sss_to_note(notes)

        current = notes
    else:
        print("filename required")


lastfile = open("test.trnts", "rb+")
load()
save()
