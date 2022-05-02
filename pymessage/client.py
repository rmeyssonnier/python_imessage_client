import math
import sqlite3
from datetime import datetime

import pytz as pytz

from pymessage.chat import Chat
from pymessage.message import Message
from pymessage.tools import from_apple_time


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

    def get_last_messages(self, count=10) -> [Message]:
        res = []
        for row in self.cur.execute(
                'select guid, text, service, date, date_read, destination_caller_id from message order by ROWID desc limit {}'.format(
                    count)):
            message = Message()
            message.guid = row[0]
            message.text = row[1]
            message.service = row[2]
            message.date = from_apple_time(int(row[3]))
            message.date_read = from_apple_time(int(row[4]))
            message.destination_caller_id = row[5]
            res.append(message)
        return res

    def get_all_chat(self):
        res = []
        for row in self.cur.execute(
                'select guid, chat_identifier, service_name, last_read_message_timestamp, ROWID from chat order by ROWID desc'):
            chat = Chat()
            chat.guid = row[0]
            chat.chat_identifier = row[1]
            chat.service_name = row[2]
            chat.last_read_message_timestamp = from_apple_time(int(row[3]))
            chat.id = int(row[4])
            res.append(chat)
        return res

    def get_messages_for_chat(self, chat):
        res = []
        for row in self.cur.execute('select m.guid, m.text, m.service, m.date, m.date_read, m.destination_caller_id from message as m left join chat_message_join cmj on m.ROWID = cmj.message_id where chat_id = {}'.format(chat.id)):
            message = Message()
            message.guid = row[0]
            message.text = row[1]
            message.service = row[2]
            message.date = from_apple_time(int(row[3]))
            message.date_read = from_apple_time(int(row[4]))
            message.destination_caller_id = row[5]
            res.append(message)
        return res