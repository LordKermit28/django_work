from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from mailing.models import MailingLog


def logging_func(mailing, status, response):
    log = MailingLog(
        mailing=mailing,
        timestamp=timezone.now(),
        status=status,
        server_response=response
    )
    log.save()


def send_mailing(mailing):
    clients = mailing.clients.all()
    messages = mailing.messages.all()

    for client in clients:
        for message in messages:
            response = send_mail(
                subject=message.subject,
                message=message.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email],
            )
            logging_func(mailing=mailing, status='message was sent', response=response)

    mailing.status = 'completed'
    mailing.save()
