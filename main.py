from pymessage.api.py_message_api import run_api
from pymessage.messaging import Messaging


def main():
    test = False
    if test:
        messaging = Messaging()
        messaging.init()

        for c in messaging.get_all_conversations():
            print(c)

        chat = messaging.get_conversation_by_id(242)
        print(chat)

        messaging.send(chat.contact.phone_number, 'Hey!')

        for m in chat.messages:
            print(m)

        messaging.close()
    else:
        run_api('0.0.0.0', 8080)


if __name__ == '__main__':
    main()
