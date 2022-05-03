import json

import jsonpickle as jsonpickle
from flask import Flask, request, Response

from pymessage.messaging import Messaging


class PyMessageApi:
    def __init__(self, name, host, port):
        self.host = host
        self.port = port
        self.messaging = Messaging()
        self.app = Flask(name)
        self.register_urls()

    def run(self):
        self.app.run(host=self.host, port=self.port)

    def register_urls(self):
        self.app.add_url_rule('/chat', view_func=self.get_all_chats, methods=['GET'])
        self.app.add_url_rule('/chat/<int:chat_id>', view_func=self.get_chat_by_id, methods=['GET'])
        self.app.add_url_rule('/message/send', view_func=self.send_message, methods=['POST'])

    def get_all_chats(self):
        self.messaging.init()
        res = self.messaging.get_all_conversations(load_messages=False)

        return Response(jsonpickle.encode(res, unpicklable=False), mimetype='application/json')

    def get_chat_by_id(self, chat_id):
        self.messaging.init()
        res = self.messaging.get_conversation_by_id(chat_id)

        return Response(jsonpickle.encode(res, unpicklable=False), mimetype='application/json')

    def send_message(self):
        phone = request.json['phone_number']
        message = request.json['message']
        self.messaging.send(phone, message)
        return Response(jsonpickle.encode({"result": True}, unpicklable=False), mimetype='application/json')


def run_api(host, port):
    app = PyMessageApi('py_message_api', host, port)
    app.run()
