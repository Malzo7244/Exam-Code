from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, Pizza
from .forms import UserRegisterForm, Pizza_Form, Order_Form
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

@login_required
def home(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user) # Gets our orders if the user is logged in.
    else:
        orders = []
    return render(request, 'home.html', {'orders': orders})

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user) # Gets our order.
    masked_card_number = "**** **** **** " + order.card_number[-4:] # Hides the card number for security.

    if request.method == "POST":
        return redirect('order_details', order_id=order.id)

    return render(request, 'order_confirmation.html', {'order': order, 'masked_card_number': masked_card_number})


@login_required
def create_pizza(request):
    if request.method == 'POST':
        form = Pizza_Form(request.POST)
        if form.is_valid():
            pizza = form.save() # After completing the form successfully, saves pizza.
            request.session['pizza_id'] = pizza.id  # Save pizza ID in session
            return redirect('place_order', pizza_id=pizza.id)
    else:
        form = Pizza_Form()
    return render(request, 'create_pizza.html', {'form': form})


@login_required
def place_order(request, pizza_id):
    pizza = get_object_or_404(Pizza, id=pizza_id)

    if request.method == "POST":
        form = Order_Form(request.POST)
        if form.is_valid():
            order = form.save(commit=False) # Create order but doesn't save yet.
            order.user = request.user # Assigns the current user to the order.
            order.pizza = pizza # Links the order to the selected pizza.
            order.save() # Saves our order to the database.
            return redirect('order_confirmation', order_id=order.id)
    else:
        form = Order_Form()

    return render(request, 'place_order.html', {'form': form, 'pizza': pizza})



def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save() # Saves the new user.
            login(request, user)
            return redirect("home")
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    pizza = order.pizza # Retrieves the specific order and pizza.
    return render(request, 'order_details.html', {'order': order, 'pizza': pizza})


