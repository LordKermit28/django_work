from django.utils import timezone

from mailing.models import MailingLog


def logging_func(mailing, status, HttpResponse):
    log = MailingLog(
        mailing=mailing,
        timestamp=timezone.now(),
        status=status,
        server_response=HttpResponse
    )
    log.save()

