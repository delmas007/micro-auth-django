
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
import requests
from authentification.serializers import LoginSerializer


# Create your views here.

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Authentification réussie
                email = user.email
                external_api_url = 'http://external-service-url'

                # Envoyer une requête POST à l'autre service
                response = requests.post(external_api_url, json={'email': email})

                if response.status_code == 200:
                    return Response({'detail': 'Authentification réussie et traitement externe réussi'}, status=status.HTTP_200_OK)
                else:
                    return Response({'detail': 'Erreur lors du traitement externe'}, status=response.status_code)
            else:
                return Response({'detail': 'Identifiants invalides'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
