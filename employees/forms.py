from django import forms
from .models import Employee

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'address', 'phone_number', 'salary', 'designation', 'short_description']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit():
            raise forms.ValidationError('Phone number must contain only digits.')
        if len(phone_number) < 10 or len(phone_number) > 15:
            raise forms.ValidationError('Phone number must be between 10 and 15 digits.')
        return phone_number

    def clean_salary(self):
        salary = self.cleaned_data.get('salary')
        if salary <= 0:
            raise forms.ValidationError('Salary must be a positive value.')
        return salary

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from the kwargs
        super(EmployeeForm, self).__init__(*args, **kwargs)
        
        # If the form is being used to update an existing employee
        if self.instance.pk:
            # Allow admin or superuser to update salary and designation
            if not user or not user.is_superuser:
                self.fields['salary'].disabled = True
                self.fields['designation'].disabled = True

# In your view, make sure to pass the request.user to the form
# Example:
# form = EmployeeForm(instance=employee_instance, user=request.user)

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

