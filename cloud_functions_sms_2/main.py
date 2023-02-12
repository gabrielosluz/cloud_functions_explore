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

    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body='This is the ship that made the Kessel Run in fourteen parsecs?',
        from_='+16812461902',
        media_url=['https://c1.staticflickr.com/3/2899/14341091933_1e92e62d12_b.jpg'],
        to='+5521982930075'
    )

    print(message.sid)