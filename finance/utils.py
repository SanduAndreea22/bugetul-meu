from django.utils.timezone import now
from .models import RecurringTransaction, Income, Expense


def generate_recurring_transactions(user):
    today = now().date()

    recurrings = RecurringTransaction.objects.filter(
        user=user,
        active=True,
        day_of_month=today.day
    )

    for r in recurrings:
        # prevenim dublarea în aceeași lună
        if r.last_generated and r.last_generated.month == today.month:
            continue

        if r.type == "income":
            Income.objects.create(
                user=user,
                amount=r.amount,
                category=r.category,
                date=today,
                source="recurring",
                recurring=r      # 🔥 CHEIA
            )
        else:
            Expense.objects.create(
                user=user,
                amount=r.amount,
                category=r.category,
                date=today,
                source="recurring",
                recurring=r      # 🔥 CHEIA
            )

        r.last_generated = today
        r.save()
