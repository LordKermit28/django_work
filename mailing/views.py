from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
import time
from clients.models import Author
from config import settings
from mailing.forms import MailingForm, MessageForm, ClientForm
from mailing.models import Mailing, Message, Client


def index(request):
    author = Author.objects.first()
    return render(request, 'mailing/index.html', {'author': author})

@method_decorator(login_required, name='dispatch')
class MailingCreateView(CreateView, UserPassesTestMixin):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('list_mailing')

    def test_func(self):
        return self.request.author.is_authenticated

    def form_valid(self, form):
        form.instance.status = 'created'
        form.instance.author = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class MailingUpdateView(UserPassesTestMixin, UpdateView):
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

@method_decorator(login_required, name='dispatch')
class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('list_mailing')


@method_decorator(login_required, name='dispatch')
def start_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)

    if mailing.send_time > timezone.now():
        mailing.status = 'started'
        mailing.save()

        clients = Client.objects.all()
        messages = Message.objects.filter(mailing=mailing)

        while mailing.status != 'completed':
            for client in clients:
                for message in messages:
                    send_mail(
                        subject=message.subject,
                        message=message.body,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[client.email],
                    )
                    time.sleep(int(mailing.frequency) * 60)

            mailing.refresh_from_db()

        return HttpResponseRedirect(reverse('list_mailing'))

@method_decorator(login_required, name='dispatch')
def stop_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if mailing.status == 'started':
        mailing.status = 'completed'
        mailing.save()

    return redirect("list_mailing")

class MessageCreateView(UserPassesTestMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('list_message')


class MessageUpdateView(UserPassesTestMixin, UpdateView):
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

@method_decorator(login_required, name='dispatch')
class MessageListView(ListView):
    model = Message

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

@method_decorator(login_required, name='dispatch')
class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('list_message')


class ClientCreateView(UserPassesTestMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('list_client')



class ClientUpdateView(UserPassesTestMixin, UpdateView):
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

@method_decorator(login_required, name='dispatch')
class ClientListView(ListView):
    model = Client
    template_name = 'mailing/list_client.html'

@method_decorator(login_required, name='dispatch')
class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('list_client')