import hakash
from table import *
from subwin import *
import json
from tkinter import messagebox as msgbox


class PakalCell(Cell):
    def __init__(self, table, frame, pos, text='', as_title=False, readonly=False, status=CellStatus.NORMAL,
                 is_new=False, newly_created=False):
        super().__init__(table, frame, pos, text, as_title, readonly)
        self._entry.bind('<KeyPress>', self._reset_color)
        self._entry.bind('<Button-3>', self._popup_menu)
        self._status = status
        self._refresh_status_color()
        self._color = None
        self._start_values = [text, as_title, readonly, status]
        if newly_created:
            self._start_values = [None] * len(self._start_values)
        self._start_new = is_new
        self.set_new(is_new)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        self._entry.config(fg=self._color)

    @property
    def is_new(self):
        current_values = [self._text.get(), self._as_title, self._readonly, self._status]
        for i in range(len(current_values)):
            if current_values[i] != self._start_values[i]:
                return True
        return False

    @property
    def is_start_new(self):
        return self._start_new

    @property
    def to_json(self):
        return self._text.get(), self._as_title, self._readonly, self._status, self.is_new

    def set_new(self, is_new=True):
        self.color = Color.RED if is_new else Color.BLACK

    def _reset_color(self, _=None):
        self.color = Color.BLACK
    
    def _refresh_status_color(self):
        if self._status == CellStatus.NORMAL:
            self._bg_color = TITLE_BG if self._as_title else BODY_BG
        elif self._status == CellStatus.WS_RELAY:
            self._bg_color = WS_RELAY_BG
        elif self._status == CellStatus.ERROR:
            self._bg_color = ERROR_BG
        self._entry.config(bg=self._bg_color, readonlybackground=self._bg_color)
        self._check_content()

    def _popup_menu(self, event):
        self._table.popup_menu(event, self._pos)

    def set_bg_color(self, bg_color):
        self._bg_color = bg_color
        self._entry.config(bg=self._bg_color, readonlybackground=self._bg_color)

    def _check_content(self, _=None):
        if not super()._check_content():
            self._is_not_working = False
            self._is_ws_relay = False

    def set_ws_relay(self):
        if self._text.get():
            new_status = CellStatus.NORMAL if self._status == CellStatus.WS_RELAY else CellStatus.WS_RELAY
            self._bg_color = WS_RELAY_BG if new_status == CellStatus.WS_RELAY else BODY_BG
            self._entry.config(bg=self._bg_color, readonlybackground=self._bg_color)
            self._status = new_status
        else:
            msgbox.showerror('סימון ריק!', 'לא ניתן לסמן תא ריק')

    def set_work_not(self):
        if self._text.get():
            new_status = CellStatus.NORMAL if self._status == CellStatus.ERROR else CellStatus.ERROR
            self._bg_color = ERROR_BG if new_status == CellStatus.ERROR else BODY_BG
            self._entry.config(bg=self._bg_color, readonlybackground=self._bg_color)
            self._status = new_status
        else:
            msgbox.showerror('סימון ריק!', 'לא ניתן לסמן תא ריק')

    def reset_is_new(self):
        self._start_values = [self._text.get(), self._as_title, self._readonly, self._status]


