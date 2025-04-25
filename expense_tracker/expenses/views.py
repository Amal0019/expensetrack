import calendar
from django.shortcuts import render, redirect
from .forms import ExpenseForm 
from .models import Expense, Category
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
import json
from decimal import Decimal  # Import Decimal for serialization

# View to display home page
def home(request):
    # Get all expenses ordered by date
    expenses = Expense.objects.all().order_by('-date')

    # Get expected expenses for next month
    expected_expenses = get_expected_expenses()

    # Prepare chart data
    chart_data = prepare_chart_data()  # Get data for the chart

    # No need to call decimal_to_float here anymore, we handle it in prepare_chart_data()

    # Send chart data as JSON to be used in JS
    return render(request, 'home.html', {
        'expenses': expenses,
        'expected_expenses': expected_expenses,
        'chart_data': json.dumps(chart_data),  # Send chart data as JSON
    })



def add_expense(request):
    if request.method == 'POST':
         form = ExpenseForm(request.POST)
         if form.is_valid():
             form.save()
             # Redirect to the home page after saving the expense
             return redirect('home')
    else:
         form = ExpenseForm()
    return render(request, 'exp/add_expense.html', {'form':form})  # Correct path to the template

# from .forms import ExpenseForm

# def add_expense(request):
#     if request.method == 'POST':
#         form = ExpenseForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # Redirect to the home page after saving the expense
#             return redirect('home')
#     else:
#         form = ExpenseForm()

#     return render(request, 'add_expense.html', {'form': form})


# Get expected expenses for the next month based on last month's data
def get_expected_expenses():
    today = timezone.now()

    # Get the first and last day of the previous month
    first_day_of_last_month = today.replace(day=1) - timedelta(days=1)
    first_day_of_last_month = first_day_of_last_month.replace(day=1)
    
    last_day_of_last_month = today.replace(day=1) - timedelta(days=1)
    
    # Get expenses from last month
    last_month_expenses = Expense.objects.filter(date__gte=first_day_of_last_month, date__lte=last_day_of_last_month)
    
    # Group expenses by category and calculate total amount
    category_expenses = last_month_expenses.values('category').annotate(total_amount=Sum('amount'))
    
    # Use a single query to get all categories we will reference
    categories_dict = {category.id: category for category in Category.objects.filter(id__in=[ce['category'] for ce in category_expenses])}
    
    projected_expenses = []
    for category_expense in category_expenses:
        category = categories_dict[category_expense['category']]  # Get the category from the preloaded dictionary

        # Assuming the average expense of last month is the expected expense for next month
        avg_expense = float(category_expense['total_amount'])  # Convert Decimal to float
        projected_expenses.append({
            'category': category.name,
            'expected_expense': avg_expense,
        })

    return projected_expenses

# Prepare chart data for visualization
def prepare_chart_data():
    # Get all expenses (or filter as necessary)
    expenses = Expense.objects.all()

    # Prepare chart data
    labels = []
    actual_expenses = []
    expected_expenses_list = []

    # Prepare actual and expected expenses for each category
    for expense in expenses:
        category = expense.category.name
        if category not in labels:
            labels.append(category)
            actual_expenses.append(0)
            expected_expenses_list.append(0)

        category_index = labels.index(category)
        actual_expenses[category_index] += float(expense.amount)  # Convert Decimal to float

    # Assuming expected_expenses are calculated or fetched elsewhere
    # Here we mock this data for the sake of the example
    for i, label in enumerate(labels):
        expected_expenses_list[i] = 200  # Mocked expected expense for each category

    # Prepare chart data in the format expected by the template
    chart_data = {
        'labels': labels,
        'actual_expenses': actual_expenses,
        'expected_expenses': expected_expenses_list
    }

    return chart_data
