from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from chats.models import Chat, Message
from chats.serializers import ChatSerializer
from users.models import User
import json

@api_view(['POST'])
def create_chat(request, user_id):
    current_user = request.user

    try:
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "user not found"}, status=status.HTTP_404_NOT_FOUND)

    if current_user == target_user:
        return Response({"error": "you cant chat with yourself"}, status=status.HTTP_400_BAD_REQUEST)

    existing_chat = Chat.objects.filter(
        (Q(user1=current_user) & Q(user2=target_user)) |
        (Q(user1=target_user) & Q(user2=current_user))
    ).first()

    if existing_chat:
        return Response({
            "message": "chat already existed",
            "chat_id": existing_chat.id,
            "user1": existing_chat.user1.username,
            "user2": existing_chat.user2.username
        }, status=status.HTTP_200_OK)

    chat = Chat.objects.create(user1=current_user, user2=target_user)

    return Response({
        "message": "chat created successfully",
        "chat_id": chat.id,
        "user1": chat.user1.username,
        "user2": chat.user2.username
    }, status=status.HTTP_201_CREATED)



@api_view(['GET'])
def list_chats(request):
    current_user = request.user
    chats = Chat.objects.filter(user1=current_user) | Chat.objects.filter(user2=current_user)
    serializer = ChatSerializer(chats, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@login_required
def chat_room(request, room_name):
    chat = get_object_or_404(Chat, id=room_name)
    if request.user != chat.user1 and request.user != chat.user2:
        return HttpResponseForbidden("شما اجازه دسترسی به این چت را ندارید.")

    return render(request, 'chats/chat_room.html', {
        'room_name': room_name,
        'chat': chat
    })

@login_required
def get_messages(request, chat_id):
    chat = Chat.objects.get(id=chat_id)
    messages = chat.messages.all().order_by('timestamp')
    message_data = []
    for message in messages:
        message_data.append({
            'sender': message.sender.username,
            'content': message.content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    return JsonResponse(message_data, safe=False)

@csrf_exempt
def send_message(request, room_name):
    if request.method == 'POST':
        data = json.loads(request.body)
        message_content = data.get('message')

        chat = Chat.objects.get(id=room_name)

        message = Message.objects.create(
            chat=chat,
            sender=request.user,
            content=message_content
        )

        return JsonResponse({
            "success": True,
            "message": message_content,
            "sender": request.user.username
        })
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)
