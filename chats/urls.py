# chat/urls.py
from django.urls import path
from . import consumers, views

urlpatterns = [
    path('create-chat/<int:user_id>/', views.create_chat, name='create_chat'),
    path('chat-list/', views.list_chats, name='list_chats'),
    path('chat/<str:room_name>/', views.chat_room, name='chat_room'),
    path('<int:chat_id>/messages/', views.get_messages, name='get_messages'),
    path('<str:room_name>/send_message/', views.send_message, name='send_message'),
]
