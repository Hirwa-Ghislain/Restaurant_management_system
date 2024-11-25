from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
class Customer(AbstractUser):

    phone = models.CharField(max_length=15)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',
        blank=True,
    )
    def __str__(self):
        return self.username
    class Meta:
        db_table = "customers"