from django.urls import path
from .views import like_change

#http://localhost:8000/like/
urlpatterns = [
    path('like_change', like_change, name='like_change'),
]