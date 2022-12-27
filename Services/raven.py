import os
from twilio.rest import Client


class Raven:
    def __init__(self, identity):
        self.identity = identity
        if identity == "Jarvis":
            self.source_number = os.environ.get('TWILIO_JARVIS_NUM')
        else:
            self.source_number = os.environ.get('TWILIO_SRC_NUM')
        self.target_number = os.environ.get('TWILIO_TAR_NUM')
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        self.client = Client(account_sid, auth_token)

    def send_a_message(self, body):
        self.client.messages.create(
            body=body,
            from_=self.source_number,
            to=self.target_number
        )
        print("*** INFO: Message sent")
