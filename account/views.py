from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .serializer import *
from django.http import JsonResponse

User = get_user_model()

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserProfileView(generics.RetrieveAPIView):
    def get(self, request, id):
        try:
            user = User.objects.get(pk=id)
            user_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                # Ajoutez d'autres champs que vous souhaitez exposer
            }
            return JsonResponse(user_data, status=200)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)


# Récupérer tous les utilisateurs
class GetAllUsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Mettre à jour un utilisateur en fonction de son ID
class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'  # Utilisation de l'ID pour la mise à jour

    def put(self, request, id):
        try:
            user = User.objects.get(pk=id)
            serializer = UserSerializer(user, data=request.data, partial=True)  # partial=True permet de ne mettre à jour que les champs modifiés
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=200)
            return JsonResponse(serializer.errors, status=400)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        
class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'  # Utilisation de l'ID pour la mise à jour

    def delete(self, request, id):
        try:
            user = User.objects.get(pk=id)
            user.delete()
            return JsonResponse({"message": "User deleted"}, status=200)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        