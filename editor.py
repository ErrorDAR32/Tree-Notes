import curses


class TextEditorBackend:
    text = [[], ]
    y = 0
    x = 0
    x_render_offst = 0
    y_render_offst = 0

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

    def unite_lines(self, ):  # only to use when cursor is at x == 0
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
        elif self.y != 0:  # when deleteing a line
            self.move_up()  # unite_lines is always the current line with the next line
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
                res += "\n"
        return res


def render(Wtext: TextEditorBackend, yfst=0, xfst=0, stdscr=None):
    stdscr.clear()
    stdscr.refresh()
    stdscr.move(xfst, yfst)

    lines, columns = stdscr.getmaxyx()

    if Wtext.x >= Wtext.x_render_offst + columns - xfst - 1:
        Wtext.x_render_offst = Wtext.x - columns + xfst + 1
    elif Wtext.x < Wtext.x_render_offst:
        Wtext.x_render_offst = Wtext.x
    Wtext.a = Wtext.x_render_offst

    if Wtext.y >= Wtext.y_render_offst + lines - yfst - 1:
        Wtext.y_render_offst = Wtext.y - lines + yfst + 1
    elif Wtext.y < Wtext.y_render_offst:
        Wtext.y_render_offst = Wtext.y

    # rendering the text:
    for line in range(len(Wtext.text)):
        if (line < Wtext.y_render_offst) or (line >= Wtext.y_render_offst + lines - yfst):
            continue
        stdscr.move(line - Wtext.y_render_offst + yfst, 0 + xfst)

        for char in range(len(Wtext.text[line])):
            if (char < Wtext.x_render_offst) or (char >= Wtext.x_render_offst + columns - xfst):
                continue
            stdscr.addch(Wtext.text[line][char])

    # position cursos to where user is editing
    stdscr.move(Wtext.y - Wtext.y_render_offst + yfst, Wtext.x - Wtext.x_render_offst + xfst)
    stdscr.refresh()


def editor(string: str, toptext="press crtl + x to exit"):
    def main(stdscr: curses.window):
        # initialization
        curses.curs_set(True)
        curses.noecho()
        text = TextEditorBackend(string)

        # main_loop
        key = ""
        while True:
            render(text, 1, 1, stdscr)
            coords = stdscr.getyx()
            stdscr.move(0, 0)
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
            # exit char
            elif key == "\x18":
                stdscr.move(0, 0)
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
    if saved is False:
        return False
    else:
        return saved
