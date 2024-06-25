from django.urls import path
from .views import home_login_page, show_departamentos


app_name = "pages"
urlpatterns = [
    path("", home_login_page, name="home_login"),
    path("departamentos", show_departamentos, name="departamentos"),
]
