from django.shortcuts import render, redirect
from .forms import EmployeeForm, CreateUserForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import Employee
from .decorators import unauthenticated_user, admin_only


@unauthenticated_user
def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            group = Group.objects.get(name='customer')
            user.groups.add(group)

            return redirect('login')  # Redirect to login after registering
            

    return render(request, 'registerPage.html', {'form': form})


@unauthenticated_user
def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            print(f'User {user.username} is in group: {user.groups.all()}')  # Print group info for debugging
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'loginPage.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login after logging out

@login_required(login_url = 'login')
@admin_only
def home(request):
    employees = Employee.objects.all()    # Retrieve all employees from the database
    return render(request, 'home.html', {'employees': employees})    # Render the home template, passing the employees as context

@login_required(login_url = 'login')
def profile(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'profile_page.html', {'employee': employee})    # Render the home template, passing the employees as context

def user_page(request):
    employees = Employee.objects.all()
    return render(request, 'user.html', {'employees': employees})  # Render the user page template, passing the user as context


@login_required(login_url = 'login')
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EmployeeForm()
    return render(request, 'add_employee.html', {'form': form})

@login_required(login_url = 'login')
def update(request):
    employees = Employee.objects.all()
    return render(request, 'update_page.html', {'employees': employees})


@login_required(login_url='login')
def update_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)  # Safer way to get the employee
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee, user=request.user)  # Pass the user
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to home after updating
    else:
        form = EmployeeForm(instance=employee, user=request.user)  # Pass the user for initial form
        
    return render(request, 'update_employee.html', {'form': form, 'employee': employee})


@login_required(login_url = 'login')
def delete(request):
    employees = Employee.objects.all()
    return render(request, 'delete_page.html', {'employees': employees})

@login_required(login_url = 'login')
def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('home')
    return render(request, 'delete_employee.html', {'employee': employee})

