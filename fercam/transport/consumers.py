from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
     print("Line 6. This get's called as soon as the server runs")
     async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        print('self.scope: ', self.scope['url_route']['kwargs']['room_name'])
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print('line 16 in ChatConsumer. This happens when you click on create a room')
        await self.accept()
        print('after accept')
        print(" ")

     async def disconnect(self, close_code):
        print('line 21 Disconnect method -- before code')
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print('line 27 after code in disconnect method')

    # Receive message from WebSocket
     async def receive(self, text_data):
        print('line 31 in receive method -- before code')
        text_data_json = json.loads(text_data)
        user = text_data_json['user']
        message = text_data_json['message']
        print('The message is: ', message)
        print('line 34  in receive method, before async_to_sync')
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user,
            }

        )

        print('line 43 in receive method. After code!')

    # Receive message from room group
     async def chat_message(self, event):

        print("Line 47 in chat_message method before code")
        message = event['message']
        print('event: ', event)
        print('self: ', self)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': event['user'],
        }))
        print('line 54 in chat_message. after code')
