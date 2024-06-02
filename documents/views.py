from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.mail import EmailMessage
from django.http import FileResponse
from django.conf import settings
from .models import CustomUser, Document, Download, EmailLog
from .serializers import CustomUserSerializer, DocumentSerializer, DownloadSerializer, EmailLogSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def download(self, request, pk=None):
        document = self.get_object()
        Download.objects.create(document=document, user=request.user)

        response = FileResponse(document.file.open(), as_attachment=True, filename=document.file.name)
        return response
