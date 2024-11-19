
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        return instance


class TextToSpeechSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=115000)
    language = serializers.CharField(max_length=10)
    selectedVoice = serializers.CharField(max_length=10)



# class TextToSpeechSerializerVideo(serializers.Serializer):
#     text = serializers.CharField(max_length=5000)
#     language = serializers.CharField(max_length=5)
#     selectedVoice = serializers.CharField(max_length=10)
#     videoFile = serializers.FileField()

class TextToSpeechSerializerVideo(serializers.Serializer):
    text = serializers.CharField()
    language = serializers.CharField()
    selectedVoice = serializers.CharField()
    videoFile = serializers.FileField()

class UserSerializerProfile(serializers.ModelSerializer):
    class Meta:
        Model= User
        fields= ['id', 'username', 'email', 'first_name', 'last_name']  