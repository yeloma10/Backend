from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from gtts import gTTS
from io import BytesIO
from account.serializer import TextToSpeechSerializer
from googletrans import Translator

from education.models import Parametre_vocal  # Utiliser Google Translate pour la traduction

@api_view(['POST'])
def text_to_speech(request):
    if request.method == 'POST':
        serializer = TextToSpeechSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data['text']
            language = serializer.validated_data['language']
            selected_voice = serializer.validated_data['selectedVoice']

            # Sauvegarde des données dans la base de données
            tts_request = Parametre_vocal.objects.create(
                text=text,
                language=language,
                selected_voice=selected_voice
            )
            tts_request.save()
            
            # Traduction si nécessaire
            if language == 'en' and not is_english(text):  # Si la langue sélectionnée est anglais et le texte n'est pas déjà en anglais
                translator = Translator()
                text = translator.translate(text, src='fr', dest='en').text
            elif language == 'fr' and is_english(text):  # Si la langue sélectionnée est français et le texte est en anglais
                translator = Translator()
                text = translator.translate(text, src='en', dest='fr').text
            elif language == 'es' and not is_spanish(text):  # Si la langue sélectionnée est espagnol et le texte n'est pas déjà en espagnol
                translator = Translator()
                text = translator.translate(text, src='fr', dest='es').text
            elif language == 'de' and not is_german(text):  # Si la langue sélectionnée est allemand et le texte n'est pas déjà en allemand
                translator = Translator()
                text = translator.translate(text, src='fr', dest='de').text

            try:
                tts = gTTS(text=text, lang=language, slow=False)
                speech_file = BytesIO()
                tts.write_to_fp(speech_file)
                speech_file.seek(0)

                response = HttpResponse(speech_file, content_type='audio/mp3')
                response['Content-Disposition'] = 'attachment; filename="speech.mp3"'
                
                return response
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse(serializer.errors, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

# Fonction pour vérifier si le texte est déjà en anglais
def is_english(text):
    try:
        # Simple vérification en utilisant Google Translate pour détecter la langue
        translator = Translator()
        detected_lang = translator.detect(text).lang
        return detected_lang == 'en'
    except Exception as e:
        return False

# Fonction pour vérifier si le texte est déjà en espagnol
def is_spanish(text):
    try:
        # Simple vérification en utilisant Google Translate pour détecter la langue
        translator = Translator()
        detected_lang = translator.detect(text).lang
        return detected_lang == 'es'
    except Exception as e:
        return False

# Fonction pour vérifier si le texte est déjà en allemand
def is_german(text):
    try:
        # Simple vérification en utilisant Google Translate pour détecter la langue
        translator = Translator()
        detected_lang = translator.detect(text).lang
        return detected_lang == 'de'
    except Exception as e:
        return False
