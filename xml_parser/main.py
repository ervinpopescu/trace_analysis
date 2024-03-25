#!/usr/bin/env python

import argparse
import pathlib

from modules.menu import Menu


def main():
    argparser = argparse.ArgumentParser(
        prog="parse_trace.py", description="Parse Apigee trace"
    )
    argparser.add_argument("target")
    args = argparser.parse_args()
    menu = Menu(pathlib.Path(args.target))
    menu.parser.json()
    menu_config = dict(
        clear_screen=True,
        cycle_cursor=True,
        menu_cursor_style=("fg_red", "bold"),
        menu_cursor="> ",
        menu_highlight_style=("bg_red", "fg_yellow"),
        quit_keys=("escape", "backspace"),
        raise_error_on_interrupt=True,
    )
    menu.main_menu_loop(menu_config)
    return 0


if __name__ == "__main__":
    main()
