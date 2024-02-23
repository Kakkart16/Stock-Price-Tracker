import json

from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
from asgiref.sync import sync_to_async, async_to_sync
from django_celery_beat.models import PeriodicTask, IntervalSchedule

class StockConsumer(AsyncWebsocketConsumer):
    
    @sync_to_async
    def addToCeleryBeat(self, stock):
        task = PeriodicTask.objects.filter(name="every-20-seconds")
        if len(task)>0:
            task = task.first()
            args = json.loads(task.args)
            args = args[0]
            for x in stock:
                if x not in args:
                    args.append(x)
            task.args = json.dumps([args])
            task.save()
        else:
            schedule, created = IntervalSchedule.objects.get_or_create(every=20, period = IntervalSchedule.SECONDS)
            task = PeriodicTask.objects.create(interval = schedule, name='every-20-seconds', task="tracker.tasks.update_stock", args = json.dumps([stock]))

    # @sync_to_async    
    # def addToStockDetail(self, selected_stocks):
    #     user = self.scope["user"]
    #     for i in selected_stocks:
    #         stock, created = StockDetail.objects.get_or_create(stock = i)
    #         stock.user.add(user)
    
    
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"stock_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        query_params = parse_qs(self.scope["query_string"].decode())
        print(query_params)
        stock = query_params['stock']
        
        await self.addToCeleryBeat(stock)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "stock.message", "message": message}
        )

    # Receive message from room group
    async def send_stock_update(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))