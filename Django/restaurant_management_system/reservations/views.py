from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import CustomerReservation
from .forms import  CustomerReservationForm
from customers.models import Customer

# Admin: View all available reservations
# @login_required
def view_available_reservations(request):
    #  if request.session.get('is_admin'):
        available_reservations = CustomerReservation.objects.all()
        return render(request, 'reservations/reservation_list.html', {'available_reservations': available_reservations})

# Customer: Make a reservation
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomerReservation
from .forms import CustomerReservationForm

@login_required
def make_reservation(request):
    if request.method == 'POST':
        form = CustomerReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.customer = request.user
            # Calculate total price based on number of guests (example: $10 per guest)
            reservation.total_price = reservation.number_of_guests * 10
            reservation.save()
            messages.success(request, "Reservation booked successfully!")
            return redirect('view_customer_reservations')
    else:
        form = CustomerReservationForm()

    return render(request, 'reservations/make_reservation.html', {'form': form})


# Customer: View their own reservations
@login_required
def view_customer_reservations(request):
    reservations = CustomerReservation.objects.filter(customer_id=request.user.id)
    return render(request, 'reservations/view_customer_reservations.html', {'reservations': reservations})


