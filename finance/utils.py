from djmoney.money import Money

def calculate_delivery_fee(total):
    """
    Calculate the delivery fee based on the order total.
    :param total: A Money object representing the order total.
    :return: A Money object representing the delivery fee.
    """
    if total.amount < 500:  # Assuming total is in KES
        return Money(50, 'KES')
    elif total.amount < 1000:
        return Money(75, 'KES')
    elif total.amount < 5000:
        return Money(90, 'KES')
    elif total.amount < 10000:
        return Money(115, 'KES')
    else:
        return Money(150, 'KES')
