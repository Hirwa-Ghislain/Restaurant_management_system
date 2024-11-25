from django.shortcuts import render, redirect
from .forms import StaffMemberForm
from django.contrib.auth import authenticate,logout
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import StaffMember
from django.shortcuts import render, redirect, get_object_or_404



def admin_dashboard(request):
    return render(request, 'admin_dashboard/dashboard.html')



def add_staff_member(request):
    if request.method == 'POST':
        form = StaffMemberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff member added successfully!")
            return redirect('view_staff')
    else:
        form = StaffMemberForm()
    return render(request, 'admin_dashboard/add_staff_member.html', {'form': form})

# @login_required
def view_staff(request):
    # if request.session.get('is_admin'):
    staff_members = StaffMember.objects.all()
    return render(request, 'admin_dashboard/view_staff_members.html', {'staff_members': staff_members})

# @login_required
def edit_staff_member(request, staff_id):
    staff = get_object_or_404(StaffMember, id=staff_id)
    
    if request.method == 'POST':
        form = StaffMemberForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff member updated successfully!")
            return redirect('view_staff')
        else:
            messages.error(request, "Error updating staff member. Please check the form.")
    else:
        form = StaffMemberForm(instance=staff)
    
    return render(request, 'admin_dashboard/edit_staff_member.html', {'form': form, 'staff': staff})

# Admin: Delete staff member
# @login_required
def delete_staff_memebr(request, staff_id):
    staff = get_object_or_404(StaffMember, id=staff_id)
    
    if request.method == 'POST':
        staff.delete()
        messages.success(request, "Staff member deleted successfully!")
        return redirect('view_staff')
    
    return render(request, 'admin_dashboard/delete_staff_member.html', {'staff': staff})



def admin_logout(request):
    logout(request)
    return redirect('/login')



