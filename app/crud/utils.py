def calc_land_discount(price: float, quantity: int) -> tuple[float, float]:
    base_price = price * quantity
    
    discount = 0.0
    if quantity > 10:
        
        discount = base_price * 0.05
    
    final_price = base_price - discount
    
    return discount, final_price

def calc_sea_discount(price: float, quantity: int) -> tuple[float, float]:
    base_price = price * quantity
    discount = 0.0
    if quantity > 10:
        discount = base_price * 0.03
    
    final_price = base_price - discount
    
    return discount, final_price