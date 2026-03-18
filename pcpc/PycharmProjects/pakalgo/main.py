from menu import *


def do_quit(root, table, main_menu):
    if ask_for_save(table, main_menu):
        root.destroy()


def main():
    root = tk.Tk()
    root.title(DEF_SCREEN_TITLE)
    main_frame = tk.Frame(root)

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    main_frame.grid(row=0, column=0, sticky=tk.NSEW)

    table = PakalTable(root, main_frame, (0, 0))
    menu = MainMenu(root, table)
    table.set_menu(menu)

    credit_label = tk.Label(root, text=f"Pakalgo by Yuval Kalanthroff", bd=1, relief=tk.SUNKEN)
    credit_label.grid(row=1, column=0, sticky=tk.NSEW)

    root.protocol('WM_DELETE_WINDOW', lambda: do_quit(root, table, menu))
    root.mainloop()


if __name__ == '__main__':
    main()
