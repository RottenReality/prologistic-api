def calculate_land_discount(price: float, quantity: int) -> tuple[float, float]:
    discount = price * 0.05 if quantity > 10 else 0
    return discount, price - discount

def calculate_sea_discount(price: float, quantity: int) -> tuple[float, float]:
    discount = price * 0.03 if quantity > 10 else 0
    return discount, price - discount