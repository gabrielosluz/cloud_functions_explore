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

    account_sid = 'AC22fcfed0682af349f9713c409273d4c3'
    auth_token = '2bcbf768bf56e61d222fc47ce5d6dcd9'
    client = Client(account_sid, auth_token)

    # message = client.messages \
    #     .create(
    #     body='This is the ship that made the Kessel Run in fourteen parsecs?',
    #     from_='+15017122661',
    #     to='+15558675310'
    # )

    numbers_to_message = ['+5521982930075', '+5521992924005', '+5521994675452', '+5521975600522', '+5521988667469', '+5521996357742', '+5521975287060', '+5521998087781', '+5521980862382', '+5521964787456', '+5521982151748','+5521999016181', '+5531993515421']
    for number in numbers_to_message:
        client.messages.create(
            body='Mensagem para voce:' + pubsub_message,
            from_='+15154894323',
            to=number
        )
    print(numbers_to_message)

    # print(message.sid)
