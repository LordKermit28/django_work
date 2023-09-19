import datetime

from django.utils import timezone
from django_cron import CronJobBase, Schedule
from dateutil import parser
from mailing.models import Mailing
from mailing.services import send_mailing


class MailingCronJob(CronJobBase):
    RUN_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'mailing.mailing_cron_job'

    def do(self):

        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        daily_mailings = Mailing.objects.filter(send_time__lte=current_time, frequency='1', status='started')
        weekly_mailings = Mailing.objects.filter(send_time__lte=current_time, frequency='7', status='started')
        monthly_mailings = Mailing.objects.filter(send_time__lte=current_time, frequency='30', status='started')

        send_mailings(daily_mailings)
        send_mailings(weekly_mailings)
        send_mailings(monthly_mailings)

def send_mailings(mailings):
    for mailing in mailings:
        send_mailing(mailing)