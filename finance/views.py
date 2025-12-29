from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from .forms import (
    RegisterForm,
    LoginForm,
    IncomeForm,
    ExpenseForm,
    RecurringTransactionForm,
)
from .models import Income, Expense, RecurringTransaction
from .services.recurring import generate_recurring_transactions


# ======================
# PUBLIC
# ======================

def home(request):
    return render(request, "finance/home.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("finance:dashboard")

    form = LoginForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("finance:dashboard")

    return render(request, "finance/login.html", {"form": form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("finance:dashboard")

    form = RegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("finance:dashboard")

    return render(request, "finance/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("finance:home")


# ======================
# DASHBOARD
# ======================

@login_required
def dashboard(request):
    # generează tranzacții recurente
    generate_recurring_transactions(request.user)

    total_income = (
        Income.objects.filter(user=request.user)
        .aggregate(total=Sum("amount"))["total"] or 0
    )

    total_expense = (
        Expense.objects.filter(user=request.user)
        .aggregate(total=Sum("amount"))["total"] or 0
    )

    balance = total_income - total_expense

    return render(request, "finance/dashboard.html", {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
    })


# ======================
# ADD TRANSACTIONS
# ======================
@login_required
def add_income(request):
    form = IncomeForm(
        request.POST or None,
        user=request.user
    )

    if form.is_valid():
        income = form.save(commit=False)
        income.user = request.user
        income.source = "manual"
        income.save()
        return redirect("finance:dashboard")

    return render(request, "finance/add_income.html", {"form": form})

@login_required
def add_expense(request):
    form = ExpenseForm(
        request.POST or None,
        user=request.user
    )

    if form.is_valid():
        expense = form.save(commit=False)
        expense.user = request.user
        expense.source = "manual"
        expense.save()
        return redirect("finance:dashboard")

    return render(request, "finance/add_expense.html", {"form": form})

@login_required
def add_recurring(request):
    form = RecurringTransactionForm(
        request.POST or None,
        user=request.user
    )

    if form.is_valid():
        recurring = form.save(commit=False)
        recurring.user = request.user
        recurring.save()
        return redirect("finance:recurring_list")

    return render(request, "finance/recurring_form.html", {
        "form": form,
        "title": "Adaugă recurent"
    })

# ======================
# HISTORY
# ======================
@login_required
def transaction_history(request):
    filter_type = request.GET.get("type", "all")

    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)

    transactions = []

    # INCOME
    if filter_type in ["all", "income"]:
        for i in incomes:
            if filter_type == "income" or filter_type == "all":
                transactions.append({
                    "type": "income",
                    "obj": i,
                    "date": i.date,
                    "source": i.source,
                })

    # EXPENSE
    if filter_type in ["all", "expense"]:
        for e in expenses:
            if filter_type == "expense" or filter_type == "all":
                transactions.append({
                    "type": "expense",
                    "obj": e,
                    "date": e.date,
                    "source": e.source,
                })

    # RECURRING (din ambele)
    if filter_type == "recurring":
        for i in incomes.filter(source="recurring"):
            transactions.append({
                "type": "income",
                "obj": i,
                "date": i.date,
                "source": i.source,
            })

        for e in expenses.filter(source="recurring"):
            transactions.append({
                "type": "expense",
                "obj": e,
                "date": e.date,
                "source": e.source,
            })

    transactions.sort(key=lambda x: x["date"], reverse=True)

    return render(request, "finance/history.html", {
        "transactions": transactions,
        "filter_type": filter_type,
    })

# ======================
# EDIT / DELETE TRANSACTIONS
# ======================

@login_required
def edit_income(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    form = IncomeForm(request.POST or None, instance=income)

    if form.is_valid():
        form.save()
        return redirect("finance:history")

    return render(request, "finance/edit_transaction.html", {
        "form": form,
        "title": "Editează Venit"
    })


@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    form = ExpenseForm(request.POST or None, instance=expense)

    if form.is_valid():
        form.save()
        return redirect("finance:history")

    return render(request, "finance/edit_transaction.html", {
        "form": form,
        "title": "Editează Cheltuială"
    })


@login_required
def delete_income(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    income.delete()
    return redirect("finance:history")


@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    expense.delete()
    return redirect("finance:history")


# ======================
# RECURRING
# ======================

@login_required
def recurring_list(request):
    recurrings = RecurringTransaction.objects.filter(
        user=request.user
    ).order_by("day_of_month")

    return render(request, "finance/recurring_list.html", {
        "recurrings": recurrings
    })

@login_required
def edit_recurring(request, pk):
    recurring = get_object_or_404(
        RecurringTransaction,
        pk=pk,
        user=request.user
    )

    form = RecurringTransactionForm(
        request.POST or None,
        instance=recurring
    )

    if form.is_valid():
        form.save()
        return redirect("finance:recurring_list")

    return render(request, "finance/recurring_form.html", {
        "form": form,
        "title": "Editează recurent"
    })



@login_required
def delete_recurring(request, pk):
    recurring = get_object_or_404(
        RecurringTransaction,
        pk=pk,
        user=request.user
    )
    recurring.delete()
    return redirect("finance:recurring_list")
