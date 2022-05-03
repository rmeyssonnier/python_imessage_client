class Message:
    def __init__(self, guid, text, service, date, date_read, destination_caller_id, is_from_me):
        self.guid = guid
        self.text = text
        self.service = service
        self.date = date
        self.date_read = date_read
        self.destination_caller_id = destination_caller_id
        self.is_from_me = is_from_me

    def __str__(self):
        if self.is_from_me:
            sens = '->'
        else:
            sens = '<-'
        return '{} {}'.format(sens, self.text.replace('\n', '\\n'))