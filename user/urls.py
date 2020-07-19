from django.urls import path
from .views import log_in,log_in_for_modal,log_out,register,user_info,change_nickname,bind_email,send_verification_code

#http://localhost:8000/user/
urlpatterns = [
    path('login/',log_in,name='login'),
    path('login_for_modal/',log_in_for_modal,name='login_for_modal'),
    path('logout/',log_out,name='logout'),
    path('register/',register,name='register'),
    path('user_info/',user_info,name='user_info'),
    path('change_nickname/',change_nickname,name='change_nickname'),
    path('bind_email/',bind_email,name='bind_email'),
    path('send_verification_code/',send_verification_code,name='send_verification_code'),

]