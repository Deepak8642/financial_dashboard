from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages 
from django.contrib.auth.models import User  # Import User model 
from .models import Expense 
from datetime import datetime, timedelta
def calculate_time(request):
    if request.method == 'POST':
        data = request.POST
        salary = int(data.get('salary', 0))
        targeted_item_cost = int(data.get('targeted_item_cost', 0))

        # Calculate total expenses
        expenses = Expense.objects.filter(user=request.user)
        total_expenses = sum(expense.price for expense in expenses)

        # Ensure salary is enough to cover expenses and targeted item cost
        if salary <= total_expenses:
            return render(request, 'time_required.html', {'time_required': 'Infinity'})  # Salary is not enough

        # Calculate time required
        remaining_amount = targeted_item_cost - (salary - total_expenses)
        time_required = remaining_amount / salary  # Assuming monthly salary

        return render(request, 'time_required.html', {'time_required': time_required})

    return render(request, 'calculate_time.html')
# Create Expense page 
@login_required(login_url='/login/')
def salary(request): 
    user = request.user
    if request.method == 'POST':
        data = request.POST 
        salary = int(data.get('salary', 0)) 
        goal_cost = int(data.get('goal_cost', 0))
        
        # Calculate time required to reach goal
        if salary > 0:
            months_to_goal = goal_cost / salary
            years_to_goal = int(months_to_goal // 12)
            months_remaining = int(months_to_goal % 12)
            completion_date = datetime.now() + timedelta(days=30*int(months_to_goal))
        else:
            years_to_goal = 0
            months_remaining = 0
            completion_date = None

        # Render the template with calculated data
        context = {
            'years_to_goal': years_to_goal,
            'months_remaining': months_remaining,
            'completion_date': completion_date,
        }
        return render(request, 'salary.html', context)

    return render(request, 'salary.html')

@login_required(login_url='/login/') 
def expenses(request): 
    salary = 0 
    if request.method == 'POST': 
        data = request.POST 
        salary = int(data.get('salary', 0)) 
        name = data.get('name') 
        price = int(data.get('price', 0)) 
  
        Expense.objects.create( 
            salary=salary, 
            name=name, 
            price=price, 
        ) 
        return redirect('/') 
  
    queryset = Expense.objects.all() 
    if request.GET.get('search'): 
        queryset = queryset.filter( 
            name__icontains=request.GET.get('search')) 
  
    # Calculate the total sum 
    total_sum = sum(expense.price for expense in queryset) 
      
    context = {'expenses': queryset, 'total_sum': total_sum} 
    return render(request, 'expenses.html', context) 
  
  
# Update the Expenses data 
@login_required(login_url='/login/') 
def update_expense(request, id): 
    queryset = Expense.objects.get(id=id) 
  
    if request.method == 'POST': 
        data = request.POST 
        name = data.get('name') 
        price = int(data.get('price', 0)) 
  
        queryset.name = name 
        queryset.price = price 
        queryset.save() 
        return redirect('/') 
  
    context = {'expense': queryset} 
    return render(request, 'update_expense.html', context) 
def time_required(request):
    # Calculate time required logic here
    goal_completion_date = datetime.now() + timedelta(days=365)  # Example: Goal completion in 1 year

    # Pass the goal_completion_date to the template
    context = {'goal_completion_date': goal_completion_date}
    return render(request, 'time_required.html', context) 
# Delete the Expenses data 
@login_required(login_url='/login/') 
def delete_expense(request, id): 
    queryset = Expense.objects.get(id=id) 
    queryset.delete() 
    return redirect('/') 
  
# Login page for user 
def login_page(request): 
    if request.method == "POST": 
        try: 
            username = request.POST.get('username') 
            password = request.POST.get('password') 
            user_obj = User.objects.filter(username=username).first() 
            if not user_obj: 
                messages.error(request, "Username not found") 
                return redirect('/login/') 
            user_auth = authenticate(username=username, password=password) 
            if user_auth: 
                login(request, user_auth) 
                return redirect('expenses') 
            messages.error(request, "Wrong Password") 
            return redirect('/login/') 
        except Exception as e: 
            messages.error(request, "Something went wrong") 
            return redirect('/register/') 
    return render(request, "login.html") 
  
# Register page for user 
def register_page(request): 
    if request.method == "POST": 
        try: 
            username = request.POST.get('username') 
            password = request.POST.get('password') 
            user_obj = User.objects.filter(username=username) 
            if user_obj.exists(): 
                messages.error(request, "Username is taken") 
                return redirect('/register/') 
            user_obj = User.objects.create(username=username) 
            user_obj.set_password(password) 
            user_obj.save() 
            messages.success(request, "Account created") 
            return redirect('/login') 
        except Exception as e: 
            messages.error(request, "Something went wrong") 
            return redirect('/register') 
    return render(request, "register.html") 
  
# Logout function 
def custom_logout(request): 
    logout(request) 
    return redirect('login') 
  
# Generate the Bill 
@login_required(login_url='/login/') 
def pdf(request): 
    if request.method == 'POST': 
        data = request.POST 
        salary = int(data.get('salary')) 
        name = data.get('name') 
        price = int(data.get('price', 0)) 
  
        Expense.objects.create( 
            salary=salary, 
            name=name, 
            price=price, 
        ) 
        return redirect('pdf') 
  
    queryset = Expense.objects.all() 
    if request.GET.get('search'): 
        queryset = queryset.filter( 
            name__icontains=request.GET.get('search')) 
  
    # Calculate the total sum 
    total_sum = sum(expense.price for expense in queryset) 
    # Get the username 
    username = request.user.username 
  
    context = {'expenses': queryset, 'total_sum': total_sum, 'username':username} 
    return render(request, 'pdf.html', context) 