from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
  
    path("", home_page, name="home"),
    path("psybot/", psybot_page, name="psybot"),
    path("delete-chat/", delete_chat, name="delete_chat"),
    path("journal/", journal_page, name="journal"),
    path("delete-entry/", delete_entry, name="delete_entry"),
    path("therapy/", therapy_page, name="therapy")
]