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
    path("add-income/", views.add_income, name="add_income"),
    path("add-expense/", views.add_expense, name="add_expense"),
    path("add-recurring/", views.add_recurring, name="add_recurring"),

    path("istoric/", views.transaction_history, name="history"),

    path("income/<int:pk>/edit/", views.edit_income, name="edit_income"),
    path("expense/<int:pk>/edit/", views.edit_expense, name="edit_expense"),
    path("income/<int:pk>/delete/", views.delete_income, name="delete_income"),
    path("expense/<int:pk>/delete/", views.delete_expense, name="delete_expense"),

    # recurente
    path("recurente/", views.recurring_list, name="recurring_list"),
    path("recurente/edit/<int:pk>/", views.edit_recurring, name="edit_recurring"),
    path("recurente/delete/<int:pk>/", views.delete_recurring, name="delete_recurring"),
]


