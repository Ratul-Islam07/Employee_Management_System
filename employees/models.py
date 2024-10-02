from django.db import models
from django.core.validators import RegexValidator

class Employee(models.Model):
    # Validator to ensure phone number contains only digits and has 10-15 characters
    phone_number_validator = RegexValidator(
        regex=r'^\d{10,15}$', 
        message="Phone number must be between 10 and 15 digits and contain only numbers."
    )

    name = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.CharField(
        max_length=15, 
        unique=True, 
        validators=[phone_number_validator]
    )
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    designation = models.CharField(max_length=100)
    short_description = models.TextField()

    def __str__(self):
        return self.name
