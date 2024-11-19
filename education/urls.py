from django.urls import path
from .views import text_to_speech

urlpatterns = [
    path('text-to-speech/', text_to_speech, name='text_to_speech'),
]
