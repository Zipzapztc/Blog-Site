from django.urls import path,include
from .views import update_comment

urlpatterns = [
    path('update_comment',update_comment,name='update_comment'),
]