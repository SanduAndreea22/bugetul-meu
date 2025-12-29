# finance/models.py
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    TYPE_CHOICES = (
        ("income", "Venit"),
        ("expense", "Cheltuială"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name

class Income(models.Model):
    SOURCE_CHOICES = [
        ("manual", "Manual"),
        ("recurring", "Recurring"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT
    )
    date = models.DateField()

    source = models.CharField(
        max_length=10,
        choices=SOURCE_CHOICES,
        default="manual"
    )

    recurring = models.ForeignKey(
        "RecurringTransaction",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="generated_incomes"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"+{self.amount} {self.category}"


class Expense(models.Model):
    SOURCE_CHOICES = [
        ("manual", "Manual"),
        ("recurring", "Recurring"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT
    )
    date = models.DateField()

    source = models.CharField(
        max_length=10,
        choices=SOURCE_CHOICES,
        default="manual"
    )

    recurring = models.ForeignKey(
        "RecurringTransaction",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="generated_expenses"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"-{self.amount} {self.category}"

class RecurringTransaction(models.Model):
    TYPE_CHOICES = [
        ("income", "Income"),
        ("expense", "Expense"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT
    )

    day_of_month = models.PositiveSmallIntegerField(
        help_text="Ziua din lună (1–28)"
    )

    active = models.BooleanField(default=True)

    last_generated = models.DateField(
        null=True,
        blank=True,
        help_text="Ultima lună în care a fost generată"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_display()} recurent – {self.amount}"


class MonthlyBudget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        limit_choices_to={"type": "expense"}
    )
    month = models.DateField(help_text="Prima zi a lunii")
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ("user", "category", "month")
