from django.urls import path,include
from .views import update_comment

#http://localhost:8000/comment/
urlpatterns = [
    path('update_comment',update_comment,name='update_comment'),
]