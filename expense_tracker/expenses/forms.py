# forms.py
from django import forms
from .models import Expense  # Import the Expense model

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense  # Associate the form with the Expense model
        fields = ['name', 'amount', 'category', 'description', 'date']  # List the fields you want in the form

