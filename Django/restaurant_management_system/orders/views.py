from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from .models import FoodItem, Order, OrderItem
from .forms import FoodItemForm, OrderForm
from customers.models import Customer
from django.contrib import messages
from django.conf import settings


# @login_required
def view_food_items(request):
    food_items = FoodItem.objects.all()
    return render(request, 'orders/view_food_items.html', {'food_items': food_items})

def customer_food_items(request):
    food_items = FoodItem.objects.all()
    return render(request, 'orders/customer_food_items.html', {'food_items': food_items})


# @login_required
def add_food_item(request):
    # if request.session.get('is_admin'):
        # return HttpResponseForbidden("You are not authorized to access this page.")
    
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Food item added successfully!")
            return redirect('view_food_items')
    else:
        form = FoodItemForm()
    return render(request, 'orders/add_food_item.html', {'form': form})

# @login_required
def edit_food_item(request, item_id):
    # if not request.session.get('is_admin'):
        # return HttpResponseForbidden("You are not authorized to access this page.")
    
    food_item = get_object_or_404(FoodItem, id=item_id)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES, instance=food_item)
        if form.is_valid():
            form.save()
            messages.success(request, "Food item updated successfully!")
            return redirect('view_food_items')
    else:
        form = FoodItemForm(instance=food_item)
    return render(request, 'orders/edit_food_item.html', {'form': form})

# @login_required
def delete_food_item(request, item_id):
    # if not request.session.get('is_admin'):
        # return HttpResponseForbidden("You are not authorized to access this page.")
    
    food_item = get_object_or_404(FoodItem, id=item_id)
    food_item.delete()
    messages.success(request, "Food item deleted successfully!")
    return redirect('view_food_items')

# @login_required
def admin_view_orders(request):

    # if not request.session.get('is_admin'):
        # return HttpResponseForbidden("You are not authorized to access this page.")
    
    orders = Order.objects.all()
    # print(orders.all())
    customers = {}
    for order in orders:
        # print(order.customer)
        customers[order.id] = order.customer
    
    print(customers.values())
    return render(request, 'orders/order_list.html', {'orders': orders})



from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta

from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta

# orders/views.py
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta

# ... your other imports and views ...

def get_chart_data(request):
    """Consolidated view for all chart data"""
    try:
        # Get food items data
        food_items = FoodItem.objects.all()
        food_data = {
            'labels': [item.name for item in food_items],
            'prices': [float(item.price) for item in food_items]
        }

        # Get time periods
        now = timezone.now()
        today = now.date()
        last_week = today - timedelta(days=7)
        last_month = today - timedelta(days=30)

        # Get orders data with time periods
        orders = Order.objects.all()
        orders_today = orders.filter(created_at__date=today)
        orders_week = orders.filter(created_at__date__gte=last_week)
        orders_month = orders.filter(created_at__date__gte=last_month)

        # Get popular items (most ordered)
        popular_items = OrderItem.objects.values(
            'food_item__name'
        ).annotate(
            total_quantity=Sum('quantity')
        ).order_by('-total_quantity')[:5]

        # Calculate revenue periods
        revenue_today = orders_today.aggregate(total=Sum('total_price'))['total'] or 0
        revenue_week = orders_week.aggregate(total=Sum('total_price'))['total'] or 0
        revenue_month = orders_month.aggregate(total=Sum('total_price'))['total'] or 0

        data = {
            'foodItems': {
                'labels': food_data['labels'],
                'prices': food_data['prices']
            },
            'orderTiming': {
                'labels': ['Today', 'This Week', 'This Month'],
                'data': [
                    orders_today.count(),
                    orders_week.count(),
                    orders_month.count()
                ]
            },
            'popularItems': {
                'labels': [item['food_item__name'] for item in popular_items],
                'data': [float(item['total_quantity']) for item in popular_items]
            },
            'revenueData': {
                'labels': ['Today', 'This Week', 'This Month'],
                'data': [
                    float(revenue_today),
                    float(revenue_week),
                    float(revenue_month)
                ]
            },
            'statistics': {
                'total_orders': orders.count(),
                'total_revenue': float(orders.aggregate(
                    total=Sum('total_price'))['total'] or 0),
                'today_orders': orders_today.count(),
                'today_revenue': float(revenue_today),
                'popular_item': popular_items[0]['food_item__name'] if popular_items else 'No orders yet',
                'total_items': food_items.count()
            }
        }
        return JsonResponse(data)
    except Exception as e:
        print(f"Error in get_chart_data: {str(e)}")
        return JsonResponse({
            'error': str(e),
            'foodItems': {'labels': [], 'prices': []},
            'orderTiming': {'labels': [], 'data': []},
            'popularItems': {'labels': [], 'data': []},
            'revenueData': {'labels': [], 'data': []},
            'statistics': {
                'total_orders': 0,
                'total_revenue': 0,
                'today_orders': 0,
                'today_revenue': 0,
                'popular_item': 'None',
                'total_items': 0
            }
        }, status=500)

