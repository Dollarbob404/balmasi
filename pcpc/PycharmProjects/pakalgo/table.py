from constants import *
from tkinter import font as tkfont


MIN_CELL_WIDTH = 10


class Cell:
    def __init__(self, table, frame, pos, text='', as_title=False, readonly=False):
        row, column = pos
        self._pos = pos
        self._table = table
        self._frame = frame
        self._text = tk.StringVar()
        self._text.set(text)
        self._start_text = text
        self._is_draw = False
        self._as_title = as_title
        self._readonly = readonly
        self._bg_color = TITLE_BG if as_title else BODY_BG
        state = 'readonly' if readonly else tk.NORMAL
        justify = tk.CENTER if as_title else tk.RIGHT
        family, size, weight = TITLE_FONT if as_title else BODY_FONT
        self._font = tkfont.Font(family=family, size=size, weight=weight)
        self._entry = tk.Entry(self._frame, width=MIN_CELL_WIDTH, borderwidth=1, textvariable=self._text,
                               bg=self._bg_color, font=self._font, state=state, readonlybackground=self._bg_color,
                               justify=justify)
        self._entry.grid(row=row, column=column, sticky=tk.NSEW)
        self._entry.bind('<FocusIn>', self._focus_in)
        self._entry.bind('<FocusOut>', self._check_content)
        self._entry.bind('<KeyRelease>', self._update_width)
        self._avg_char_width = self._font.measure('a')
        self._current_width = 0
        self._check_content()
        self._update_width()

    @property
    def to_json(self):
        return self._text.get(), self._as_title, self._readonly

    @property
    def width(self):
        return self._current_width

    @property
    def pixle_width(self):
        return self._entry.winfo_width()

    @property
    def pixle_height(self):
        return self._entry.winfo_height()

    @width.setter
    def width(self, width):
        self._entry.config(width=width)
        self._current_width = width

    @property
    def pixle_pos(self):
        return self._entry.winfo_x(), self._entry.winfo_y()

    @property
    def frame(self):
        return self._frame

    def focus_set(self):
        self._entry.focus_set()

    def _check_content(self, _=None):
        if self._text.get():
            self._entry.config(bg=self._bg_color, readonlybackground=self._bg_color)
            return True
        self._bg_color = TITLE_BG if self._as_title else BODY_BG
        self._entry.config(bg=Color.BLACK, readonlybackground=Color.BLACK)
        return False

    def _focus_in(self, _=None):
        self._table.update_current_cell(self._pos)
        self._entry.config(bg=self._bg_color, readonlybackground=self._bg_color)

    def _update_width(self, _=None):
        if self._as_title:
            return
        text = str(self)
        text_width = self._font.measure(text)
        new_width = max(MIN_CELL_WIDTH, text_width // self._avg_char_width + 2)
        self._entry.config(width=new_width)
        self._current_width = new_width
        self._table.update_width(self._pos)

    def shift_right(self):
        self.remove()
        row, column = self._pos
        self._pos = (row, column + 1)
        self.draw()

    def shift_left(self):
        self.remove()
        row, column = self._pos
        self._pos = (row, column - 1)
        self.draw()

    def shift_up(self):
        self.remove()
        row, column = self._pos
        self._pos = (row - 1, column)
        self.draw()

    def draw(self):
        row, column = self._pos
        self._entry.grid(row=row, column=column, sticky=tk.NSEW)
        self._is_draw = True

    def remove(self):
        self._entry.grid_remove()
        self._is_draw = False

    def destroy(self):
        self._entry.destroy()

    def __str__(self):
        return self._text.get()

    def set_value(self, value):
        self._text.set(value)
        self._update_width()

    @property
    def have_changed(self):
        return str(self) != self._start_text

    @have_changed.setter
    def have_changed(self, value):
        if value:
            self._start_text = ''
        else:
            self._start_text = str(self)

    @property
    def is_draw(self):
        return self._is_draw


class Table:
    def __init__(self, root: tk.Tk, master: tk.Misc, pos):
        self._have_changed = False
        self._root = root

        row, column = pos
        self._master = master
        self._master.grid_rowconfigure(row, weight=1)
        self._master.grid_columnconfigure(column, weight=1)

        self._frame = tk.Frame(self._master)
        self._frame.grid(row=row, column=column, sticky=tk.NSEW)

        self._scrollbar_x = tk.Scrollbar(self._frame, orient=tk.HORIZONTAL, command=self._x_scrollbar_cmd)
        self._scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        self._scrollbar_y = tk.Scrollbar(self._frame, orient=tk.VERTICAL, command=self._y_scrollbar_cmd)
        self._scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        self._table_frame = tk.Frame(self._frame)
        self._table_frame.grid_rowconfigure(1, weight=1)
        self._table_frame.grid_columnconfigure(0, weight=1)
        self._table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._col_header_canvas = tk.Canvas(self._table_frame, height=20)
        self._col_header_canvas.grid(row=0, column=0, sticky=tk.EW)

        self._base_header_canvas = tk.Canvas(self._table_frame)
        self._base_header_canvas.grid(row=0, column=1, sticky=tk.EW)

        self._row_header_canvas = tk.Canvas(self._table_frame)
        self._row_header_canvas.grid(row=1, column=1, sticky=tk.NS)

        self._body_canvas = tk.Canvas(self._table_frame)
        self._body_canvas.grid(row=1, column=0, sticky=tk.NSEW)
        self._body_canvas.configure(xscrollcommand=self._scrollbar_x.set, yscrollcommand=self._scrollbar_y.set)

        self._col_frame = tk.Frame(self._col_header_canvas)
        self._col_header_canvas.create_window((0, 0), window=self._col_frame, anchor=tk.NW)

        self._base_frame = tk.Frame(self._base_header_canvas)
        self._base_header_canvas.create_window((0, 0), window=self._base_frame, anchor=tk.NW)

        self._row_frame = tk.Frame(self._row_header_canvas)
        self._row_header_canvas.create_window((0, 0), window=self._row_frame, anchor=tk.NW)

        self._body_frame = tk.Frame(self._body_canvas)
        self._body_canvas.create_window((0, 0), window=self._body_frame, anchor=tk.NW)

        self._col_header_canvas.update_idletasks()
        self._row_header_canvas.update_idletasks()
        self._body_canvas.update_idletasks()

        self.configure_canvas()
        self._entries: List[List[Cell]] = []
        self._current_cell = (0, 0)

        self._body_canvas.bind('<Configure>', self.configure_canvas)
        self._root.bind('<Right>', self.arrow_right)
        self._root.bind('<Left>', self.arrow_left)
        self._root.bind('<Down>', self.arrow_down)
        self._root.bind('<Up>', self.arrow_up)

    @property
    def have_changed(self):
        return self._have_changed

    @have_changed.setter
    def have_changed(self, value):
        self._have_changed = value
        self._master.after(100, self.configure_canvas)

    def _x_scrollbar_cmd(self, *args):
        self._col_header_canvas.xview(*args)
        self._body_canvas.xview(*args)
        self.configure_canvas()

    def _y_scrollbar_cmd(self, *args):
        self._row_header_canvas.yview(*args)
        self._body_canvas.yview(*args)
        self.configure_canvas()

    def configure_canvas(self, *_):
        self._col_header_canvas.configure(scrollregion=self._col_header_canvas.bbox('all'))
        self._base_header_canvas.configure(scrollregion=self._base_header_canvas.bbox('all'))
        self._row_header_canvas.configure(scrollregion=self._row_header_canvas.bbox('all'))
        self._body_canvas.configure(scrollregion=self._body_canvas.bbox('all'))
        self._update_canvases_size()

    def arrow_right(self, event):
        if event.state & SCROLL_LOCK:
            self._body_canvas.xview_scroll(1, 'units')
        else:
            next_cell = (self._current_cell[0], min(self._current_cell[1] + 1, len(self._entries[0]) - 1))
            self.set_focus(next_cell)

    def arrow_left(self, event):
        if event.state & SCROLL_LOCK:
            self._body_canvas.xview_scroll(-1, 'units')
        else:
            next_cell = (self._current_cell[0], max(self._current_cell[1] - 1, 0))
            self.set_focus(next_cell)

    def arrow_down(self, event):
        if event.state & SCROLL_LOCK:
            self._body_canvas.yview_scroll(1, 'units')
        else:
            next_cell = (min(self._current_cell[0] + 1, len(self._entries) - 1), self._current_cell[1])
            self.set_focus(next_cell)

    def arrow_up(self, event):
        if event.state & SCROLL_LOCK:
            self._body_canvas.yview_scroll(-1, 'units')
        else:
            next_cell = (max(self._current_cell[0] - 1, 0), self._current_cell[1])
            self.set_focus(next_cell)

    def update_current_cell(self, cell):
        self._current_cell = cell

    def update_width(self, cell_pos):
        _, c = cell_pos
        max_width = MIN_CELL_WIDTH
        for i, row in enumerate(self._entries):
            if i == 0:
                continue
            max_width = max(row[c].width, max_width)
        if self._entries[0][c].width != max_width:
            self._entries[0][c].width = max_width
            self._frame.after(100, self._update_canvases_size)

    def _update_canvases_size(self):
        x, y, w, h = self._base_header_canvas.bbox('all')
        self._base_header_canvas.config(width=w, height=h)
        x, y, w, h = self._row_header_canvas.bbox('all')
        self._row_header_canvas.config(width=w)
        x, y, w, h = self._col_header_canvas.bbox('all')
        self._col_header_canvas.config(height=h)

    def set_focus(self, cell):
        row, column = cell
        current_cell = self._entries[row][column]
        current_cell.focus_set()
        self.update_current_cell(cell)
        if current_cell.frame == self._body_frame:
            x1, y1 = current_cell.pixle_pos
            cell_width, cell_height = current_cell.pixle_width, current_cell.pixle_height
            canvas_width, canvas_height = self._body_frame.winfo_width(), self._body_frame.winfo_height()

            canvas_x1 = self._body_canvas.canvasx(0)
            canvas_y1 = self._body_canvas.canvasy(0)
            canvas_x2 = self._body_canvas.canvasx(self._body_canvas.winfo_width())
            canvas_y2 = self._body_canvas.canvasy(self._body_canvas.winfo_height())

            a_x1, a_y1, a_x2, a_y2 = (x1, y1, cell_width+x1, cell_height+y1)
            b_x1, b_y1, b_x2, b_y2 = (canvas_x1, canvas_y1, canvas_x2, canvas_y2)
            if b_x1 > a_x1:                             # if cell is at the left
                d_x = a_x1 / canvas_width
            elif a_x2 > b_x2:                           # ----------------- right
                d_x = (a_x2 - (b_x2-b_x1)) / canvas_width
            else:
                d_x = None
            if b_y1 > a_y1:                             # ----------------- top
                d_y = a_y1 / canvas_height
            elif a_y2 > b_y2:                           # ----------------- bottom
                d_y = (a_y2 - (b_y2 - b_y1)) / canvas_height
            else:
                d_y = None
            if d_x is not None:
                self._body_canvas.xview_moveto(d_x)
                self._col_header_canvas.xview_moveto(d_x)
            if d_y is not None:
                self._body_canvas.yview_moveto(d_y)
                self._row_header_canvas.yview_moveto(d_y)
