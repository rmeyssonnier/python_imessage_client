from pymessage.client import Client
from pymessage.contact import Contact
from pymessage.tools import normalize_contact


class ContactClient(Client):
    def __init__(self, path):
        super().__init__(path)

    def get_all(self) -> [Contact]:
        res = []
        for row in self.cur.execute(
                'select c.ZFIRSTNAME, c.ZLASTNAME, a.ZFULLNUMBER '
                'from ZABCDPHONENUMBER as a inner join ZABCDRECORD c on a.ZOWNER = c.Z_PK'):
            res.append(normalize_contact(row))
        return res

    def get_by_number(self, number):
        number = number.replace(' ', '').replace('+33', '')
        r = self.cur.execute(
            f'select c.ZFIRSTNAME, c.ZLASTNAME, a.ZFULLNUMBER \
            from ZABCDPHONENUMBER as a inner join ZABCDRECORD c on a.ZOWNER = c.Z_PK \
            where a.ZFULLNUMBER like "%{number}%"').fetchone()
        if r is None:
            return None

        return normalize_contact(r)
