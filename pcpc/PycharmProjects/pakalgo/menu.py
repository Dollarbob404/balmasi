import csv
import tkinter
from pakaltable import *
from tkinter import filedialog as fd
import os


class MainMenu(SubMaster):
    def __init__(self, root: tk.Tk, table: PakalTable):
        super().__init__()
        self._root = root
        self._table = table
        self._file_name = ''

        self._main_menu = tk.Menu(root, tearoff=False)

        self._file_menu = tk.Menu(self._main_menu, tearoff=False)
        self._add_menu = tk.Menu(self._main_menu, tearoff=False)
        self._filter_menu = tk.Menu(self._main_menu, tearoff=False)
        self._pakal_menu = tk.Menu(self._main_menu, tearoff=False)

        self._main_menu.add_cascade(label='קובץ', menu=self._file_menu)
        self._file_menu.add_command(label='פתח', command=self.open_file_cmd)
        self._file_menu.add_command(label='חדש', command=self.new_file_cmd)
        self._file_menu.add_separator()
        self._file_menu.add_command(label='שמור', command=self.save_file_cmd)
        self._file_menu.entryconfig('שמור', state='normal' if self._file_name else 'disable')
        self._file_menu.add_command(label='שמור בשם', command=self.save_as_file_cmd)
        self._file_menu.add_separator()
        self._file_menu.add_command(label='ייצוא', command=self._export_file_cmd)
        self._file_menu.add_command(label='ייבוא', command=self._import_file_cmd)

        self._main_menu.add_cascade(label='הוסף', menu=self._add_menu)
        self._add_menu.add_command(label='רשת', command=self._add_net_command)
        self._add_menu.add_command(label='אתר', command=self._add_site_command)

        self._main_menu.add_cascade(label='סינון', menu=self._filter_menu)

        self._filters_counter = 0
        self._btn_relevant_only = tk.IntVar(value=0)
        self._filter_menu.add_checkbutton(label='רלוונטי בלבד', variable=self._btn_relevant_only,
                                          command=self._relevant_only_cmd)
        self._filters_counter += 1

        self._btn_new_only = tk.IntVar(value=0)
        self._filter_menu.add_checkbutton(label='חדש בלבד', variable=self._btn_new_only, command=self._new_only_cmd)
        self._filters_counter += 1

        self._btn_all = tk.IntVar(value=1)
        self._filter_menu.add_checkbutton(label='הכל', variable=self._btn_all, command=self._filter_all_cmd)
        self._filters_counter += 1

        self._groups: List[Tuple[str, tkinter.IntVar]] = []
        self.set_groups()

        self._main_menu.add_cascade(label='פקל', menu=self._pakal_menu)
        self._pakal_menu.add_command(label='הפץ', command=self._set_pakal_cmd)
        self._pakal_menu.add_command(label='משוך', command=self._get_pakal_cmd)

        self._pakal_last_counter = 0

        root.config(menu=self._main_menu)
        root.after(100, self._check_for_update)

    @property
    def file_name(self):
        return self._file_name

    @property
    def filter(self):
        return {key: value.get() for key, value in self._groups}

    def new_file_cmd(self):
        if ask_for_save(self._table, self):
            self._file_name = ''
            self._table.reset()
            self._table.have_changed = False
            self._file_menu.entryconfig('שמור', state='disable')
            self._root.title(DEF_SCREEN_TITLE)
            return True
        return False

    @staticmethod
    def _read_pakal_file(filename):
        try:
            with open(filename, 'r', encoding='utf-8-sig') as my_file:
                content = my_file.read()
        except FileNotFoundError:
            msgbox.showerror('שגיאה!', 'אירע שגיאה בקריאת פקל!')
            return None
        return json.loads(content)

    def open_file_cmd(self, filename=''):
        last_file_name = self._file_name
        if ask_for_save(self._table, self):
            if filename:
                self._file_name = filename
            else:
                self._file_name = fd.askopenfilename(title='פתח קובץ', filetypes=FILE_TYPES, defaultextension='.pkl')
            if self._file_name:
                try:
                    content = self._read_pakal_file(self._file_name)
                    self._table.set_data(content)
                    self._table.have_changed = False
                    self._file_menu.entryconfig('שמור', state='normal')
                    self._set_title()
                    return True
                except Exception as e:
                    msgbox.showerror('Error!', f'can\'t open file! {e}')
                self._file_name = last_file_name
        return False

    def save_file_cmd(self):
        if self._file_name:
            with open(self._file_name, 'w+', encoding='utf-8-sig') as my_file:
                table_data = self._table.to_json
                my_file.write(table_data)
            self._table.have_changed = False
            return True
        return False

    def save_as_file_cmd(self):
        self._file_name = fd.asksaveasfilename(title='שמור קובץ', filetypes=FILE_TYPES, defaultextension='.pkl')
        if self.save_file_cmd():
            self._set_title()
            self._file_menu.entryconfig('שמור', state='normal')
            return True
        return False

    def _export_file_cmd(self):
        file_name = fd.asksaveasfilename(title='שמור קובץ', filetypes=EXPORT_TYPES, defaultextension='.csv')
        table_data = self._table.to_text
        if file_name:
            with open(file_name, 'w+', encoding='utf-8-sig', newline='') as my_file:
                csv_writer = csv.writer(my_file)
                for row in table_data:
                    csv_writer.writerow(row[::-1])

    def _import_file_cmd(self):
        file_name = fd.askopenfilename(title='פתח קובץ', filetypes=IMPORT_TYPES, defaultextension='.csv')
        if file_name:
            table_data = []
            with open(file_name, 'r', encoding='utf-8-sig') as my_file:
                csv_reader = csv.reader(my_file)
                for i, row in enumerate(csv_reader):
                    table_row = []
                    row = row[::-1]
                    for j, cell in enumerate(row):
                        value = cell
                        as_title = i == 0
                        readonly = i == 0 or j > len(row) - len(NET_PARAMS)
                        table_row.append([value, as_title, readonly, CellStatus.NORMAL])
                    table_data.append(table_row)
            self._table.set_data(table_data)
            self._table.have_changed = False

    def _set_title(self):
        self._root.title(os.path.basename(self._file_name))

    def _add_net_command(self):
        if not self._sub_win:
            self.create_win(AddNetWin(self._root, self))
        self._sub_win.focus_set()

    def _add_site_command(self):
        if not self._sub_win:
            self.create_win(AddSiteWin(self._root, self))
        self._sub_win.focus_set()

    def set_groups(self):
        """
        set groups filter from table
        :return:
        """
        # delete old groups
        if self._groups:
            self._filter_menu.delete(self._filters_counter, len(self._groups) + self._filters_counter)
        # create new groups
        self._groups = sorted([(key, tk.IntVar(value=1)) for key in self._table.groups])
        for group, var in self._groups:
            self._filter_menu.add_checkbutton(label=group, variable=var, command=self._filter_changed)

    def add_net(self, values):
        self._table.add_net(*values)

    def add_site(self, values):
        self._table.add_site(values)

    def _new_only_cmd(self):
        self._table.set_filter(self.filter, self._btn_relevant_only.get(), self._btn_new_only.get())

    def _relevant_only_cmd(self):
        self._table.set_filter(self.filter, self._btn_relevant_only.get(), self._btn_new_only.get())

    def _filter_all_cmd(self):
        value = self._btn_all.get()
        for _, var in self._groups:
            var.set(value)
        self._table.set_filter(self.filter, self._btn_relevant_only.get(), self._btn_new_only.get())

    def _filter_changed(self):
        all_on = 1
        for _, var in self._groups:
            all_on &= var.get()
        self._btn_all.set(all_on)
        self._table.set_filter(self.filter, self._btn_relevant_only.get(), self._btn_new_only.get())

    def _set_pakal_cmd(self):
        pakals = os.listdir(PAKAL_FOLDER)
        last_filename = os.path.join(PAKAL_FOLDER, f'pakal{len(pakals) - 1}.pkl')
        last_content = self._read_pakal_file(last_filename)
        table_grid = self._table.to_grid
        # compare the two
        # check if table grid has changed
        if last_content:
            have_change = len(table_grid) != len(last_content) or len(table_grid[0]) != len(last_content[0])
        else:
            have_change = True
        for i in range(len(table_grid)):                        # every row
            if have_change:
                break
            for j in range(len(table_grid[i])):                 # every cell
                for k in range(len(table_grid[i][j]) - 1):      # every value of that cell, -1 to remove is_new param
                    if table_grid[i][j][k] != last_content[i][j][k]:
                        have_change = True
                        break
        if not have_change:
            msgbox.showerror('אין שינוי!', 'לא קיים שינוי בפקל!')
        else:
            msg_box = msgbox.askyesno('אשר הפצת פקל', 'האם ברצונך להפיץ פקל אקטיבי?')
            if msg_box:
                with open(os.path.join(PAKAL_FOLDER, f'pakal{len(pakals)}.pkl'), 'w', encoding='utf-8-sig') as new_pakal:
                    new_pakal.write(self._table.to_json)
                self._pakal_last_counter = len(pakals) + 1
                self._table.have_changed = False
                self._table.update_cell_new()

    def _get_pakal_cmd(self):
        pakals = os.listdir(PAKAL_FOLDER)
        self._pakal_last_counter = len(pakals)
        if len(pakals) != 0:
            msg_box = msgbox.askyesno('קבלת פקל אקטיבי', 'האם ברצונך למשוך פקל אקטיבי?')
            if msg_box:
                if self.new_file_cmd():
                    current_filename = os.path.join(PAKAL_FOLDER, f'pakal{len(pakals)-1}.pkl')
                    current_content = self._read_pakal_file(current_filename)
                    if current_content:
                        self._table.set_data(current_content)
                        self._table.have_changed = False
                        self._table.set_filter(self.filter, self._btn_relevant_only.get(), self._btn_new_only.get())
        else:
            msgbox.showerror('פקל חסר!', 'לא נמצא פקל למשוך')

    def _check_for_update(self):
        if self._pakal_last_counter != len(os.listdir(PAKAL_FOLDER)):
            self._get_pakal_cmd()
        self._root.after(2000, self._check_for_update)


