import glob
import os
from pathlib import Path

from pymessage.chat_client import ChatClient
from pymessage.client import Client
from pymessage.contact_client import ContactClient
from pymessage.tools import get_contact_db


def main():
    home = os.environ['HOME']
    message_db_path = f'{home}/Library/Messages/chat.db'
    contact_db_path = get_contact_db('/Users/robinmeyssonnier/Library/Application Support/AddressBook/')

    message_client = ChatClient(message_db_path)
    message_client.connect()
    chats = message_client.get_all_chat()
    messages = message_client.get_messages_for_chat(chats[2])
    message_client.close()

    contact_client = ContactClient(contact_db_path)
    contact_client.connect()
    contacts = contact_client.get_all()
    contact_client.get_by_number('')
    contact_client.close()


if __name__ == '__main__':
    main()
