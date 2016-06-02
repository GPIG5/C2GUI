from decimal import Decimal

MIN_LAT = Decimal(53.929472)
MAX_LON = Decimal(-1.004663)
MAX_LAT = Decimal(54.007111)
MIN_LON = Decimal(-1.165084)
REG_NUM_X = 40    # number of tiles in x axis
REG_NUM_Y = 32     # number of tiles in y axis
REG_WIDTH = (MAX_LON - MIN_LON) / REG_NUM_X
REG_HEIGHT = (MAX_LAT - MIN_LAT) / REG_NUM_Y

C2_LOCATIONS = [{"lat": 53.957285, "lon": -1.0906344}, {"lat": 53.959457, "lon": -1.1170224}, {"lat": 53.955843, "lon": -1.0800438}]