class AddNetWin(NetMaker):
    def __init__(self, root: tk.Tk, menu: MainMenu):
        super().__init__(root, menu, 'הוסף רשת')
        self._my_window.grid_rowconfigure(0, weight=1)
        self._my_window.grid_columnconfigure(0, weight=1)
        self._my_window.grid_columnconfigure(1, weight=1)

        self._my_window.bind('<Return>', self._submit_cmd)
        self._my_window.bind('<Escape>', self._close_cmd)

        self._data_frame = tk.Frame(self._my_window)
        self._data_frame.grid_rowconfigure(0, weight=1)
        self._data_frame.grid_columnconfigure(0, weight=1)
        self._data_frame.grid_columnconfigure(1, weight=1)
        self._data_frame.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)

        self._values_frame = tk.Frame(self._data_frame, bg=Color.BLACK)
        self._values_frame.grid_columnconfigure(0, weight=1)
        self._values_frame.grid(row=0, column=0, sticky=tk.NSEW)

        self._keys_frame = tk.Frame(self._data_frame, bg=Color.BLACK)
        self._keys_frame.grid_columnconfigure(0, weight=1)
        self._keys_frame.grid(row=0, column=1, sticky=tk.NSEW)

        self._params = gen_net_params(self, self._values_frame, self._keys_frame)

        self._buttons_frame = tk.Frame(self._my_window)
        self._buttons_frame.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        self._buttons_frame.grid_columnconfigure(0, weight=1)
        self._buttons_frame.grid_columnconfigure(1, weight=1)

        self._cancel_btn = Button(self._buttons_frame, 'ביטול', (0, 0), self._close_cmd)
        self._cancel_btn.draw(sticky=tk.EW)
        self._submit_btn = Button(self._buttons_frame, 'הוסף', (0, 1), self._submit_cmd)
        self._submit_btn.draw(sticky=tk.EW)

    def _submit_cmd(self, *_):
        for i in range(20):
            self._master.add_net([param.value for param in self._params.values()])
        # super()._submit_cmd()


