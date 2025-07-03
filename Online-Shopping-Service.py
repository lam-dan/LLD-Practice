
from typing import Dict, List, Optional
from enum import Enum
from threading import Lock

class OrderStatus(Enum):
    PENDING = 1
    PLACED = 2
    SHIPPED = 3
    DELIVERED = 4
    CANCELLED = 5

class OrderItem:
    def __init_(self, quantity: int):
        self.product = Product 
        self.quantity = quantity


class Order:
    def __init__(self, user: User, items: List[OrderItem]):
        self.id = str(uuid.uuid4())
        self.user = user
        self.items = items
        self.total_amount = self._calculate_total_amount()
        self.status = OrderStatus.PENDING

    def _calculate_total_amount(self) -> float:
        return sum(item.product.price * item.quantity for item in self.items)

    def cancel(self):
        if self.status == OrderStatus.SHIPPED:
            raise Exception("Cannot cancel shipped order")
        self.status = OrderStatus.CANCELLED

    def set_status(self, status: OrderStatus):
        self.status = status

    def get_id(self):
        return self.id

    def get_user(self):
        return self.user

    def get_items(self):
        return self.items

    def get_total_amount(self):
        return self.total_amount

    def get_status(self):
        return self.status


class Product:
    def __init__(self, name: str, price: int, description: str, quantity: int):
        self.id = id(self)
        self.description = description
        self.name = name
        self.price = price
        self.quantity = quantity

    def increase_quantity(self, amount: int):
        self.quantity += amount
    
    def decrease_quantity(self, amount: int):
        self.quantity -= amount

    def update_quanttoy(self, amount: int):
        self.quantity = amount
    
    def is_available(self, amount: int):
        return amount <= self.quantity 
    
    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    
    def get_description(self):
        return self.description
    
    def get_price(self):
        return self.price
    
    def get_quantity(self):
        return self.quantity

class Cart:
    def __init__(self):
        self.items = Dict[Product, int]

class User:
    def __init__(self, email: str, name: str, phone_number: int, password: str, cart: Cart):
        self.id: int = id(self)
        self.email = email
        self.name = name
        self.phone_number = phone_number
        self.password = password
        self.orders = List[Order]
        self.cart = Cart

    def add_order(self, order: Order):
        self.orders.append(order)

    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    
    def get_email(self):
        return self.email
    
    def get_password(self):
        return self.password

    def get_cart(self):
        return self.cart
    
    def get_orders(self):
        return self.orders

class OnlineShoppingService:
    _instance = None
    _lock = Lock()

    def __init__(self):
        self.users: Dict[str, User] = {}
        self.products: Dict[str, Product] = {}
        self.orders: Dict[str, Order] = {}

    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = OnlineShoppingService()
            return cls._instance

    def register_user(self, name: str, email: str, password: str) -> User:
        user = User(name, email, password)
        self.users[user.id] = user
        return user

    def get_user(self, user_id: str) -> User:
        return self.users.get(user_id)

    def add_product(self, name: str, description: str, price: float, stock: int) -> Product:
        product = Product(name, description, price, stock)
        self.products[product.id] = product
        return product

    def add_to_cart(self, user_id: str, product_id: str, quantity: int):
        user = self.users.get(user_id)
        product = self.products.get(product_id)

        if user is None or product is None:
            raise ValueError("User or product not found")

        user.cart.add(product, quantity)

    def get_user_cart(self, user_id: str):
        user = self.users.get(user_id)
        return user.cart

    def get_product(self, product_id: str) -> Product:
        return self.products.get(product_id)

    def search_products(self, keyword: str) -> List[Product]:
        result = []
        keyword_lower = keyword.lower()
        
        for product in self.products.values():
            product_name_lower = product.name.lower()
            
            if keyword_lower in product_name_lower:
                result.append(product)
        
        return result

    def place_order(self, user_id: str, payment: Payment) -> Order:
        with self._lock:
            user = self.users.get(user_id)
            if user is None:
                raise ValueError("User not found")

            order_items = []
            items = user.cart.items  # Assuming `items` is a dict {Product: int}

            for product, quantity in items.items():
                if product.is_available(quantity):
                    product.decrease_stock(quantity)
                    order_items.append(OrderItem(product, quantity))

            order = Order(user, order_items)
            self.orders[order.id] = order
            user.cart.clear()
            user.add_order(order)

            if payment.process_payment(order.total_amount):
                order.status = OrderStatus.PLACED
            else:
                order.status = OrderStatus.CANCELLED
                # Revert stock
                for item in order_items:
                    product = item.product
                    quantity = item.quantity
                    product.increase_stock(quantity)

            return order

    def cancel_order(self, order_id: str):
        with self._lock:
            order = self.orders.get(order_id)
            if order is None:
                raise ValueError("Order not found")

            order.cancel()

            for item in order.items:
                product = item.product
                quantity = item.quantity
                product.increase_stock(quantity)

    def get_order(self, order_id: str) -> Order:
        return self.orders.get(order_id)

    def generate_order_id(self) -> str:
        return f"ORDER{uuid4().hex[:8].upper()}"
    


shopping_service = OnlineShoppingService.get_instance()

# Register users
user1 = shopping_service.register_user("John Doe", "john@example.com", "password123")
user2 = shopping_service.register_user("Jane Smith", "jane@example.com", "password456")

# Add products
product1 = shopping_service.add_product("Smartphone", "High-end smartphone", 999.99, 10)
product2 = shopping_service.add_product("Laptop", "Powerful gaming laptop", 1999.99, 5)

# Add items to user's cart
shopping_service.add_to_cart(user1.id, product1.id, 2)
shopping_service.add_to_cart(user1.id, product2.id, 1)

# Place order
order1 = shopping_service.place_order(user1.id, CreditCardPayment())
print(f"Order placed: {order1.id}")

# User searches for products
search_results = shopping_service.search_products("laptop")
print("Search Results:")
for product in search_results:
    print(product.name)

# User views order history
user_orders = user1.orders
print("User 1 Order History:")
for order in user_orders:
    print(f"Order ID: {order.id}")
    print(f"Total Amount: ${order.total_amount:.2f}")
    print(f"Status: {order.status.name}")



