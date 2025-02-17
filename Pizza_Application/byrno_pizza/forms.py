from django import forms
from .models import Pizza, Order, PizzaOption
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class Pizza_Form(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = "__all__" # Grabs all fields from the pizza model.

class Order_Form(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["name", "address", "card_number", "card_expiration_date", "card_cvv"] # Grabs all fields necessary.

    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number')

        if len(card_number) != 16 or not card_number.isdigit(): # Checks that the card number is valid.
            raise forms.ValidationError("Card number must be 16 digits.")
        return card_number

    def clean_card_cvv(self):
        cvv = self.cleaned_data.get('card_cvv')
        if len(cvv) != 3 or not cvv.isdigit(): # Checks if the cvv is valid.
            raise forms.ValidationError("CVV code must be 3 digits.")
        return cvv

    def clean_card_expiration_date(self):
        exp = self.cleaned_data.get('card_expiration_date')
        if len(exp) != 5 or exp[2] != "/" or not exp[:2].isdigit() or not exp[3:].isdigit(): # Checks if the expiration date is in the correct formula.
            raise forms.ValidationError("Invalid format for expiration date. Use MM/YY.")
        return exp

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True) # When registering for an account an email is required.

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"] # Two passwords for verification.

class Admin_Pizza_Form(forms.ModelForm):
    # Since I originally made pizza one singular model, we have to define fields manually so we can populate the choices dynamically.
    size = forms.ChoiceField(choices=[], required=True)
    sauce = forms.ChoiceField(choices=[], required=True)
    cheese = forms.ChoiceField(choices=[], required=True)

    def __init__(self, *args, **kwargs):
        # Dynamically fills the choices for size, sauce, and cheese.
        super().__init__(*args, **kwargs)

        # Fetch all available pizza sizes from the PizzaOption model where option_type="sizes"
        self.fields['size'].choices = [(opt.name, opt.name) for opt in PizzaOption.objects.filter(option_type=PizzaOption.SIZES)]

        # Where option_type="sauces"
        self.fields['sauce'].choices = [(opt.name, opt.name) for opt in PizzaOption.objects.filter(option_type=PizzaOption.SAUCES)]

        # Where option_type="cheeses"
        self.fields['cheese'].choices = [(opt.name, opt.name) for opt in PizzaOption.objects.filter(option_type=PizzaOption.CHEESES)]

    class Meta:
        model = Pizza
        fields = "__all__"
