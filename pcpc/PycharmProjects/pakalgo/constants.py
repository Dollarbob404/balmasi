from font import *


class NetParam(BaseEnum):
    GROUP = 'קבוצה'
    NAME = 'רשת'
    ENCRYPTION = 'הצפנה'
    OK = 'אוק'
    FRQ = 'תדר'


class SiteParam(BaseEnum):
    NAME = 'אתר'


class CellStatus(BaseEnum):
    NORMAL = 0
    WS_RELAY = 1
    ERROR = 2


ENCRYPTION_TRUE = 'מוצפן'
ENCRYPTION_FALSE = 'גלוי'

NET_PARAMS = [NetParam.GROUP, NetParam.NAME, NetParam.ENCRYPTION, NetParam.OK, NetParam.FRQ]
NET_PARAMS_DEFAULT = ['קבוצה', 'רשת', ENCRYPTION_TRUE, 'אוק', '30.000']
NET_PARAMS_PATTERN = [str, str, str, str, lambda s: f'{float(str(s)):.3f}']

NET_GROUP_COL = -1 - NET_PARAMS.index(NetParam.GROUP)
NET_NAME_COL = -1 - NET_PARAMS.index(NetParam.NAME)
NET_ENCRYPTION_COL = -1 - NET_PARAMS.index(NetParam.ENCRYPTION)
NET_OK_COL = -1 - NET_PARAMS.index(NetParam.OK)
NET_FRQ_COL = -1 - NET_PARAMS.index(NetParam.FRQ)

SITE_PARAMS = [SiteParam.NAME]

DEF_SCREEN_TITLE = 'Pakalgo'
FILE_TYPES = (('Pakal Files (*.pkl)', '*.pkl'), ('All Files (*.*)', '*.*'))
EXPORT_TYPES = (('CSV Files (*.csv)', '*.csv'), ('All Files (*.*)', '*.*'))
IMPORT_TYPES = (('CSV Files (*.csv)', '*.csv'), ('All Files (*.*)', '*.*'))


PAKAL_FOLDER = r"pakals"
