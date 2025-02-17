from django.db import models

class Pizza(models.Model):
    PIZZA_SIZES = [ 
        ("s", "Small"),
        ("m", "Medium"),
        ("l", "Large"),
        ("xl", "Extra Large")
    ] 

    CRUST_TYPE = [
        ("thin", "Thin"),
        ("thick", "Thick"),
        ("normal", "Normal"),
        ("gluten_free", "Gluten Free")
    ]

    SAUCE_TYPE = [
        ("tomato", "Tomato"),
        ("bbq", "BBQ"),
        ("harissa", "Harissa")
    ]

    CHEESE_TYPE = [
        ("mozarella", "Mozarella"),
        ("vegan", "Vegan"),
        ("low_fat", "Low Fat"),
        ("parmesan", "Parmesan")
    ]

    size = models.CharField(max_length=2, choices=PIZZA_SIZES)
    crust = models.CharField(max_length=15, choices=CRUST_TYPE)
    sauce = models.CharField(max_length=15, choices=SAUCE_TYPE)
    cheese = models.CharField(max_length=15, choices=CHEESE_TYPE)

    pepperoni = models.BooleanField(default=False)
    chicken = models.BooleanField(default=False)
    ham = models.BooleanField(default=False)
    pineapple = models.BooleanField(default=False)
    peppers = models.BooleanField(default=False)
    mushrooms = models.BooleanField(default=False)
    onions = models.BooleanField(default=False)



class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.TextField()
    card_number = models.CharField(max_length=16)
    card_expiration_date = models.CharField(max_length=5)
    card_cvv = models.CharField(max_length=3)
    order_date = models.DateTimeField(auto_now_add=True)

class PizzaOption(models.Model): # Define Pizza Options model for the admin panel, since I originally made Pizza one large model that contains sauces, cheeses, sizes, and toppings.
    SIZES = "sizes"
    CHEESES = "cheeses"
    SAUCES = "sauces"

    OPTION_TYPES = [ # Defines the options we have.
        (SIZES, "Pizza Sizes"),
        (CHEESES, "Cheese Types"),
        (SAUCES, "Sauce Types"),
    ]

    option_type = models.CharField(max_length=10, choices=OPTION_TYPES)
    name = models.CharField(max_length=50, unique=True) # Prevents duplicate entries

    def __str__(self):
        return f"{self.get_option_type_display()}: {self.name}" # Readable name in Django admin interface.
