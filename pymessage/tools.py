import math
from datetime import datetime

import pytz

DATE_OFFSET = 978307200


def from_apple_time(ts):
    if ts == 0:
        return None

    if unpack_time(ts) != 0:
        ts = unpack_time(ts)

    return datetime.fromtimestamp((ts + DATE_OFFSET), tz=pytz.timezone('Europe/Paris'))


def unpack_time(ts):
    return math.floor(ts / (10 ** 9))
