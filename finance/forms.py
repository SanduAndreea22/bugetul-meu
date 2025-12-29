from .models import Income, Expense, RecurringTransaction, Category
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email",)

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Există deja un cont cu acest email.")
        return email

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password1") != cleaned.get("password2"):
            raise forms.ValidationError("Parolele nu coincid.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput)


from django.utils.timezone import now
class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ["amount", "category", "date"]
        widgets = {
            "amount": forms.NumberInput(attrs={"placeholder": "Sumă (RON)"}),
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields["category"].queryset = Category.objects.filter(
                user=user,
                type="income"
            )

from django import forms
from django.utils.timezone import now
from .models import Expense

from django import forms
from django.utils.timezone import now
from .models import Expense, Category


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["amount", "category", "date"]
        widgets = {
            "amount": forms.NumberInput(attrs={"placeholder": "Sumă (RON)"}),
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields["category"].queryset = Category.objects.filter(
                user=user,
                type="expense"
            )

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0:
            raise forms.ValidationError("Suma trebuie să fie pozitivă.")
        return amount

    def clean_date(self):
        return self.cleaned_data.get("date") or now().date()

from django import forms
from .models import RecurringTransaction, Category


class RecurringTransactionForm(forms.ModelForm):
    class Meta:
        model = RecurringTransaction
        fields = ["type", "category", "amount", "day_of_month"]
        widgets = {
            "type": forms.Select(),
            "amount": forms.NumberInput(attrs={"placeholder": "Sumă (RON)"}),
            "day_of_month": forms.NumberInput(attrs={
                "min": 1,
                "max": 28
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields["category"].queryset = Category.objects.filter(
                user=user
            )

            # dacă editezi sau ai POST
            tx_type = (
                self.data.get("type")
                or self.initial.get("type")
            )

            if tx_type in ["income", "expense"]:
                self.fields["category"].queryset = Category.objects.filter(
                    user=user,
                    type=tx_type
                )

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0:
            raise forms.ValidationError("Suma trebuie să fie pozitivă.")
        return amount

    def clean_day_of_month(self):
        day = self.cleaned_data["day_of_month"]
        if day < 1 or day > 28:
            raise forms.ValidationError("Ziua trebuie să fie între 1 și 28.")
        return day


