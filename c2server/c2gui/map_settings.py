from decimal import Decimal

MIN_LAT = Decimal(53.929472)
MIN_LON = Decimal(1.004663)
MAX_LAT = Decimal(54.007111)
MAX_LON = Decimal(1.165084)
REG_NUM_X = 10    # number of tiles in x axis
REG_NUM_Y = 8     # number of tiles in y axis
REG_WIDTH = (MAX_LON - MIN_LON) / REG_NUM_X
REG_HEIGHT = (MAX_LAT - MIN_LAT) / REG_NUM_Y
