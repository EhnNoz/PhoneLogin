from twilio.rest import Client
from django.conf import settings


def send_sms(to_phone_number, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    try:
        message = client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to_phone_number
        )
        return True
    except Exception as e:
        print(f"Failed to send SMS: {e}")
        return False