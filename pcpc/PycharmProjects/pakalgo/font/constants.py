import enum
from typing import *


COLOR = str
POSITION = Tuple[int, int]


class BaseEnum(enum.Enum):
    def __get__(self, *args, **kwargs):
        return self.value


class Color(BaseEnum):
    BLACK: COLOR = '#000000'
    RED: COLOR = '#FF0000'
    GREEN: COLOR = '#00FF00'
    BLUE: COLOR = '#0000FF'
    WHITE: COLOR = '#FFFFFF'
    YELLOW: COLOR = '#FFFF00'
    GRAY: COLOR = '#808080'
    ENC_TRUE: COLOR = '#92D050'


SCROLL_LOCK = 32

TEXT_SIZE = 12
TEXT_FONT = 'Heebo'

TITLE_FONT = (TEXT_FONT, TEXT_SIZE, 'bold')
TITLE_BG = '#419CFF'

BODY_FONT = (TEXT_FONT, TEXT_SIZE, 'normal')
BODY_BG = Color.WHITE
WS_RELAY_BG = '#98C2E6'
ERROR_BG = '#FFC7CE'
