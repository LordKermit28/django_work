from django import forms
from tempus_dominus.widgets import DateTimePicker
from mailing.models import Mailing, Message, Client


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('name', 'send_time', 'frequency', 'messages', 'clients', )
        widgets = {
            'send_time': DateTimePicker(
                options={
                    'format': 'YYYY-MM-DD HH:mm',
                    'sideBySide': True,
                },
                attrs={
                    'placeholder': 'Введите формат даты и времени: ГГГГ-ММ-ДД ЧЧ:мм',
                }
            )
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('subject', 'body', )


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('email', 'full_name', 'comment', )