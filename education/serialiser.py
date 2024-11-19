from rest_framework import serializers

class TextToSpeechSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=5000)  # Le texte à convertir
    language = serializers.CharField(max_length=10)  # Langue du texte
    selectedVoice = serializers.CharField(max_length=10)  # Voix sélectionnée
    speed = serializers.IntegerField(min_value=1, max_value=200, required=False)  # Vitesse de la parole
    username = serializers.IntegerField()  # ID de l'utilisateur qui envoie la requête

    def validate_language(self, value):
        valid_languages = ['en', 'fr', 'es', 'de']
        if value not in valid_languages:
            raise serializers.ValidationError(f"Invalid language code: {value}")
        return value
