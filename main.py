import os

from pymessage.client import Client


def main():
    home = os.environ['HOME']
    db_path = f'{home}/Library/Messages/chat.db'

    client = Client(db_path)
    client.connect()

    chats = client.get_all_chat()
    messages = client.get_messages_for_chat(chats[2])

    client.close()


if __name__ == '__main__':
    main()
