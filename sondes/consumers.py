import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)

class SondaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Connexion WebSocket"""
        logger.info("Nouvelle connexion WebSocket")
        await self.channel_layer.group_add("sonda_updates", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """Déconnexion WebSocket"""
        logger.info(f"Déconnexion WebSocket : {close_code}")
        await self.channel_layer.group_discard("sonda_updates", self.channel_name)

    async def receive(self, text_data):
        """Réception d'un message WebSocket"""
        logger.info(f"Message reçu : {text_data}")
        await self.send(text_data=json.dumps({"message": "Message reçu"}))

    async def send_status_update(self, event):
        """Envoi d'une mise à jour en temps réel à tous les clients connectés"""
        logger.info(f"Envoi d'une mise à jour : Franchise {event['franchise_id']} - Statut {event['status']}")
        await self.send(text_data=json.dumps({
            "franchise_id": event["franchise_id"],
            "status": event["status"]
        }))
