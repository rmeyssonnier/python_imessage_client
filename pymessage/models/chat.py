from pymessage.models.contact import Contact
from pymessage.models.message import Message


class Chat:
    messages: [Message] = []
    contact: Contact = None

    def __init__(self, id, guid, chat_identifier, service_name, last_read_message_timestamp):
        self.id = id
        self.guid = guid
        self.chat_identifier = chat_identifier
        self.service_name = service_name
        self.last_read_message_timestamp = last_read_message_timestamp

    def __str__(self):
        if len(self.messages) > 0:
            return 'Id: {:5s} From: {:20s} Count: {:20s} Last message: {}'.format(str(self.id), self.contact.name, str(len(self.messages)),
                                                                        self.messages[0].text.replace('\n', '\\n '))
        else:
            return 'Id: {:5s} From: {:20s} Count: {:20s} Last message: None'.format(str(self.id), self.contact.name, str(len(self.messages)))

    def add_message(self, message: Message):
        self.messages.append(message)
