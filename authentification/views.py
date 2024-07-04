from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
import requests

from authentification.RegistrationSerializer import RegistrationSerializer
from authentification.serializers import LoginSerializer


# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])  # Permet l'accès sans authentification
def login_view(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Authentification réussie
                email = user.email
                external_api_url = 'http://localhost:5050/generate-code/'

                # Envoyer une requête POST à l'autre service
                response = requests.post(external_api_url, json={'email': email})

                if response.status_code == 200:
                    return Response({'detail': 'Authentification réussie et traitement externe réussi',
                                     'mail': email,
                                     },
                                    status=status.HTTP_200_OK)
                else:
                    return Response({'detail': 'Erreur lors du traitement externe'}, status=response.status_code)
            else:
                return Response({'detail': 'Identifiants invalides'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'detail': 'Méthode non autorisée'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([AllowAny])  # Permet l'accès sans authentification
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Inscription réussie'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'detail': 'Méthode non autorisée'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