def admin_dashboard(request):
    """Main admin dashboard view"""
    orders = Order.objects.all()
    context = {
        'total_orders': orders.count(),
        'completed_orders': orders.filter(created_at__date=timezone.now().date()).count(),
        'total_food_items': FoodItem.objects.count(),
        'total_customers': Customer.objects.count(),
    }
    return render(request, 'admin/dashboard.html', context)

# ... rest of your views ...
    """Consolidated view for all chart data"""
    try:
        # Get food items data
        food_items = FoodItem.objects.all()
        food_data = {
            'labels': [item.name for item in food_items],
            'prices': [float(item.price) for item in food_items]
        }

        # Get time periods
        now = timezone.now()
        today = now.date()
        last_week = today - timedelta(days=7)
        last_month = today - timedelta(days=30)

        # Get orders data with time periods
        orders = Order.objects.all()
        orders_today = orders.filter(created_at__date=today)
        orders_week = orders.filter(created_at__date__gte=last_week)
        orders_month = orders.filter(created_at__date__gte=last_month)

        # Get popular items (most ordered)
        popular_items = OrderItem.objects.values(
            'food_item__name'
        ).annotate(
            total_quantity=Sum('quantity')
        ).order_by('-total_quantity')[:5]

        # Calculate revenue periods
        revenue_today = orders_today.aggregate(total=Sum('total_price'))['total'] or 0
        revenue_week = orders_week.aggregate(total=Sum('total_price'))['total'] or 0
        revenue_month = orders_month.aggregate(total=Sum('total_price'))['total'] or 0

        data = {
            'foodItems': {
                'labels': food_data['labels'],
                'prices': food_data['prices']
            },
            'orderTiming': {
                'labels': ['Today', 'This Week', 'This Month'],
                'data': [
                    orders_today.count(),
                    orders_week.count(),
                    orders_month.count()
                ]
            },
            'popularItems': {
                'labels': [item['food_item__name'] for item in popular_items],
                'data': [float(item['total_quantity']) for item in popular_items]
            },
            'revenueData': {
                'labels': ['Today', 'This Week', 'This Month'],
                'data': [
                    float(revenue_today),
                    float(revenue_week),
                    float(revenue_month)
                ]
            },
            'statistics': {
                'total_orders': orders.count(),
                'total_revenue': float(orders.aggregate(
                    total=Sum('total_price'))['total'] or 0),
                'today_orders': orders_today.count(),
                'today_revenue': float(revenue_today),
                'popular_item': popular_items[0]['food_item__name'] if popular_items else 'No orders yet',
                'total_items': food_items.count()
            }
        }
        return JsonResponse(data)
    except Exception as e:
        print(f"Error in get_chart_data: {str(e)}")
        return JsonResponse({
            'error': str(e),
            'foodItems': {'labels': [], 'prices': []},
            'orderTiming': {'labels': [], 'data': []},
            'popularItems': {'labels': [], 'data': []},
            'revenueData': {'labels': [], 'data': []},
            'statistics': {
                'total_orders': 0,
                'total_revenue': 0,
                'today_orders': 0,
                'today_revenue': 0,
                'popular_item': 'None',
                'total_items': 0
            }
        }, status=500)
    """Consolidated view for all chart data"""
    try:
        # Get food items data
        food_items = FoodItem.objects.all()
        food_data = {
            'labels': [item.name for item in food_items],
            'prices': [float(item.price) for item in food_items]
        }

        # Get orders data
        orders = Order.objects.all()
        
        # If status field doesn't exist, you can use this alternative logic
        today = timezone.now().date()
        order_status = {
            'pending': orders.filter(created_at__date=today).count(),
            'completed': orders.filter(created_at__date=today, total_price__gt=0).count(),
            'cancelled': 0  # You might want to define your own logic for cancelled orders
        }

        # Get popular items data
        popular_items = OrderItem.objects.values(
            'food_item__name'
        ).annotate(
            count=Count('id')
        ).order_by('-count')[:5]

        # Calculate total revenue
        total_revenue = orders.aggregate(
            total=Sum('total_price')
        )['total'] or 0

        data = {
            'foodItems': {
                'labels': food_data['labels'],
                'prices': food_data['prices']
            },
            'orderStatus': {
                'labels': ['Today\'s Orders', 'Completed', 'Pending'],
                'data': [
                    orders.filter(created_at__date=today).count(),
                    order_status['completed'],
                    order_status['pending']
                ]
            },
            'popularItems': {
                'labels': [item['food_item__name'] for item in popular_items],
                'data': [item['count'] for item in popular_items]
            },
            'statistics': {
                'total_orders': orders.count(),
                'total_revenue': float(total_revenue),
                'today_orders': orders.filter(created_at__date=today).count(),
                'yesterday_orders': orders.filter(
                    created_at__date=today - timedelta(days=1)
                ).count()
            }
        }
        return JsonResponse(data)
    except Exception as e:
        print(f"Error in get_chart_data: {str(e)}")  # For debugging
        return JsonResponse({
            'error': str(e),
            'foodItems': {'labels': [], 'prices': []},
            'orderStatus': {'labels': [], 'data': []},
            'popularItems': {'labels': [], 'data': []},
            'statistics': {
                'total_orders': 0,
                'total_revenue': 0,
                'today_orders': 0,
                'yesterday_orders': 0
            }
        }, status=500)
    """Consolidated view for all chart data"""
    try:
        # Get food items data
        food_items = FoodItem.objects.all()
        food_data = {
            'labels': [item.name for item in food_items],
            'prices': [float(item.price) for item in food_items]
        }

        # Get orders data
        orders = Order.objects.all()
        order_status = {
            'pending': orders.filter(status='pending').count(),
            'completed': orders.filter(status='completed').count(),
            'cancelled': orders.filter(status='cancelled').count(),
        }

        # Get popular items data (items with most orders)
        order_items = OrderItem.objects.values('food_item__name').annotate(
            order_count=Count('id')
        ).order_by('-order_count')[:5]

        data = {
            'foodItems': {
                'labels': food_data['labels'],
                'prices': food_data['prices']
            },
            'orderStatus': {
                'labels': ['Pending', 'Completed', 'Cancelled'],
                'data': [
                    order_status['pending'],
                    order_status['completed'],
                    order_status['cancelled']
                ]
            },
            'popularItems': {
                'labels': [item['food_item__name'] for item in order_items],
                'data': [item['order_count'] for item in order_items]
            },
            'statistics': {
                'total_orders': orders.count(),
                'total_revenue': float(orders.filter(status='completed').aggregate(
                    total=Sum('total_price')
                )['total'] or 0)
            }
        }
        return JsonResponse(data)
    except Exception as e:
        print(f"Error in get_chart_data: {str(e)}")  # For debugging
        return JsonResponse({'error': str(e)}, status=500)

