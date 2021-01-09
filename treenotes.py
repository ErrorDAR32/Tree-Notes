#!/bin/python3
import commands
import utils

current = utils.Note()

commands.current = current


def main():
    from sys import argv
    if len(argv) > 1:
        args = argv[1:]
        cmd = args
        func = cmd[0]
        args = cmd[1:]
        for f in commands.funcs:
            if f.__name__ == func:
                f(*args)
                break
        else:
            print("invalid command")

    print("mensaje de bienvenida :v")
    while True:
        cmd = input(">>>: ").split()
        if cmd:
            func = cmd[0]
            args = cmd[1:]
        else:
            continue

        for f in commands.funcs:
            if f.__name__ == func:
                f(*args)
                break
        else:
            print("invalid command")


main()
