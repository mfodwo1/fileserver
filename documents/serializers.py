from rest_framework import serializers
from .models import CustomUser, Document, Download, EmailLog


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'file', 'upload_date', 'uploaded_by']


class DownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Download
        fields = ['id', 'document', 'user', 'download_date']


class EmailLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailLog
        fields = ['id', 'document', 'user', 'recipient_email', 'email_date']
