from .constants import *
import tkinter as tk


class TextObj:
    def __init__(self, master: tk.Misc, text: str, pos, color=None, bg_color=None,
                 size=TEXT_SIZE):
        self._text = text
        self._color = color
        self._pos = pos
        self._bg_color = bg_color
        self._bg_color_changed = False
        self._font = (TEXT_FONT, size)
        self._widget = tk.Entry(master, fg=color, readonlybackground=bg_color, font=self._font, bd=0)
        self._widget.insert(0, text)
        self._widget.config(state='readonly')
        self._is_dead = False

    def draw(self, **kwargs):
        row, column = self._pos
        self._widget.grid(row=row, column=column, **kwargs)

    def pack(self, *args, **kwargs):
        self._widget.pack(*args, **kwargs)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    @property
    def bg_color(self):
        return self._bg_color

    @bg_color.setter
    def bg_color(self, bg_color):
        self._bg_color_changed = self._bg_color != bg_color or self._bg_color_changed
        self._bg_color = bg_color

    @property
    def bg_color_changed(self):
        res = self._bg_color_changed
        self._bg_color_changed = False
        return res

    @property
    def widget(self):
        return self._widget

    def change_background(self):
        self._widget.config(readonlybackground=self._bg_color)

    def destroy(self):
        self._widget.destroy()

    def bind(self, event, handler):
        self._widget.bind(event, handler)

    def config(self, **kwargs):
        self._widget.config(**kwargs)


class Button(TextObj):
    def __init__(self, master: tk.Misc, text: str, pos, func, color=None, bg_color=None,
                 size=TEXT_SIZE):
        super(Button, self).__init__(master, text, pos, color, bg_color, size)
        self._func = func
        self._widget = tk.Button(master, text=text, fg=color, bg=bg_color, command=func, font=self._font)


class InputBox(TextObj):
    def __init__(self, master: tk.Misc, text: str, pos, color=Color.BLACK, bg_color=None,
                 size=TEXT_SIZE, **kwargs):
        super(InputBox, self).__init__(master, text, pos, color, bg_color, size)
        self._widget = tk.Entry(master, fg=Color.GRAY, bg=bg_color, font=self._font, **kwargs)
        self._widget.insert(0, text)
        self._changed = False
        self._widget.bind('<FocusIn>', self._got_focus)

    def _got_focus(self, *_):
        if not self._changed:
            self._changed = True
            self._widget.delete(0, tk.END)
            self._widget.config(foreground=self._color)

    def reset_text(self):
        self._widget.delete(0, tk.END)
        self._widget.insert(0, self._text)
        self._widget.config(foreground=Color.GRAY)
        self._changed = False

    @property
    def value(self):
        return self._widget.get()

    @value.setter
    def value(self, value):
        self._got_focus()
        self._widget.insert(0, value)

    @property
    def changed(self):
        return self._changed

    def config(self, **kwargs):
        self._widget.config(**kwargs)


class FloatInputBox(TextObj):
    def __init__(self, master: tk.Misc, text: str, pos, from_, to, jump_by=1, color=Color.BLACK,
                 bg_color=None, size=TEXT_SIZE, on_change: Optional[Callable] = None):
        super(FloatInputBox, self).__init__(master, text, pos, color, bg_color, size)
        self._from = from_
        self._to = to
        validate_cmd = (master.register(self.validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self._widget = tk.Spinbox(master, from_=from_, to=to, increment=jump_by, fg=color, font=self._font, bd=0,
                                  bg=bg_color, validate='key', validatecommand=validate_cmd, wrap=True,
                                  command=on_change)
        self.set_text(text)

    def validate(self, action, index, value_if_allowed: str, prior_value, text, validation_type, trigger_type,
                 widget_name):
        if value_if_allowed:
            try:
                float(value_if_allowed)
            except ValueError:
                return False
        return True

    @property
    def value(self):
        v = self._widget.get()
        if v:
            return max(min(float(v), self._to), self._from)
        return None

    def set_text(self, text: str):
        self._widget.delete(0, tk.END)
        self._widget.insert(0, text)


class IntInputBox(FloatInputBox):
    def __init__(self, master: tk.Misc, text: str, pos, from_, to, jump_by=1, color=Color.BLACK,
                 bg_color=None, size=TEXT_SIZE, on_change=None):
        super(IntInputBox, self).__init__(master, text, pos, from_, to, jump_by, color, bg_color, size, on_change)

    def validate(self, action, index, value_if_allowed: str, prior_value, text, validation_type, trigger_type,
                 widget_name):
        if value_if_allowed:
            try:
                int(value_if_allowed)
            except ValueError:
                return False
        return True

    @property
    def value(self):
        v = self._widget.get()
        if v:
            return max(min(int(v), self._to), self._from)
        return None


class BoolInputBox(IntInputBox):
    def __init__(self, master: tk.Misc, text: str, pos, color=Color.BLACK, bg_color=None, size=TEXT_SIZE,
                 on_change=None):
        super(IntInputBox, self).__init__(master, text, pos, None, None, 1, color, bg_color, size, on_change)
        self._values = ['True', 'False']
        self._widget.config(values=self._values)
        self.set_text(text)

    def validate(self, action, index, value_if_allowed: str, prior_value, text, validation_type, trigger_type,
                 widget_name):
        if value_if_allowed:
            if value_if_allowed not in ['True', 'False']:
                return False
        return True

    @property
    def value(self):
        v = self._widget.get()
        if v:
            return 1 if v == 'True' else 0
        return None


class FrqInputBox(FloatInputBox):
    def __init__(self, master: tk.Misc, text: str, pos, from_, to, jump_by=1, color=Color.BLACK, bg_color=None,
                 size=TEXT_SIZE):
        super(FrqInputBox, self).__init__(master, text, pos, from_, to, jump_by, color, bg_color, size,
                                          self._set_3_digit)

    def set_text(self, text: str):
        self._widget.delete(0, tk.END)
        self._widget.insert(0, text)
        self._set_3_digit()

    def _set_3_digit(self):
        super().set_text(f'{self.value:.3f}')
