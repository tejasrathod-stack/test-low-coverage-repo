import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class Product:
    id: str
    name: str
    price: float
    category: str
    stock_quantity: int
    
    def update_stock(self, quantity: int):
        """Update stock level. Raises error if insufficient stock."""
        if self.stock_quantity + quantity < 0:
            raise ValueError(f"Insufficient stock for product {self.name}")
        self.stock_quantity += quantity

class Promotion:
    def __init__(self, name: str, discount_type: str, value: float, min_spend: float = 0):
        self.name = name
        self.discount_type = discount_type # 'percentage' or 'fixed'
        self.value = value
        self.min_spend = min_spend

    def apply(self, total: float) -> float:
        """Apply promotion to a subtotal."""
        if total < self.min_spend:
            return 0.0
        
        if self.discount_type == 'percentage':
            return total * (self.value / 100)
        elif self.discount_type == 'fixed':
            return min(total, self.value)
        return 0.0

class ShoppingCart:
    def __init__(self):
        self.items: Dict[str, int] = {} # product_id -> quantity
        self.products: Dict[str, Product] = {}
        self.applied_promotions: List[Promotion] = []

    def add_item(self, product: Product, quantity: int = 1):
        """Add item to cart."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        self.products[product.id] = product
        self.items[product.id] = self.items.get(product.id, 0) + quantity

    def remove_item(self, product_id: str, quantity: int = 1):
        """Remove item from cart."""
        if product_id not in self.items:
            raise KeyError("Product not in cart")
        
        current_qty = self.items[product_id]
        if quantity >= current_qty:
            del self.items[product_id]
            if product_id in self.products:
                # We keep the product reference in products dict for now, or could clean it up
                pass
        else:
            self.items[product_id] -= quantity

    def calculate_subtotal(self) -> float:
        """Calculate total before discounts."""
        total = 0.0
        for pid, qty in self.items.items():
            product = self.products.get(pid)
            if product:
                total += product.price * qty
        return total

    def calculate_total(self) -> float:
        """Calculate final total after best promotion applied."""
        subtotal = self.calculate_subtotal()
        discount = 0.0
        
        # Simple rule: apply the single best promotion available
        if self.applied_promotions:
            possible_discounts = [p.apply(subtotal) for p in self.applied_promotions]
            discount = max(possible_discounts)
            
        return max(0.0, subtotal - discount)
        
    def add_promotion(self, promo: Promotion):
        self.applied_promotions.append(promo)

    def apply_bulk_discount(self, threshold: int, discount_percent: float):
        """
        Apply a bulk discount if the total number of items in the cart exceeds the threshold.
        """
        total_items = sum(self.items.values())
        if total_items >= threshold:
            discount_amount = self.calculate_subtotal() * (discount_percent / 100)
            # Create a dynamic promotion for this bulk discount
            bulk_promo = Promotion(f"Bulk Discount (> {threshold} items)", "fixed", discount_amount)
            self.add_promotion(bulk_promo)

class OrderProcessor:
    def __init__(self):
        self.orders = []

    def process_order(self, cart: ShoppingCart, customer_email: str) -> Dict:
        """
        Process the order: validate stock, deduct stock, record order.
        """
        if not cart.items:
            raise ValueError("Cannot process empty cart")
            
        if not self._validate_email(customer_email):
            raise ValueError("Invalid email address")

        # 1. Check Stock
        for pid, qty in cart.items.items():
            product = cart.products[pid]
            if product.stock_quantity < qty:
                raise ValueError(f"Out of stock for {product.name}. Requested: {qty}, Available: {product.stock_quantity}")
        
        # 2. Deduct Stock
        for pid, qty in cart.items.items():
            product = cart.products[pid]
            product.update_stock(-qty)
            
        # 3. Finalize
        order_details = {
            "order_id": f"ORD-{len(self.orders) + 1:04d}",
            "date": datetime.datetime.now().isoformat(),
            "customer": customer_email,
            "items": list(cart.items.items()),
            "total_amount": cart.calculate_total(),
            "status": "confirmed"
        }
        self.orders.append(order_details)
        return order_details

    def _validate_email(self, email: str) -> bool:
        return "@" in email and "." in email.split("@")[1]
