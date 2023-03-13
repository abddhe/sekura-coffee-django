import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.dispatch import receiver
from django.db.models.signals import post_save
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from menu.models import (Order, Notification)


class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = "orders"
        self.room_group_name = "orders_%s" % self.room_name
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.send(text_data=json.dumps({"type": "disconnect", "message": "disconnected"}))

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "notification"}
        )

    async def notification(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({'data': event['data'], "message": event['message']}))
