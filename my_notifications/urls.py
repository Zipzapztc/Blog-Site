from django.urls import path,include
from .views import my_notifications,notification,delete_all_read_notifications

#http://localhost:8000/my_notifications/
urlpatterns = [
    path('', my_notifications, name='my_notifications'),
    path('notification/<int:notification_id>', notification, name='notification'),
    path('delete_all_read_notifications', delete_all_read_notifications, name='delete_all_read_notifications'),

]