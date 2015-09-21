from django.contrib import admin

from .models import Message

class MessageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['username']}),
        ('Date information', {'fields': ['post_time']}),
        (None,               {'fields': ['message_text']}),
    ]

admin.site.register(Message, MessageAdmin)

