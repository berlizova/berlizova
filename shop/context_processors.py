def cart_count(request):
    """
    Calculate the total number of items in the shopping cart.

    Retrieves the 'cart' from the session data and sums up the quantities
    of all items in the cart.

    Args:
        request (HttpRequest): The HTTP request object containing session data.

    Returns:
        dict: A dictionary containing the total count of items in the cart.
    """
    cart = request.session.get(
        "cart", {}
    )  # Retrieve the cart from session, default to empty dict if not found
    count = sum(cart.values())  # Calculate the total quantity of all items in the cart
    return {"cart_count": count}  # Return the total count as a dictionary
