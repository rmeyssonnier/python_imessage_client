import os
from typing import Optional

from pymessage.chat import Chat
from pymessage.chat_client import ChatClient
from pymessage.contact import Contact
from pymessage.contact_client import ContactClient
from pymessage.tools import get_contact_db


class Messaging:
    __home = os.environ['HOME']
    __message_db_path = f'{__home}/Library/Messages/chat.db'
    __contact_db_path = get_contact_db(f'{__home}/Library/Application Support/AddressBook/')

    def __init__(self):
        self.chat_client = ChatClient(self.__message_db_path)
        self.contact_client = ContactClient(self.__contact_db_path)

    def init(self):
        self.chat_client.connect()
        self.contact_client.connect()

    def close(self):
        self.chat_client.close()
        self.contact_client.close()

    def get_conversations(self) -> [Chat]:
        chats = self.chat_client.get_all_chat()
        for chat in chats:
            chat = self.__set_contact_to_chat(chat)
            chat.messages = self.chat_client.get_messages_for_chat(chat)
        return chats

    def get_chat(self, chat_id) -> Optional[Chat]:
        chat = self.chat_client.get_chat_by_id(chat_id)
        if chat is None:
            return None
        chat = self.__set_contact_to_chat(chat)
        chat.messages = self.chat_client.get_messages_for_chat(chat)
        return chat

    def __set_contact_to_chat(self, chat) -> Chat:
        chat.contact = self.contact_client.get_by_number(chat.chat_identifier)
        if chat.contact is None:
            chat.contact = Contact()
            chat.contact.name = 'Unknown'
            chat.contact.phone_number = chat.chat_identifier
        return chat
