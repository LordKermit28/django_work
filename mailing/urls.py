from django.urls import path

from mailing.views import index, MailingCreateView, MessageCreateView, MailingListView, MailingDeleteView, \
    MailingUpdateView, MessageListView, MessageDeleteView, MessageUpdateView, ClientCreateView, ClientListView, \
    ClientDeleteView, ClientUpdateView, start_mailing, stop_mailing

urlpatterns = [
    path('', index, name='index'),
    path('create_mailing/', MailingCreateView.as_view(), name='create_mailing'),
    path('list_mailing/', MailingListView.as_view(), name='list_mailing'),
    path('delete_mailing/<int:pk>/', MailingDeleteView.as_view(), name='delete_mailing'),
    path('edit_mailing/<int:pk>/', MailingUpdateView.as_view(), name='edit_mailing'),
    path('create_message/', MessageCreateView.as_view(), name='create_message'),
    path('list_message/', MessageListView.as_view(), name='list_message'),
    path('delete_message/<int:pk>/', MessageDeleteView.as_view(), name='delete_message'),
    path('edit_message/<int:pk>/', MessageUpdateView.as_view(), name='edit_message'),
    path('create_client/', ClientCreateView.as_view(), name='create_client'),
    path('list_client/', ClientListView.as_view(), name='list_client'),
    path('delete_client/<int:pk>/', ClientDeleteView.as_view(), name='delete_client'),
    path('edit_client/<int:pk>/', ClientUpdateView.as_view(), name='edit_client'),
    path('start_mailing/<int:pk>/', start_mailing, name='start_mailing'),
    path('stop_mailing/<int:pk>/', stop_mailing, name='stop_mailing'),
]
