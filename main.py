from pymessage.messaging import Messaging


def main():
    messaging = Messaging()
    messaging.init()

    for c in messaging.get_conversations():
        print(c)

    chat = messaging.get_chat(242)
    print(chat)

    messaging.send(chat.contact.phone_number, 'Hey!')

    for m in chat.messages:
        print(m)

    messaging.close()


if __name__ == '__main__':
    main()
