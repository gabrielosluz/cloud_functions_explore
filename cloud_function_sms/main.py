import base64
import os
from twilio.rest import Client


def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print(pubsub_message)

    account_sid = 'AC0d451b7f8ebb5155874000ca292aa727'
    auth_token = '19fe1145ccdd15556d6a16f3ce5b9f4e'
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body='Mensagem:' + pubsub_message,
        from_='+16812461902',
        to='+55982930075'
    )

    print(message.sid)
