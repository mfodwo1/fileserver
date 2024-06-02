from django.db import models
from users.models import CustomUser


class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    upload_date = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def download_count(self):
        return self.download_set.count()

    def email_count(self):
        return self.emaillog_set.count()

    def __str__(self):
        return self.title


class Download(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    download_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} downloaded {self.document.title}"


class EmailLog(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    recipient_email = models.EmailField()
    email_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} emailed {self.document.title} to {self.recipient_email}"
