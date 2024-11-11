# consumer.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # اتصال به گروه
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # قطع اتصال از گروه
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # دریافت پیام از WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']  # نام فرستنده

        # ارسال پیام به گروه
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,  # ارسال نام فرستنده
            }
        )

    # ارسال پیام به WebSocket
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']  # دریافت نام فرستنده

        # ارسال پیام به WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,  # ارسال نام فرستنده
        }))
