from django.urls import path
from .views import home_login_page



urlpatterns = [
    path("", home_login_page, name="home_login" )
]
