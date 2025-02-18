import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)

class SondaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info("Nouvelle connexion WebSocket")
        await self.channel_layer.group_add(
            "sonda_updates",  # Nom du groupe
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        logger.info(f"Déconnexion WebSocket : {close_code}")
        await self.channel_layer.group_discard(
            "sonda_updates",
            self.channel_name
        )

    # Recevoir un message depuis le WebSocket
    async def receive(self, text_data):
        logger.info(f"Message reçu : {text_data}")
        data = json.loads(text_data)
        message = data.get('message', 'Aucun message reçu')
        await self.send(text_data=json.dumps({
            "message": f"Message reçu : {message}"
        }))

    # Envoyer un message depuis le backend
    async def sonda_status_update(self, event):
        message = event['message']
        logger.info(f"Message backend reçu : {message}")
        await self.send(text_data=json.dumps({
            "message": message
        }))
