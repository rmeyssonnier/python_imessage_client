import sqlite3


class Client:
    def __init__(self, path):
        self.cur = None
        self.db = None
        self.path = path

    def connect(self):
        self.db = sqlite3.connect(self.path, uri=True)
        self.cur = self.db.cursor()

    def close(self):
        if self.db:
            self.cur.close()
