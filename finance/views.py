from django.shortcuts import render, redirect
from django.contrib.auth import logout


# ===== PUBLIC =====

def home(request):
    return render(request, "finance/home.html")


from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import RegisterForm, LoginForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect("finance:dashboard")

    form = LoginForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("finance:home")

    return render(request, "finance/login.html", {"form": form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("finance:home")

    form = RegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("finance:home")

    return render(request, "finance/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("finance:home")



# ===== PRIVATE (deocamdată fără protecție) =====

def dashboard(request):
    return render(request, "finance/dashboard.html")


def venituri(request):
    return render(request, "finance/venituri.html")


def cheltuieli(request):
    return render(request, "finance/cheltuieli.html")


def diagrame(request):
    return render(request, "finance/diagrame.html")
