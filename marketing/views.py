import time
import os
import tempfile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip
from account.serializer import TextToSpeechSerializerVideo
from googletrans import Translator
from .models import TextToSpeechRequest  # Assurez-vous d'importer le modèle

class TextToSpeechView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TextToSpeechSerializerVideo(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data.get('text')
            language = serializer.validated_data.get('language')
            selected_voice = serializer.validated_data.get('selectedVoice')
            video_file = serializer.validated_data.get('videoFile')

            # Traduction si nécessaire
            if language == 'en' and not self.is_english(text):  # Si la langue sélectionnée est anglais et le texte n'est pas déjà en anglais
                translator = Translator()
                text = translator.translate(text, src='fr', dest='en').text
            elif language == 'fr' and self.is_english(text):  # Si la langue sélectionnée est français et le texte est en anglais
                translator = Translator()
                text = translator.translate(text, src='en', dest='fr').text

            # Génération du fichier audio avec gTTS
            tts = gTTS(text=text, lang=language, slow=False)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as audio_fp:
                tts.save(audio_fp.name)

                # Sauvegarder la vidéo
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as video_fp:
                    video_fp.write(video_file.read())
                    video_fp.close()

                    # Traiter la vidéo et l'audio
                    video_clip = VideoFileClip(video_fp.name)
                    audio_clip = AudioFileClip(audio_fp.name)

                    final_clip = video_clip.set_audio(audio_clip)          
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as final_fp:
                        final_clip.write_videofile(final_fp.name, codec='libx264', audio_codec='aac')
                        final_fp.seek(0)
                        response = HttpResponse(final_fp.read(), content_type="video/mp4")
                        response['Content-Disposition'] = 'attachment; filename="synced_video.mp4"'

            # Attendre un certain temps avant de supprimer les fichiers temporaires
            time.sleep(2)  # Attendez 2 secondes pour s'assurer que le processus est terminé

            # Sauvegarder les informations dans la base de données
            tts_request = TextToSpeechRequest(
                text=text,
                language=language,
                selected_voice=selected_voice,
                video_file=video_file,  # Vous pouvez envisager de sauvegarder les fichiers dans des emplacements appropriés
                audio_file=audio_fp.name,
                video_with_audio=final_fp.name
            )
            tts_request.save()

            # Nettoyage des fichiers temporaires
            try:
                os.remove(audio_fp.name)
                os.remove(video_fp.name)
                os.remove(final_fp.name)
            except Exception as e:
                print(f"Erreur lors de la suppression des fichiers temporaires: {e}")

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Fonction pour vérifier si le texte est déjà en anglais
    def is_english(self, text):
        try:
            # Simple vérification en utilisant Google Translate pour détecter la langue
            translator = Translator()
            detected_lang = translator.detect(text).lang
            return detected_lang == 'en'
        except Exception as e:
            return False