class AddSiteWin(SubWin):
    def __init__(self, root: tk.Tk, menu: MainMenu):
        super().__init__(root, menu, 'הוסף אתר')
        self._my_window.grid_rowconfigure(0, weight=1)
        self._my_window.grid_columnconfigure(0, weight=1)
        self._my_window.grid_columnconfigure(1, weight=1)

        self._my_window.bind('<Return>', self._submit_cmd)
        self._my_window.bind('<Escape>', self._close_cmd)

        self._data_frame = tk.Frame(self._my_window)
        self._data_frame.grid_columnconfigure(0, weight=1)
        self._data_frame.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)

        self._params = []
        for i, param in enumerate(SITE_PARAMS):
            self._data_frame.grid_rowconfigure(i, weight=1)
            param_value = InputBox(self._data_frame, param, (i, 0))
            param_value.config(justify=tk.RIGHT)
            param_value.draw(padx=2, pady=2, sticky=tk.NSEW)
            self._params.append(param_value)

        self._buttons_frame = tk.Frame(self._my_window)
        self._buttons_frame.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        self._buttons_frame.grid_columnconfigure(0, weight=1)
        self._buttons_frame.grid_columnconfigure(1, weight=1)

        self._cancel_btn = Button(self._buttons_frame, 'ביטול', (0, 0), self._close_cmd)
        self._cancel_btn.draw(sticky=tk.EW)
        self._submit_btn = Button(self._buttons_frame, 'הוסף', (0, 1), self._submit_cmd)
        self._submit_btn.draw(sticky=tk.EW)

    def _submit_cmd(self, *_):
        for i in range(20):
            self._master.add_site([param.value for param in self._params])
        # super()._submit_cmd()


def ask_for_save(table: PakalTable, main_menu: MainMenu):
    if table.have_changed:
        msg_box = msgbox.askyesnocancel('שמור שינויים', 'האם אתה מעוניין לשמור שינויים?')
        if msg_box in [True, False]:
            if msg_box is True:
                if main_menu.file_name:
                    main_menu.save_file_cmd()
                else:
                    if not main_menu.save_as_file_cmd():
                        return False
        else:
            return False
    return True
