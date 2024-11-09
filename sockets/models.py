from channels.generic.websocket import WebsocketConsumer
import json


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        self.send(text_data=json.dumps({'message': message}))

    def disconnect(self, close_code):
        pass
