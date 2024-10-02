from django.shortcuts import render, redirect
from .forms import EmployeeForm
from django.shortcuts import get_object_or_404
from .models import Employee

def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EmployeeForm()
    return render(request, 'add_employee.html', {'form': form})

def update(request):
    employees = Employee.objects.all()
    return render(request, 'update_page.html', {'employees': employees})

def update_employee(request, pk):
    employee = Employee.objects.get(pk=pk)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to home after updating
    else:
        form = EmployeeForm(instance=employee)  # Editing an existing instance
    return render(request, 'update_employee.html', {'form': form, 'employee': employee})

def delete(request):
    employees = Employee.objects.all()
    return render(request, 'delete_page.html', {'employees': employees})

def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('home')
    return render(request, 'delete_employee.html', {'employee': employee})

def home(request):
    employees = Employee.objects.all()    # Retrieve all employees from the database
    return render(request, 'home.html', {'employees': employees})    # Render the home template, passing the employees as context

def profile(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'profile_page.html', {'employee': employee})    # Render the home template, passing the employees as context

