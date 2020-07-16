from django.urls import path,include
from .views import like_change

urlpatterns = [
    path('like_change',like_change,name='like_change'),
]