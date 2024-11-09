# chat/urls.py
from django.urls import path
from . import consumers, views

urlpatterns = [
    path('create-chat/<int:user_id>/', views.create_chat, name='create_chat'),
    path('chat-list/', views.list_chats, name='list_chats'),

]
