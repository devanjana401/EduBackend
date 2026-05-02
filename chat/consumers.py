import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.course_id = self.scope['url_route']['kwargs']['course_id']
        # this is the student's id from the URL path
        self.student_id = self.scope['url_route']['kwargs']['user_id']
        
        # both student and vendor must join this identical string
        self.room_group_name = f'chat_{self.course_id}_{self.student_id}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        sender_id = data.get('sender_id') # Current sender (Vendor or Student)

        # save to DB
        await self.save_message(sender_id, message)

        # broadcast to everyone in the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id
            }
        )

    async def chat_message(self, event):
        # pushes to the frontend
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_id': event['sender_id']
        }))

    @database_sync_to_async
    def save_message(self, sender_id, message):
        from django.contrib.auth import get_user_model
        from userside.models import ChatMessage
        from vendorside.models import Course
        
        User = get_user_model()
        try:
            sender = User.objects.get(id=sender_id)
            # the 'owner' of the chat context is always the student (from URL)
            student = User.objects.get(id=self.student_id)
            course = Course.objects.get(id=self.course_id)
            
            return ChatMessage.objects.create(
                user=student,
                course=course,
                sender=sender,
                message=message
            )
        except Exception as e:
            print(f"Chat Error: {e}")
            return None