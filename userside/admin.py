from django.contrib import admin
from . models import Purchase,ChatMessage
# Register your models here.


admin.site.register(Purchase)
@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'course', 'message', 'timestamp')
    list_filter = ('course', 'timestamp')