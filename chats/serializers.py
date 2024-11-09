from rest_framework import serializers
from .models import Chat


class ChatSerializer(serializers.ModelSerializer):
    user1 = serializers.StringRelatedField(source='user1.username')
    user2 = serializers.StringRelatedField(source='user2.username')

    class Meta:
        model = Chat  # مدل مربوطه را مشخص می‌کنیم
        fields = ['id', 'created_at', 'user1', 'user2']  # فیلدهایی که می‌خواهیم در خروجی باشند
