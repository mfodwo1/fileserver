from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Document, Download, EmailLog


# Register the CustomUser model
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Add any custom configurations here if needed
    pass


# Register the Document model
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_by', 'upload_date', 'download_count', 'email_count')
    search_fields = ('title', 'uploaded_by__username')
    list_filter = ('upload_date',)
    readonly_fields = ('download_count', 'email_count')

    def download_count(self, obj):
        return obj.download_count()

    def email_count(self, obj):
        return obj.email_count()

    download_count.short_description = 'Download Count'
    email_count.short_description = 'Email Count'


# Register the Download model
@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    list_display = ('document', 'user', 'download_date')
    search_fields = ('document__title', 'user__username')
    list_filter = ('download_date',)


# Register the EmailLog model
@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('document', 'user', 'recipient_email', 'email_date')
    search_fields = ('document__title', 'user__username', 'recipient_email')
    list_filter = ('email_date',)
