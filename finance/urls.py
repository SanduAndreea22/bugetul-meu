from django.urls import path
from . import views

app_name = "finance"

urlpatterns = [
    # public
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),

    # private
    path("dashboard/", views.dashboard, name="dashboard"),
    path("venituri/", views.venituri, name="venituri"),
    path("cheltuieli/", views.cheltuieli, name="cheltuieli"),
    path("diagrame/", views.diagrame, name="diagrame"),
]
