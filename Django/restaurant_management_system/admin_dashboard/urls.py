from django.urls import path
from .views import  admin_dashboard, admin_logout, add_staff_member,view_staff, edit_staff_member,delete_staff_memebr

urlpatterns = [
    path('', admin_dashboard, name='admin_dashboard'),
    path('logout/', admin_logout, name='admin_logout'),
    path('add-staff/', add_staff_member, name='add_staff_member'),
    path('view/',view_staff, name='view_staff'),
    path('edit/<int:staff_id>/',edit_staff_member, name='edit_staff'),
    path('delete/<int:staff_id>/', delete_staff_memebr, name='delete_staff'),
]