class PakalTable(Table, SubMaster):
    def __init__(self, root, master, pos):
        Table.__init__(self, root, master, pos)
        SubMaster.__init__(self)
        self._menu = tk.Menu(self._table_frame, tearoff=False)
        self._remove_menu = tk.Menu(self._menu, tearoff=False)
        self._edit_menu = tk.Menu(self._menu, tearoff=False)
        self._mark_menu = tk.Menu(self._menu, tearoff=False)

        self._main_menu_pointer = None

        self._remove_menu.add_command(label='רשת', command=self._remove_net_cmd)
        self._remove_menu.add_command(label='אתר', command=self._remove_site_cmd)
        self._menu.add_cascade(label='הסר', menu=self._remove_menu)

        self._edit_menu.add_command(label='רשת', command=self._edit_net_cmd)
        self._edit_menu.add_command(label='אתר', command=self._edit_site_cmd)
        self._menu.add_cascade(label='ערוך', menu=self._edit_menu)

        self._mark_menu.add_command(label='ממסור ללבן', command=self._ws_relay_cmd)
        self._mark_menu.add_command(label='תקין/תקול', command=self._work_not_cmd)
        self._menu.add_cascade(label='סמן', menu=self._mark_menu)

        self._menu_cell = (0, 0)
        self.create_base()

    def set_menu(self, menu):
        self._main_menu_pointer = menu
        self._main_menu_pointer.set_groups()

    @property
    def have_changed(self):
        for row in self._entries:
            for cell in row:
                if cell.have_changed:
                    return True
        return self._have_changed

    @have_changed.setter
    def have_changed(self, value):
        if not value:
            for row in self._entries:
                for cell in row:
                    cell.have_changed = value
        if self._main_menu_pointer:
            self._main_menu_pointer.set_groups()
        self.recolor()
        self._have_changed = value
        self._master.after(100, self.configure_canvas)

    @property
    def groups(self):
        return {str(row[NET_GROUP_COL]) for row in self._entries[1:]}

    def recolor(self):
        # recolor encryption column
        for i, row in enumerate(self._entries):
            if i == 0:
                continue
            for j, cell in enumerate(row):
                if j == len(row)+NET_ENCRYPTION_COL:
                    cell.set_bg_color(Color.ENC_TRUE if str(cell) == ENCRYPTION_TRUE else Color.RED)

    @property
    def to_grid(self):
        byte_grid = []
        for row in self._entries:
            byte_row = []
            for cell in row:
                byte_row.append(cell.to_json)
            byte_grid.append(byte_row)
        return byte_grid

    @property
    def to_json(self):
        return json.dumps(self.to_grid)

    @property
    def to_text(self):
        table_data = []
        for row in self._entries:
            table_row = []
            for cell in row:
                table_row.append(str(cell))
            table_data.append(table_row)
        return table_data

    def create_base(self):
        titles = NET_PARAMS[::-1]
        titles_row = []
        for i, title in enumerate(titles):
            new_cell = PakalCell(self, self._base_frame, (0, i), title, as_title=True, readonly=True)
            titles_row.append(new_cell)
            new_cell.draw()
        self._entries.append(titles_row)

    def add_net(self, region, name, encryption, ok, freq):
        values = [region, name, ENCRYPTION_TRUE if encryption else ENCRYPTION_FALSE, ok, f'{freq:.3f}'][::-1]
        title_row = []
        for i in range(len(self._entries[-1]) - len(values)):
            new_cell = PakalCell(self, self._body_frame, (len(self._entries), i), newly_created=True)
            title_row.append(new_cell)
            new_cell.draw()
        for i, value in enumerate(values):
            new_cell = PakalCell(self, self._row_frame, (len(self._entries), len(title_row)), value,
                                 as_title=False, readonly=True, newly_created=True)
            title_row.append(new_cell)
            new_cell.draw()
        self._entries.append(title_row)
        self.have_changed = True

    def add_site(self, values):
        values = values[::-1]
        for value in values:
            for i, row in enumerate(self._entries):
                for cell in row:
                    cell.shift_right()
                if i == 0:
                    new_cell = PakalCell(self, self._col_frame, (i, 0), value, as_title=True, readonly=True,
                                         newly_created=True)
                else:
                    new_cell = PakalCell(self, self._body_frame, (i, 0), '', newly_created=True)
                row.insert(0, new_cell)
                new_cell.draw()
        self.have_changed = True

    def remove_all(self):
        for row in self._entries:
            for cell in row:
                cell.remove()
                cell.destroy()
        self._entries: List[List[PakalCell]] = []
        self.have_changed = True

    def reset(self):
        self.remove_all()
        self.create_base()
        self.have_changed = True

    def set_data(self, content):
        print(f'loading {len(content)} rows on {len(content[0])} columns, total of {len(content) * len(content[0])}')
        self.remove_all()
        for i, row in enumerate(content):
            row_entries = []
            for j, cell in enumerate(row):
                if i == 0:
                    if len(row)-len(NET_PARAMS)-1 < j:
                        new_cell = PakalCell(self, self._base_frame, (i, j), *cell)
                    else:
                        new_cell = PakalCell(self, self._col_frame, (i, j), *cell)
                else:
                    if len(row)-len(NET_PARAMS)-1 < j:
                        new_cell = PakalCell(self, self._row_frame, (i, j), *cell)
                    else:
                        new_cell = PakalCell(self, self._body_frame, (i, j), *cell)
                row_entries.append(new_cell)
                new_cell.draw()
            self._entries.append(row_entries)
        # adjust net_params by pattern (especially for importing files)
        for i, row in enumerate(self._entries):
            if i == 0:
                continue
            net_params = [row[-1-j] for j in range(len(NET_PARAMS))]
            adjust_net_params = []
            for j in range(len(net_params)):
                adjust_net_params.append(NET_PARAMS_PATTERN[j](net_params[j]))
            for j in range(len(net_params)):
                net_params[j].set_value(adjust_net_params[j])

    def _remove_net_cmd(self):
        msg_box = msgbox.askyesno('אשר מחיקה', 'האם אתה בטוח שברצונך למחוק את הרשת?')
        if msg_box:
            row, column = self._menu_cell
            for i, r in enumerate(self._entries):
                if i > row:
                    for cell in r:
                        cell.shift_up()
            cells = self._entries.pop(row)
            for cell in cells:
                cell.remove()
            self.have_changed = True

    def _remove_site_cmd(self):
        msg_box = msgbox.askyesno('אשר מחיקה', 'האם אתה בטוח שברצונך למחוק את האתר?')
        if msg_box:
            row, column = self._menu_cell
            for i, r in enumerate(self._entries):
                for j, cell in enumerate(r):
                    if j > column:
                        cell.shift_left()
                cell = r.pop(column)
                cell.remove()
            self.have_changed = True

    def _edit_net_cmd(self):
        if not self._sub_win:
            row, column = self._menu_cell
            start_value = [str(cell) for cell in self._entries[row][-len(NET_PARAMS):][::-1]]
            self.create_win(EditNetWin(self, self._root, row, start_value))

    def edit_net(self, row, values):
        region, name, encryption, ok, freq = values
        values = [region, name, ENCRYPTION_TRUE if encryption else ENCRYPTION_FALSE, ok, f'{freq:.3f}'][::-1]
        for i, cell in enumerate(self._entries[row][-len(NET_PARAMS):]):
            cell.set_value(values[i])
        self.have_changed = True

    def _edit_site_cmd(self):
        if not self._sub_win:
            row, column = self._menu_cell
            start_values = [str(self._entries[0][column])]
            self.create_win(EditSiteWin(self, self._root, column, start_values))

    def edit_site(self, column, values):
        name = values[0]
        self._entries[0][column].set_value(name)
        self.have_changed = True

    def _ws_relay_cmd(self):
        row, column = self._menu_cell
        self._entries[row][column].set_ws_relay()

    def _work_not_cmd(self):
        row, column = self._menu_cell
        self._entries[row][column].set_work_not()

    def popup_menu(self, event, pos):
        self._menu_cell = row, column = pos

        disable_col = column >= len(self._entries[0]) - len(NET_PARAMS)
        disable_row = row == 0

        self._remove_menu.entryconfig('רשת', state=tk.DISABLED if disable_row else tk.NORMAL)
        self._edit_menu.entryconfig('רשת', state=tk.DISABLED if disable_row else tk.NORMAL)

        self._remove_menu.entryconfig('אתר', state=tk.DISABLED if disable_col else tk.NORMAL)
        self._edit_menu.entryconfig('אתר', state=tk.DISABLED if disable_col else tk.NORMAL)
        self._menu.tk_popup(event.x_root, event.y_root)

    def set_filter(self, menu_filter, relevant_only, new_only):
        # show all
        for row in self._entries:
            for cell in row:
                cell.draw()
        # filter rows
        for i, row in enumerate(self._entries):
            if i == 0:
                continue
            for key in menu_filter:
                if not menu_filter[key] and str(row[-1]) == key:
                    for item in row:
                        item.remove()
        if new_only:
            self.filter_new_only()
        if relevant_only:
            self.filter_columns()
        self._root.after(100, self.configure_canvas)

    def filter_new_only(self):
        rows_to_filter = [True]*len(self._entries)
        for i, row in enumerate(self._entries):
            if i == 0:
                continue
            for j, cell in enumerate(row):
                if j == 0 or not cell.is_draw:
                    continue
                rows_to_filter[i] = rows_to_filter[i] and not cell.is_start_new
        for i, row in enumerate(self._entries):
            if i == 0:
                continue
            if rows_to_filter[i]:
                for cell in row:
                    cell.remove()

    def filter_columns(self):
        # filter columns by rows
        cols_to_filter = [False]*len(self._entries[0])
        for i, row in enumerate(self._entries):
            if i == 0:
                continue
            for j, cell in enumerate(row):
                if j == 0 or not cell.is_draw:
                    continue
                cols_to_filter[j] = cols_to_filter[j] or str(cell) != ''
        for i, row in enumerate(self._entries):
            for j, cell in enumerate(row):
                if not cols_to_filter[j]:
                    cell.remove()

    def update_cell_new(self):
        for row in self._entries:
            for cell in row:
                if cell.is_new:
                    cell.set_new(True)
                    cell.reset_is_new()
                else:
                    cell.set_new(False)


