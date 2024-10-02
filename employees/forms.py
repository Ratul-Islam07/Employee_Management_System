from django import forms
from .models import Employee

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
        super(EmployeeForm, self).__init__(*args, **kwargs)
        # If the form is being used to update an existing employee, disable salary and designation fields
        if self.instance.pk:
            self.fields['salary'].disabled = True
            self.fields['designation'].disabled = True
