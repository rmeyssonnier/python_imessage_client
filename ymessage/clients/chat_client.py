from typing import Optional

from ymessage.models.attachment import Attachment
from ymessage.models.chat import Chat
from ymessage.clients.client import Client
from ymessage.models.message import Message
from ymessage.tools.tools import from_apple_time


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
                'select ROWID, guid, chat_identifier, service_name, last_read_message_timestamp, MAX(message_date) from chat '
                'inner join chat_message_join cmj on chat.ROWID = cmj.chat_id '
                'group by ROWID order by ROWID desc'):
            chat = Chat(int(row[0]), row[1], row[2], row[3], from_apple_time(int(row[4])), from_apple_time(int(row[5])))
            res.append(chat)
        return res

    def get_chat_by_id(self, chat_id) -> Optional[Chat]:
        row = self.cur.execute(f'select ROWID, guid, chat_identifier, service_name, last_read_message_timestamp, MAX(message_date) from chat \
                inner join chat_message_join cmj on chat.ROWID = cmj.chat_id \
                where ROWID={chat_id}').fetchone()
        if row is None:
            return None

        chat = Chat(int(row[0]), row[1], row[2], row[3], from_apple_time(int(row[4])), from_apple_time(int(row[5])))
        return chat

    def get_messages_for_chat(self, chat_id, start, length):
        res = []
        for row in self.cur.execute(f'select m.ROWID, m.text, m.service, m.date, m.date_read, m.destination_caller_id, m.is_from_me, m.cache_has_attachments \
                                    from message as m left join chat_message_join cmj on m.ROWID = cmj.message_id \
                                    where cmj.chat_id = {chat_id} \
                                    order by m.date desc limit {length} offset {start}'):
            message = Message(row[0], row[1], row[2], from_apple_time(int(row[3])), from_apple_time(int(row[4])),
                              row[5], bool(row[6]), bool(row[7]))
            res.append(message)
        return res

    def get_attachments(self, message_id):
        res = []
        for row in self.cur.execute(f'select ROWID, mime_type, filename from attachment \
                inner join message_attachment_join maj on attachment.ROWID = maj.attachment_id \
                where message_id = {message_id}'):
            attachment = Attachment(int(row[0]), row[1], row[2])
            res.append(attachment)
        return res

    def get_attachment_by_id(self, attachment_id):
        row = self.cur.execute(f'select ROWID, mime_type, filename from attachment \
                        where ROWID = {attachment_id}').fetchone()
        return Attachment(int(row[0]), row[1], row[2])

