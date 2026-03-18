import tkinter as tk


class SubMaster:
    def __init__(self):
        self._sub_win = None

    def sub_win_close(self):
        self._sub_win = None

    def close(self):
        self._sub_win.force_close()

    def create_win(self, sub_win_obj):
        if not self._sub_win:
            self._sub_win = sub_win_obj
        self._sub_win.focus_set()


class SubWin:
    def __init__(self, root: tk.Tk, master, title=None):
        self._master = master
        self._my_window = tk.Toplevel(root)
        self._my_window.title(title)
        self._my_window.geometry('750x250')
        self._my_window.resizable(True, True)
        self._my_window.protocol('WM_DELETE_WINDOW', self._close_cmd)

    def focus_set(self):
        self._my_window.focus_set()

    def _close_cmd(self, *_):
        self._master.sub_win_close()
        self._my_window.destroy()

    def _submit_cmd(self, *_):
        self._close_cmd()

    def force_close(self):
        self._close_cmd()
