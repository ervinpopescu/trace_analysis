import pathlib

import simple_term_menu
from modules.formatter import OutputFormatter
from modules.parser import XMLParser


class Menu:
    def __init__(self, xml_file_path: pathlib.Path) -> None:
        self.parser = XMLParser(xml_file_path)
        self.output_formatter = OutputFormatter()

    def show_menu(self, menu_config, title, menu_entries):
        return simple_term_menu.TerminalMenu(
            menu_entries=menu_entries,
            title=title,
            **menu_config,
        ).show()

    def on_selected_transaction(self, tr_sel: int):
        match tr_sel:
            case 0:
                self.output_formatter.print_everything(self.parser.everything)
            case 1:
                self.output_formatter.print_policies(self.parser.skipped)
            case 2:
                self.output_formatter.print_policies(self.parser.invoked)
            case 3:
                self.output_formatter.print_flow_infos(self.parser.flow_infos)
        print()
        while True:
            try:
                key = input(
                    "Press Enter to return to previous menu or Ctrl-C to quit.\n"
                )
                if key in ["", "q", "Esc"]:
                    break
            except KeyboardInterrupt:
                print("\033c\033[3J", end="")
                exit(0)

    def transaction_menu_loop(
        self, main_sel, menu_cursor_spaces, menu_config, transaction_menu_exit
    ):
        back_string = "Press Backspace to return to previous menu or Ctrl-C to quit.\n"
        while not transaction_menu_exit:
            transaction_id = self.parser.get_transaction_id(main_sel)
            title = f"{menu_cursor_spaces}Chosen transaction has id `{transaction_id}`.\n{menu_cursor_spaces}{back_string}"
            menu_entries = [
                "Everything",
                "Skipped policies",
                "Invoked policies",
                "Flow infos",
            ]
            try:
                tr_sel = self.show_menu(
                    menu_config=menu_config,
                    menu_entries=menu_entries,
                    title=title,
                )
                if tr_sel is not None:
                    self.on_selected_transaction(tr_sel)
                else:
                    transaction_menu_exit = True
            except KeyboardInterrupt:
                exit(0)

    def main_menu_loop(self, menu_config):
        menu_cursor_spaces = "".join(len(menu_config["menu_cursor"]) * [" "])
        main_menu_exit = False
        transaction_menu_exit = False
        while not main_menu_exit:
            try:
                main_sel = self.show_menu(
                    menu_entries=[
                        f"Transaction {str(i)}"
                        for i in range(len(self.parser.transactions) - 1)
                    ],
                    title=f"{menu_cursor_spaces}File: {self.parser.file}\n  Press Backspace or Ctrl-C to quit. \n",
                    menu_config=menu_config,
                )
                if main_sel is not None:
                    self.parser.set_data(main_sel)
                    self.transaction_menu_loop(
                        main_sel=main_sel,
                        menu_config=menu_config,
                        menu_cursor_spaces=menu_cursor_spaces,
                        transaction_menu_exit=transaction_menu_exit,
                    )
                elif isinstance(main_sel, int):
                    main_menu_exit = True
            except KeyboardInterrupt:
                exit(0)