class NetMaker(SubWin):
    def __init__(self, root: tk.Tk, master, title=None):
        super().__init__(root, master, title)
        self._params = {}

    def ok_focus_out(self, _):
        try:
            frq = hakash.hakash[self._params[NetParam.OK].value]
            self._params[NetParam.FRQ].set_text(frq)
        except KeyError:
            msgbox.showwarning('אוק לא קיים!', 'האוק שהוכנס אינו קיים בהקש!')


class EditNetWin(NetMaker):
    def __init__(self, master, root, row_index, start_params):
        super().__init__(root, master, 'ערוך רשת')
        self._row_index = row_index

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

        self._params = gen_net_params(self, self._values_frame, self._keys_frame, start_params)

        self._buttons_frame = tk.Frame(self._my_window)
        self._buttons_frame.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        self._buttons_frame.grid_columnconfigure(0, weight=1)
        self._buttons_frame.grid_columnconfigure(1, weight=1)

        self._cancel_btn = Button(self._buttons_frame, 'ביטול', (0, 0), self._close_cmd)
        self._cancel_btn.draw(sticky=tk.EW)
        self._submit_btn = Button(self._buttons_frame, 'ערוך', (0, 1), self._submit_cmd)
        self._submit_btn.draw(sticky=tk.EW)

    def _submit_cmd(self, *_):
        self._master.edit_net(self._row_index, [param.value for param in self._params.values()])
        super()._submit_cmd()


