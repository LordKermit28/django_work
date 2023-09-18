from django.db import models

from clients.models import Author

class Message(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()
    def __str__(self):
        return f"Тема:{self.subject}\nПисьмо:{self.body}"

class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name="email")
    full_name = models.CharField(max_length=100)
    comment = models.TextField()

class Mailing(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='name')
    send_time = models.DateTimeField()

    frequency = models.CharField(max_length=2, choices=[
        ('1', 'Раз в день'),
        ('7', 'Раз в неделю'),
        ('30', 'Раз в месяц'),
    ])

    status = models.CharField(choices=[

        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
        ],
        max_length=50)
    clients = models.ManyToManyField(Client)
    messages = models.ManyToManyField(Message)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


class MailingLog(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=200)
    server_response = models.TextField(null=True, blank=True)




