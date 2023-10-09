import json
from app.config import settings
from azure.servicebus import ServiceBusClient

with ServiceBusClient.from_connection_string(settings.ASB_CONNECTION_STRING) as sb_client:
    receiver = sb_client.get_queue_receiver(queue_name=settings.QUEUE_NAME)
    with receiver:
        for message in receiver:
            event = json.loads(str(message))
            print(f"Received event: {event['data']}")
            # mark message as completed
            receiver.complete_message(message)
