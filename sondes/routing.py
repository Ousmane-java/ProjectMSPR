from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/sondes/', consumers.SondaConsumer.as_asgi()),
]
