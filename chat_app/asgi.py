import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from chats import consumers  # فرض میکنیم که کد WebSocket در داخل اپلیکیشن chat قرار داره

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(  # برای احراز هویت
        URLRouter([
            path("ws/chat/<str:chat_id>/", consumers.ChatConsumer.as_asgi()),  # مسیر WebSocket
        ])
    ),
})
