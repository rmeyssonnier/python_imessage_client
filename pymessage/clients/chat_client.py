from typing import Optional

from pymessage.models.chat import Chat
from pymessage.clients.client import Client
from pymessage.models.message import Message
from pymessage.tools.tools import from_apple_time


class ChatClient(Client):
    def __init__(self, path):
        super().__init__(path)

    def get_last_messages(self, count=10) -> [Message]:
        res = []
        for row in self.cur.execute(
                'select guid, text, service, date, date_read, destination_caller_id, is_from_me'
                'from message order by ROWID desc limit {}'.format(count)):
            message = Message(row[0], row[1], row[2], from_apple_time(int(row[3])), from_apple_time(int(row[4])),
                              row[5], bool(row[6]))
            res.append(message)
        return res

    def get_all_chat(self) -> [Chat]:
        res = []
        for row in self.cur.execute(
                'select ROWID, guid, chat_identifier, service_name, last_read_message_timestamp '
                'from chat order by ROWID desc'):
            chat = Chat(int(row[0]), row[1], row[2], row[3], from_apple_time(int(row[4])))
            res.append(chat)
        return res

    def get_chat_by_id(self, chat_id) -> Optional[Chat]:
        row = self.cur.execute(f'select ROWID, guid, chat_identifier, service_name, last_read_message_timestamp \
                  from chat where ROWID = {chat_id}').fetchone()
        if row is None:
            return None

        chat = Chat(int(row[0]), row[1], row[2], row[3], from_apple_time(int(row[4])))
        return chat

    def get_messages_for_chat(self, chat):
        res = []
        for row in self.cur.execute(f'select m.guid, m.text, m.service, m.date, m.date_read, m.destination_caller_id, m.is_from_me \
                                    from message as m left join chat_message_join cmj on m.ROWID = cmj.message_id \
                                    where cmj.chat_id = {chat.id} \
                                    order by m.date desc '):
            message = Message(row[0], row[1], row[2], from_apple_time(int(row[3])), from_apple_time(int(row[4])),
                              row[5], bool(row[6]))
            res.append(message)
        return res
