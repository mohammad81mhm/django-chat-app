from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from chats.models import Chat
from chats.serializers import ChatSerializer
# from chats.models import Chat
from users.models import User


# Create your views here.

@api_view(['POST'])
def create_chat(request, user_id):
    current_user = request.user

    try:
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "کاربر مورد نظر پیدا نشد."}, status=status.HTTP_404_NOT_FOUND)

    if current_user == target_user:
        return Response({"error": "شما نمی‌توانید با خودتان چت ایجاد کنید."}, status=status.HTTP_400_BAD_REQUEST)

    chat = Chat.objects.create(user1=current_user, user2=target_user)

    return Response({
        "message": "چت جدید با موفقیت ایجاد شد.",
        "chat_id": chat.id,
        "user1": chat.user1.username,
        "user2": chat.user2.username
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def list_chats(request):
    current_user = request.user

    chats = Chat.objects.filter(user1=current_user) | Chat.objects.filter(user2=current_user)

    if not chats.exists():
        return Response({"message": "هیچ چتی یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ChatSerializer(chats, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)