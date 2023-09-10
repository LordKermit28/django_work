from random import sample
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from blog.models import Blog
from clients.models import Author
from config import settings
from mailing.forms import MailingForm, MessageForm, ClientForm
from mailing.models import Mailing, Message, Client, MailingLog
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.conf import settings
import time

from mailing.services import logging_func


def is_not_manager(user):
    return not user.groups.filter(name='manager').exists()

@cache_page(60)
def index(request):
    author = Author.objects.first()
    blogs = list(Blog.objects.all())
    if len(blogs) >= 3:
        random_blogs = sample(blogs, 3)
    else:
        random_blogs = blogs

    total_mailings = Mailing.objects.count()

    active_mailings = Mailing.objects.filter(status='started').count()

    unique_clients = Client.objects.values('email').distinct().count()

    return render(request, 'mailing/index.html', {
        'author': author,
        'blogs': random_blogs,
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_clients': unique_clients,
    })

@method_decorator(user_passes_test(is_not_manager), name='dispatch')
class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('list_mailing')

    def test_func(self):
        return self.request.author.is_authenticated

    def form_valid(self, form):
        form.instance.status = 'created'
        form.instance.author = self.request.user
        return super().form_valid(form)

@method_decorator(user_passes_test(is_not_manager), name='dispatch')
class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('list_mailing')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['formset'] = MailingForm
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']()
        formset.data = self.request.POST
        formset.is_bound = True

        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            raise self.form_invalid(form)

@method_decorator(login_required, name='dispatch')
class MailingListView(ListView):
    model = Mailing

    def get_template_names(self):
        if self.request.user.groups.filter(name='manager').exists():
            template_name = 'for_manager/manager_mailing_list.html'
        else:
            template_name = 'mailing/mailing_list.html'
        return [template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

@method_decorator(user_passes_test(is_not_manager), name='dispatch')
class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('list_mailing')



def start_mailing(request, pk):

    mailing = get_object_or_404(Mailing, pk=pk)

    if mailing.send_time > timezone.now():

        mailing.status = 'started'
        mailing.save()

        clients = Client.objects.filter(mailing=mailing)
        messages = Message.objects.filter(mailing=mailing)

        while mailing.status != 'completed':
            for client in clients:
                for message in messages:
                    response = send_mail(
                        subject=message.subject,
                        message=message.body,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[client.email],
                    )
                    logging_func(mailing=mailing, status='send_email', HttpResponse=response)
                    time.sleep(int(mailing.frequency) * 60)

            mailing.refresh_from_db()

        return HttpResponseRedirect(reverse('list_mailing'))
    else:
        return HttpResponseRedirect(reverse('list_mailing'))


def stop_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if mailing.status == 'started':
        mailing.status = 'completed'
        mailing.save()
        logging_func(mailing=mailing, status='mailing is finished', HttpResponse=HttpResponse)

    return redirect("list_mailing")

@method_decorator(user_passes_test(is_not_manager), name='dispatch')
class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('list_message')

@method_decorator(user_passes_test(is_not_manager), name='dispatch')
class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('list_message')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['formset'] = MessageForm
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']()
        formset.data = self.request.POST
        formset.is_bound = True

        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            raise self.form_invalid(form)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_template_names(self):
        if self.request.user.groups.filter(name='manager').exists():
            template_name = 'for_manager/manager_message_list.html'
        else:
            template_name = 'mailing/message_list.html'
        return [template_name]
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

@method_decorator(user_passes_test(is_not_manager), name='dispatch')
class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('list_message')

@method_decorator(user_passes_test(is_not_manager), name='dispatch')
class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('list_client')


@method_decorator(user_passes_test(is_not_manager), name='dispatch')
class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('list_client')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.request.POST:
            context_data['formset'] = ClientForm(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = ClientForm(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'mailing/list_client.html'
    def get_template_names(self):
        if self.request.user.groups.filter(name='manager').exists():
            template_name = 'for_manager/manager_client_list.html'
        else:
            template_name = 'mailing/client_list.html'
        return [template_name]

@method_decorator(user_passes_test(is_not_manager), name='dispatch')
class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('list_client')