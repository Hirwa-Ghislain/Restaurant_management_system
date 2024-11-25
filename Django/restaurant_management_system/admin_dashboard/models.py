from django.db import models


class StaffMember(models.Model):
    ROLE_CHOICES = [
        ('waiter', 'Waiter'),
        ('chef', 'Chef'),
        ('manager', 'Manager'),
        ('cleaner','Cleaner'),
        ('receptionist','Receptionist')
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role}"
    
    class Meta:
        db_table = "staff_members"
