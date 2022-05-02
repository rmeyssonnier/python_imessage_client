import math
import os
from datetime import datetime
from pathlib import Path

import pytz

from pymessage.contact import Contact

DATE_OFFSET = 978307200


def from_apple_time(ts):
    if ts == 0:
        return None

    if unpack_time(ts) != 0:
        ts = unpack_time(ts)

    return datetime.fromtimestamp((ts + DATE_OFFSET), tz=pytz.timezone('Europe/Paris'))


def unpack_time(ts):
    return math.floor(ts / (10 ** 9))


def normalize_contact(r):
    contact = Contact()
    if r[0] is not None:
        contact.name = r[0]

    if r[1] is not None:
        contact.name += ' ' + r[1]
    contact.phone_number = r[2].replace(' ', '')
    return contact


def get_contact_db(base_dir):
    # Get list of files in a directory
    list_of_files = list(Path(base_dir).rglob("AddressBook-v22.abcddb"))

    # Find the file with max size from the list of files
    return max(list_of_files, key=lambda x: os.stat(x).st_size)
