from django.contrib import admin

from mailing.models import Mailing, Message, Client, MailingLog

admin.site.register(Mailing)
admin.site.register(Message)
admin.site.register(Client)
admin.site.register(MailingLog)

