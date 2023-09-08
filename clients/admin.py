from django.contrib import admin

from clients.models import Author, VerificationToken

admin.site.register(Author)

admin.site.register(VerificationToken)


