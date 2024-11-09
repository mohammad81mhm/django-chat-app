import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Chat
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'

        # اضافه کردن کاربر به گروه چت
        self.room_group_name = f'chat_{self.chat_id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # حذف کاربر از گروه چت
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # دریافت پیام از WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']
        user = self.scope['user']

        # ذخیره پیام در دیتابیس
        chat = Chat.objects.get(id=self.chat_id)
        message = Message.objects.create(
            chat=chat,
            sender=user,
            content=message_content
        )

        # ارسال پیام به گروه چت
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message.content,
                'sender': user.username,
            }
        )

    # دریافت پیام از گروه چت
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # ارسال پیام به WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
        }))
