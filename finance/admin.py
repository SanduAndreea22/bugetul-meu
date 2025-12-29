from django.contrib import admin
from .models import Category, Income, Expense, RecurringTransaction, MonthlyBudget


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "user")
    list_filter = ("type",)
    search_fields = ("name",)


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ("amount", "category", "date", "user", "source")
    list_filter = ("source", "date")


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("amount", "category", "date", "user", "source")
    list_filter = ("source", "date")


@admin.register(RecurringTransaction)
class RecurringTransactionAdmin(admin.ModelAdmin):
    list_display = ("type", "category", "amount", "day_of_month", "user", "active")
    list_filter = ("type", "active")


@admin.register(MonthlyBudget)
class MonthlyBudgetAdmin(admin.ModelAdmin):
    list_display = ("month", "amount", "user")
