from django.contrib import admin
from .models import *
from django.contrib.admin import ModelAdmin
from accounts.mixins import ExportCsvMixin

@admin.register(FAQ)
class FAQAdmin(ExportCsvMixin, ModelAdmin):
    search_fields = ['subject', 'question_types']
    list_display = ['subject', 'content', 'question_types']
    list_display_links = ['subject']
    search_help_text = "Search by subject"
    list_filter = ('subject', 'question_types')
 
 
@admin.register(Feedback)
class FeedbackAdmin(ExportCsvMixin, ModelAdmin):
    search_fields = ['sender', 'receiver']
    list_display = ['sender', 'receiver','message']
    list_display_links = ['sender']
    search_help_text = 'Search by Sender'
    list_filter = ('sender','receiver')
    

@admin.register(Contact)
class FeedbackAdmin(ExportCsvMixin, ModelAdmin):
    search_fields = ['email']
    list_display = ['email','phone_number','message']
    list_display_links = ['email']
    