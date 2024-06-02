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

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def email(self, request, pk=None):
        document = self.get_object()
        recipient_email = request.data.get('recipient_email')
        if recipient_email:
            EmailLog.objects.create(document=document, user=request.user, recipient_email=recipient_email)

            subject = 'Document from Our Service'
            message = f'Please find the document {document.title} attached.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [recipient_email]

            # Create the email
            email = EmailMessage(
                subject,
                message,
                email_from,
                recipient_list,
            )
            email.attach_file(document.file.path)

            try:
                email.send()
                return Response({'status': 'document emailed'})
            except Exception as e:
                return Response({'error': str(e)}, status=500)
        else:
            return Response({'error': 'recipient_email is required'}, status=400)


class DownloadViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Download.objects.all()
    serializer_class = DownloadSerializer
    permission_classes = [permissions.IsAuthenticated]


class EmailLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EmailLog.objects.all()
    serializer_class = EmailLogSerializer
    permission_classes = [permissions.IsAuthenticated]
