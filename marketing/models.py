from django.db import models

class TextToSpeechRequest(models.Model):
    text = models.TextField()
    language = models.CharField(max_length=10)
    selected_voice = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='videos/')
    audio_file = models.FileField(upload_to='audio/')
    video_with_audio = models.FileField(upload_to='processed_videos/')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"TextToSpeechRequest for {self.language} at {self.timestamp}"