class EditSiteWin(SubWin):
    def __init__(self, master, root, column_index, start_value):
        super().__init__(root, master, 'ערוך אתר')
        self._column_index = column_index

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
            param_value = InputBox(self._data_frame, start_value[i], (i, 0))
            param_value.config(justify=tk.RIGHT)
            param_value.draw(padx=2, pady=2, sticky=tk.NSEW)
            self._params.append(param_value)

        self._buttons_frame = tk.Frame(self._my_window)
        self._buttons_frame.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        self._buttons_frame.grid_columnconfigure(0, weight=1)
        self._buttons_frame.grid_columnconfigure(1, weight=1)

        self._cancel_btn = Button(self._buttons_frame, 'ביטול', (0, 0), self._close_cmd)
        self._cancel_btn.draw(sticky=tk.EW)
        self._submit_btn = Button(self._buttons_frame, 'ערוך', (0, 1), self._submit_cmd)
        self._submit_btn.draw(sticky=tk.EW)

    def _submit_cmd(self, *_):
        self._master.edit_site(self._column_index, [param.value for param in self._params])
        super()._submit_cmd()


def gen_net_params(sub_win, values_frame, keys_frame, start_params=NET_PARAMS_DEFAULT):
    params = {}
    for i, param in enumerate(NET_PARAMS):
        values_frame.grid_rowconfigure(i, weight=1)
        keys_frame.grid_rowconfigure(i, weight=1)
        if param in [NetParam.ENCRYPTION]:
            param_value = BoolInputBox(values_frame, str(start_params[i] == ENCRYPTION_TRUE),
                                       (i, 0))
        elif param in [NetParam.FRQ]:
            param_value = FrqInputBox(values_frame, start_params[i], (i, 0), 30, 87.975)
        elif param in [NetParam.OK]:
            param_value = InputBox(values_frame, start_params[i], (i, 0))
            param_value.bind('<FocusOut>', sub_win.ok_focus_out)
        else:
            param_value = InputBox(values_frame, start_params[i], (i, 0))
        param_title = TextObj(keys_frame, param, (i, 0))
        param_title.config(justify=tk.RIGHT)
        param_title.draw(padx=2, pady=2, sticky=tk.NSEW)

        param_value.config(justify=tk.RIGHT)
        param_value.draw(padx=2, pady=2, sticky=tk.NSEW)
        params[param] = param_value
    return params
