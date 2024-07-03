
from django.urls import path

from authentification.views import registration_view, login_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', registration_view, name='register'),
]
