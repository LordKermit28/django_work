import string
import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from clients.forms import AuthorRegisterForm, AuthorProfileForm
from clients.models import Author, VerificationToken
from config import settings


class RegisterView(CreateView):
    model = Author
    form_class = AuthorRegisterForm
    template_name = 'clients/register.html'
    success_url = reverse_lazy('clients:email_check_message')

    def generate_random_password(self):
        length = 12
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return password

    def form_valid(self, form):

        author = form.save()

        token = default_token_generator.make_token(author)
        token_object = VerificationToken(user=author, token=token)
        token_object.save()
        verify_url = self.request.build_absolute_uri(reverse_lazy('clients:verify_email', kwargs={'token': token}))

        send_mail(
            subject='Подтвердите ваш адрес электронной почты',
            message=f'Привет! Пожалуйста, подтвердите свою электронную почту, перейдя по ссылке: {verify_url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[author.email],
        )
        return super().form_valid(form)



class VerifyEmailView(TemplateView):
    def get(self, request, *args, **kwargs):
        token = self.kwargs['token']
        verified_token = get_object_or_404(VerificationToken, token=token)

        if verified_token.is_active:
            author = verified_token.user
            author.is_active = True
            author.save()

            verified_token.is_active = False
            verified_token.save()

            return redirect('clients:login')
        return redirect('clients:invalid_token')


class ProfileView(LoginRequiredMixin, UpdateView):
    model = Author
    form_class = AuthorProfileForm
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        return self.request.user


def message_view(request):
    return render(request, 'clients/email_check_message.html')

def invalid_token_view(request):
    return render(request, 'clients/invalid_token.html')


