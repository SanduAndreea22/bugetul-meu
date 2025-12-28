from .models import Income, Expense, RecurringTransaction
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
            "category": forms.TextInput(attrs={"placeholder": "Categorie"}),
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0:
            raise forms.ValidationError("Suma trebuie să fie pozitivă.")
        return amount

    def clean_date(self):
        return self.cleaned_data.get("date") or now().date()

from django import forms
from django.utils.timezone import now
from .models import Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["amount", "category", "date"]
        widgets = {
            "amount": forms.NumberInput(attrs={
                "placeholder": "Sumă (RON)"
            }),
            "category": forms.TextInput(attrs={
                "placeholder": "Categorie (ex: Alimentație)"
            }),
            "date": forms.DateInput(attrs={
                "type": "date"
            }),
        }

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0:
            raise forms.ValidationError("Suma trebuie să fie pozitivă.")
        return amount

    def clean_date(self):
        return self.cleaned_data.get("date") or now().date()


class RecurringTransactionForm(forms.ModelForm):
    class Meta:
        model = RecurringTransaction
        fields = ["type", "amount", "category", "day_of_month"]
        widgets = {
            "type": forms.Select(),
            "amount": forms.NumberInput(attrs={"placeholder": "Sumă (RON)"}),
            "category": forms.TextInput(attrs={"placeholder": "Categorie"}),
            "day_of_month": forms.NumberInput(attrs={
                "min": 1,
                "max": 28,
                "placeholder": "Ziua din lună (1–28)"
            }),
        }

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


