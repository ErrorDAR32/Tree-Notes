from struct import pack

obj_opening = 0
obj_closing = 1
field_tag = 2
named_tag = 3


class SSSObject:
    def __init__(self, fields=None, named_fields=None):
        if fields is None:
            fields = []
        if named_fields is None:
            named_fields = {}
        self.fields = fields
        self.named_fields = named_fields


class FileWrapper:
    """File wrapper used for loading SSS files into memory"""
    def __init__(self, File):
        self.data = File
        self.data.seek(0)
        self.byte = b''

    def next(self):
        self.byte = self.data.read(1)
        if self.byte != b'':
            self.byte = self.byte[0]
        return self.byte

    def current(self):
        return self.byte


class IterWrapper:
    """iterable wrapper used for parsing"""
    def __init__(self, iterable):
        self.length = len(iterable)
        self.iterable = iter(iterable)
        self.curr = None

    def next(self):
        if self.length != 0:
            self.curr = self.iterable.__next__()
        self.length -= 1
        return self.curr

    def current(self):
        return self.curr


def tokenize(file: FileWrapper):
    """tokenizes a file"""
    tokens = []
    file.next()
    while True:
        if file.current() == obj_opening:
            tokens.append(obj_opening)

        elif file.current() == obj_closing:
            tokens.append(obj_closing)

        elif file.current() == named_tag:
            tokens.append(named_tag)

        elif file.current() == field_tag:
            length = bytearray()

            for n in range(8):
                length.append(file.next())

            length = int.from_bytes(length, "big")
            data = bytearray()

            for n in range(length):
                data.append(file.next())

            tokens.append(field_tag)
            tokens.append(bytes(data))
        else:
            raise SyntaxError(f"unexpected char {file.data.tell(), file.current()}")
        if file.next() == b'':
            return tokens


def parseobj(tokens):
    """parses an SSS object from a tokens array"""
    obj = SSSObject()
    while True:
        tokens.next()
        if tokens.current() == obj_closing:
            return obj

        if tokens.current() == named_tag:
            field1, field2 = parsenamed(tokens)
            obj.named_fields[field1] = field2

        elif tokens.current() == field_tag:
            obj.fields.append(parsefield(tokens))

        elif tokens.current() == obj_opening:
            obj.fields.append(parseobj(tokens))

        else:
            raise SyntaxError(
                f"unexpected char {tokens.current()} at {tokens.pointer()}, expected {field_tag} or {obj_opening}")


def parsenamed(tokens):
    """parses a named field"""
    tokens.next()
    if tokens.current() == field_tag:
        field1 = tokens.next()
    else:
        raise SyntaxError(f"unexpected char {tokens.current()} at {tokens.pointer()}, expected {field_tag}")
    tokens.next()
    if tokens.current() == field_tag:
        field2 = tokens.next()
    elif tokens.current() == obj_opening:
        field2 = parseobj(tokens)
    else:
        raise SyntaxError(
            f"unexpected char {tokens.current()} at {tokens.pointer()}, expected {field_tag} or {obj_opening}")
    return field1, field2


def parsefield(tokens):
    """parses a field"""
    return tokens.next()


def parse(file):
    """you give it a file, it gives you a SSSObject"""
    file = FileWrapper(file)
    file.next()
    if file.current() == obj_opening:
        return \
            parseobj(
                IterWrapper(
                    tokenize(file)
                )
            )
    else:
        raise SyntaxError(f"unexpected char {file.current()}")


def serializefield(field):
    serialized = bytearray()
    if isinstance(field, SSSObject):
        serialized.extend(serialize(field))
    elif isinstance(field, bytes):
        serialized.append(field_tag)
        serialized.extend(pack(">Q", len(field)))
        serialized.extend(field)
    return serialized


def serializenamed(key, field):
    serialized = bytearray()
    serialized.append(named_tag)

    serialized.append(field_tag)
    serialized.extend(pack(">Q", len(key)))
    serialized.extend(key)

    if isinstance(field, SSSObject):
        serialized.extend(serialize(field))
    elif isinstance(field, bytes):
        serialized.append(field_tag)
        serialized.extend(pack(">Q", len(field)))
        serialized.extend(field)
    return serialized


def serialize(obj: SSSObject):
    """used convert SSSObjects into a byte arrays"""
    serialized = bytearray()
    serialized.append(obj_opening)

    for field in obj.fields:
        serialized.extend(serializefield(field))

    for key, field in obj.named_fields.items():
        serialized.extend(serializenamed(key, field))

    serialized.append(obj_closing)
    return serialized