def admin_dashboard(request):
    """Main admin dashboard view"""
    # Get basic statistics for initial page load
    orders = Order.objects.all()
    context = {
        'total_orders': orders.count(),
        'completed_orders': orders.filter(status='completed').count(),
        'pending_orders': orders.filter(status='pending').count(),
        'cancelled_orders': orders.filter(status='cancelled').count(),
        'total_food_items': FoodItem.objects.count(),
        'total_customers': Customer.objects.count(),
    }
    return render(request, 'admin/dashboard.html', context)

# Update your admin_view_orders to use the same statistics
def admin_view_orders(request):
    orders = Order.objects.all()
    context = {
        'orders': orders,
        'total_orders': orders.count(),
        'completed_orders': orders.filter(status='completed').count(),
        'pending_orders': orders.filter(status='pending').count(),
        'cancelled_orders': orders.filter(status='cancelled').count(),
    }
    return render(request, 'orders/order_list.html', context)


# ---------- Customer Views ----------

# @login_required
def place_order(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity'))
        food_item = get_object_or_404(FoodItem, id=item_id)

        # Create new order
        order = Order.objects.create(customer=request.user, total_price=food_item.price * quantity)
        OrderItem.objects.create(order=order, food_item=food_item, quantity=quantity)
        messages.success(request, "Order placed successfully!")
        return redirect('customer_orders')

    food_items = FoodItem.objects.all()
    return render(request, 'orders/customer_orders.html', {'food_items': food_items})

@login_required
def customer_orders(request):
    """Customer can view only their own orders."""
    orders = Order.objects.filter(customer_id=request.user.id)
    return render(request, 'orders/customer_orders.html', {'orders': orders})


@login_required
def edit_order(request, order_id):
    """Customer can edit their existing orders."""
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        if quantity > 0:
            order_item = order.orderitem_set.first()
            order_item.quantity = quantity
            order_item.save()
            order.total_price = order_item.food_item.price * quantity
            order.save()
            messages.success(request, "Order updated successfully!")
        else:
            messages.error(request, "Quantity must be greater than zero.")
        return redirect('customer_orders')

    return render(request, 'orders/order_edit.html', {'order': order})

@login_required
def delete_order(request, order_id):

    order = get_object_or_404(Order, id=order_id, customer=request.user)
    order.delete()
    messages.success(request, "Order deleted successfully!")
    return redirect('/orders')

def orders_data(request):
    # Fetch the data you need for the charts
    orders = Order.objects.all()  # Adjust this query as needed
    order_count = orders.count()
    # Example data structure
    data = {
        'orders': [order_count],  # Replace with actual data logic
        'status': [10, 5, 2]  # Example status counts
    }
    return JsonResponse(data)

def items_data(request):
    items = FoodItem.objects.all()
    item_names = [item.name for item in items]  # Assuming FoodItem has a 'name' field
    item_counts = [item.orderitem_set.count() for item in items]  # Count of orders for each item
    data = {
        'item_names': item_names,
        'item_counts': item_counts,
    }
    return JsonResponse(data)
