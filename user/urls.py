from django.urls import path
from .views import log_in,log_in_for_modal,log_out,register,user_info

#http://localhost:8000/user/
urlpatterns = [
    path('login/',log_in,name='login'),
    path('login_for_modal/',log_in_for_modal,name='login_for_modal'),
    path('logout/',log_out,name='logout'),
    path('register/',register,name='register'),
    path('user_info/',user_info,name='user_info'),
]