from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from notifications.models import Notification


def my_notifications(request):
    context = {}
    return render(request, 'my_notifications.html', context)


def notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.unread = False
    notification.save()
    return redirect(notification.data['url'])


def delete_all_read_notifications(request):
    notifications = request.user.notifications.read()
    notifications.delete()
    return redirect(reverse('my_notifications'))