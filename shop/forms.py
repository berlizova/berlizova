from django import forms


class AddToCartForm(forms.Form):
    """
    A form for adding items to the shopping cart.

    This form allows the user to specify the quantity of a product
    they wish to add to their cart.

    Fields:
        quantity (IntegerField): The number of items to add to the cart.
    """

    quantity = forms.IntegerField(
        min_value=1,  # The minimum value allowed for the quantity is 1
        initial=1,  # The default initial value for the quantity field
        widget=forms.NumberInput(
            attrs={"class": "form-control"}
        ),  # Use a number input field with Bootstrap classes
    )
