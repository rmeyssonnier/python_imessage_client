import json
import os

import jsonpickle as jsonpickle
from flask import Flask, request, Response, send_file
from flask_cors import CORS, cross_origin

from ymessage.messaging import Messaging


class PyMessageApi:
    def __init__(self, name, host, port):
        self.host = host
        self.port = port
        self.messaging = Messaging()
        self.app = Flask(name)
        self.cors = CORS(self.app)
        self.app.config['CORS_HEADERS'] = 'Content-Type'
        self.register_urls()

    def run(self):
        self.app.run(host=self.host, port=self.port)

    def register_urls(self):
        self.app.add_url_rule('/chat', view_func=self.get_all_chats, methods=['GET'])
        self.app.add_url_rule('/chat/<int:chat_id>', view_func=self.get_chat_by_id, methods=['GET'])
        self.app.add_url_rule('/message/send', view_func=self.send_message, methods=['POST'])
        self.app.add_url_rule('/message/<int:chat_id>/<int:start>/<int:length>', view_func=self.get_messages,
                              methods=['GET'])
        self.app.add_url_rule('/attachment/<int:attachment_id>', view_func=self.get_attachment, methods=['GET'])

    @cross_origin()
    def get_all_chats(self):
        self.messaging.init()
        res = self.messaging.get_all_conversations(load_messages=False)

        return Response(jsonpickle.encode(res, unpicklable=False), mimetype='application/json')

    @cross_origin()
    def get_chat_by_id(self, chat_id):
        self.messaging.init()
        res = self.messaging.get_conversation_by_id(chat_id, 0, 15)

        return Response(jsonpickle.encode(res, unpicklable=False), mimetype='application/json')

    @cross_origin()
    def get_messages(self, chat_id, start, length):
        self.messaging.init()
        res = self.messaging.get_messages(chat_id, start, length)

        return Response(jsonpickle.encode(res, unpicklable=False), mimetype='application/json')

    @cross_origin()
    def send_message(self):
        phone = request.json['phone_number']
        message = request.json['message']
        self.messaging.send(phone, message)
        return Response(jsonpickle.encode({"result": True}, unpicklable=False), mimetype='application/json')

    @cross_origin()
    def get_attachment(self, attachment_id):
        self.messaging.init()
        attachment = self.messaging.get_attachment(attachment_id)
        return send_file(attachment.filename.replace('~', os.environ['HOME']), mimetype=attachment.mime_type)


def run_api(host, port):
    app = PyMessageApi('py_message_api', host, port)
    app.run()
