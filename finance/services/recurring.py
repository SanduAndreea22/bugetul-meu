from django.utils.timezone import now
from finance.models import RecurringTransaction, Income, Expense


def generate_recurring_transactions(user):
    today = now().date()
    current_month_start = today.replace(day=1)

    recurrings = RecurringTransaction.objects.filter(
        user=user,
        active=True
    )

    for r in recurrings:
        # 1️⃣ deja generat luna asta → skip
        if r.last_generated and r.last_generated >= current_month_start:
            continue

        # 2️⃣ nu a venit încă ziua din lună
        if today.day < r.day_of_month:
            continue

        # 3️⃣ creează tranzacția
        if r.type == "income":
            Income.objects.create(
                user=user,
                amount=r.amount,
                category=r.category,
                date=today,
                source="recurring"
            )
        else:
            Expense.objects.create(
                user=user,
                amount=r.amount,
                category=r.category,
                date=today,
                source="recurring"
            )

        # 4️⃣ marchează ca generat
        r.last_generated = today
        r.save(update_fields=["last_generated"])
