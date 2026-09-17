from abc import ABC, abstractmethod


class User(ABC):
    def __init__(self, id, name, gmail, phone):
        self.id = id
        self.name = name
        self.gmail = gmail
        self.phone = phone

    @abstractmethod
    def get_role(self):
        pass

    @abstractmethod
    def login(self):
        pass


class Customer(User):
    def __init__(self, id, name, gmail, phone):
        super().__init__(id, name, gmail, phone)
        self.orderitems = []
        self.__wallet_balance = 0

    def get_role(self):
        return "Customer"

    def login(self):
        print(self.name, "logged in as Customer")

    def additem(self, item, quantity):
        if item.is_available:
            self.orderitems.append(OrderItem(item, quantity))
            print(item.name, "added to cart")
        else:
            print(item.name, "is not available")

    def getstatus(self, myorder):
        return myorder.status

    def add_money(self, amount):
        if amount > 0:
            self.__wallet_balance += amount

    def get_wallet_balance(self):
        return self.__wallet_balance

    def search_restaurant(self, restaurants, name, location=None, cuisine=None):
        result = []

        for restaurant in restaurants:
            if name.lower() not in restaurant.name.lower():
                continue

            if location is not None:
                if location.lower() != restaurant.location.lower():
                    continue

            if cuisine is not None:
                if cuisine.lower() != restaurant.cuisine.lower():
                    continue

            result.append(restaurant)

        return result


class RestaurantOwner(User):
    def __init__(self, id, name, gmail, phone):
        super().__init__(id, name, gmail, phone)
        self.restaurant = None

    def get_role(self):
        return "Restaurant Owner"

    def login(self):
        print(self.name, "logged in as Restaurant Owner")

    def set_restaurant(self, restaurant):
        self.restaurant = restaurant
        restaurant.owner = self

    def add_menu_item(self, item):
        if self.restaurant is not None:
            self.restaurant.addmenuitem(item)

    def remove_menu_item(self, item):
        if self.restaurant is not None:
            self.restaurant.remove_menu_item(item)

    def update_price(self, item, new_price):
        if self.restaurant is not None:
            self.restaurant.update_price(item, new_price)


class Admin(User):
    def __init__(self, id, name, gmail, phone):
        super().__init__(id, name, gmail, phone)

    def get_role(self):
        return "Admin"

    def login(self):
        print(self.name, "logged in as Admin")

    def manage_system(self):
        print("Admin is managing the system")


class FoodItem:
    def __init__(self, item_id, name, price, category, is_available=True):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.category = category
        self.is_available = is_available

    def __str__(self):
        return f"{self.name} - Rs.{self.price}"


class OrderItem:
    def __init__(self, food_item, quantity):
        self.food_item = food_item
        self.quantity = quantity

    def get_total(self):
        return self.food_item.price * self.quantity


class Restaurant:
    def __init__(self, restaurant_id, name, location, cuisine):
        self.restaurant_id = restaurant_id
        self.name = name
        self.location = location
        self.cuisine = cuisine
        self.menucard = []
        self.owner = None

    def addmenuitem(self, menu):
        self.menucard.append(menu)
        print(menu.name, "added to menu")

    def remove_menu_item(self, item):
        if item in self.menucard:
            self.menucard.remove(item)
            print(item.name, "removed from menu")

    def update_price(self, item, new_price):
        if item in self.menucard:
            item.price = new_price
            print(item.name, "price updated")

    def display_menu(self):
        print("\nMenu of", self.name)

        for item in self.menucard:
            print(
                item.name,
                "- Rs.",
                item.price,
                "- Available:",
                item.is_available
            )

    def setstatus(self, myorder):
        myorder.update_status("CONFIRMED")
        return myorder.status


class Vehicle(ABC):
    @abstractmethod
    def get_charge_per_km(self):
        pass


class Bike(Vehicle):
    def get_charge_per_km(self):
        return 10


class Scooter(Vehicle):
    def get_charge_per_km(self):
        return 12


class Cycle(Vehicle):
    def get_charge_per_km(self):
        return 7


class DeliveryPartner(User):
    def __init__(self, id, name, gmail, phone, vehicle):
        super().__init__(id, name, gmail, phone)
        self.partner_id = id
        self.vehicle = vehicle
        self.availability_status = "AVAILABLE"
        self.current_order = None

    def get_role(self):
        return "Delivery Partner"

    def login(self):
        print(self.name, "logged in as Delivery Partner")

    def accept_order(self, myorder):
        if self.availability_status == "AVAILABLE":
            self.current_order = myorder
            self.availability_status = "BUSY"
            myorder.deliveryagent = self
            myorder.update_status("OUT_FOR_DELIVERY")
            return "Order accepted by " + self.name

        return "Delivery partner is not available"

    def calculate_delivery_charge(self, distance):
        return distance * self.vehicle.get_charge_per_km()

    def setstatus(self, myorder):
        myorder.update_status("DELIVERED")
        self.current_order = None
        self.availability_status = "AVAILABLE"
        return f"{self.name} has delivered the order"


class Order:
    def __init__(
        self,
        order_id,
        customer,
        restaurant,
        orderitems,
        deliveryagent=None,
        distance=0,
        discount=None
    ):
        self.order_id = order_id
        self.customer = customer
        self.restaurant = restaurant
        self.items = orderitems
        self.deliveryagent = deliveryagent
        self.__status = "PLACED"
        self.distance = distance

        self.subtotal = self.calculate_subtotal()
        self.discount_strategy = discount

        if discount is not None:
            self.discount = discount.calculate_discount(self.subtotal)
        else:
            self.discount = 0

        if deliveryagent is not None:
            self.delivery_charge = deliveryagent.calculate_delivery_charge(
                distance
            )
        else:
            self.delivery_charge = 0

        self.tax_rate = 0.05

        taxable_amount = (
            self.subtotal
            - self.discount
            + self.delivery_charge
        )

        self.tax = taxable_amount * self.tax_rate
        self.__total_amount = taxable_amount + self.tax

    @property
    def status(self):
        return self.__status

    def update_status(self, new_status):
        valid_status = [
            "PLACED",
            "CONFIRMED",
            "PREPARING",
            "OUT_FOR_DELIVERY",
            "DELIVERED",
            "CANCELLED"
        ]

        if new_status in valid_status:
            self.__status = new_status

            notification = PushNotification()

            if new_status == "CONFIRMED":
                message = f"Your order #{self.order_id} has been confirmed!"

            elif new_status == "PREPARING":
                message = f"Your order #{self.order_id} is being prepared."

            elif new_status == "OUT_FOR_DELIVERY":
                message = f"Your order #{self.order_id} is out for delivery."

            elif new_status == "DELIVERED":
                message = f"Your order #{self.order_id} has been delivered!"

            elif new_status == "CANCELLED":
                message = f"Your order #{self.order_id} has been cancelled."

            else:
                return

            notification.send(message)

    @property
    def total_amount(self):
        return self.__total_amount

    def calculate_subtotal(self):
        total = 0

        for item in self.items:
            total += item.get_total()

        return total

    def getstatus(self):
        return self.status

    def getfinalprice(self):
        return self.total_amount


class Discount(ABC):
    @abstractmethod
    def calculate_discount(self, amount):
        pass


class PercentageDiscount(Discount):
    def __init__(self, percentage):
        self.percentage = percentage

    def calculate_discount(self, amount):
        return amount * self.percentage / 100


class FlatDiscount(Discount):
    def __init__(self, amount):
        self.amount = amount

    def calculate_discount(self, amount):
        return min(self.amount, amount)


class NoDiscount(Discount):
    def calculate_discount(self, amount):
        return 0


class Payment(ABC):
    def __init__(self, order):
        self.order = order
        self.status = "PENDING"

    def calculate_price(self):
        return self.order.total_amount

    def getstatus(self):
        return self.status

    @abstractmethod
    def pay(self):
        pass

    @abstractmethod
    def refund(self):
        pass


class UPIPayment(Payment):
    def pay(self):
        print("Processing UPI payment...")
        self.status = "SUCCESS"
        print("UPI payment successful")

    def refund(self):
        self.status = "REFUNDED"
        print("UPI payment refunded")


class CreditCardPayment(Payment):
    def pay(self):
        print("Processing Credit Card payment...")
        self.status = "SUCCESS"
        print("Credit Card payment successful")

    def refund(self):
        self.status = "REFUNDED"
        print("Credit Card payment refunded")


class CashOnDelivery(Payment):
    def pay(self):
        self.status = "PENDING"
        print("Cash on Delivery selected")
        print("Payment will be collected during delivery")

    def refund(self):
        self.status = "REFUNDED"
        print("Cash payment refunded")


class Notification(ABC):
    @abstractmethod
    def send(self, message):
        pass


class EmailNotification(Notification):
    def send(self, message):
        print("EMAIL:", message)


class SMSNotification(Notification):
    def send(self, message):
        print("SMS:", message)


class PushNotification(Notification):
    def send(self, message):
        print("PUSH:", message)


pizza = FoodItem(101, "Pizza", 89, "Fast Food")
burger = FoodItem(102, "Burger", 70, "Fast Food")
shawarma = FoodItem(103, "Shawarma", 79, "Fast Food")
nahari = FoodItem(104, "Nahari", 129, "Indian")


shahgouse = Restaurant(
    1,
    "Shahgouse",
    "Hyderabad",
    "Indian"
)

pistahouse = Restaurant(
    2,
    "Pista House",
    "Hyderabad",
    "Indian"
)


shahgouse.addmenuitem(pizza)
shahgouse.addmenuitem(burger)

pistahouse.addmenuitem(nahari)
pistahouse.addmenuitem(shawarma)


person1 = Customer(
    1,
    "Syed Kashif",
    "syedkashif2405@gmail.com",
    "9876543210"
)

owner = RestaurantOwner(
    2,
    "Shah Gouse Owner",
    "owner@gmail.com",
    "9876543211"
)

admin = Admin(
    3,
    "Admin",
    "admin@gmail.com",
    "9876543212"
)


owner.set_restaurant(shahgouse)


deliveryagent = DeliveryPartner(
    555,
    "Mohan",
    "mohan@gmail.com",
    "9876543213",
    Bike()
)


print("\n===== FOOD DELIVERY SYSTEM =====")

print("\n===== LOGIN =====")

person1.login()
owner.login()
deliveryagent.login()
admin.login()


print("\n===== RESTAURANT MENU =====")

shahgouse.display_menu()


print("\n===== ADD TO CART =====")

person1.additem(pizza, 3)
person1.additem(burger, 4)


discount = FlatDiscount(100)


myorder = Order(
    1001,
    person1,
    shahgouse,
    person1.orderitems,
    deliveryagent,
    distance=5,
    discount=discount
)


print("\n===== ORDER DETAILS =====")

print("Order ID:", myorder.order_id)
print("Customer:", person1.name)
print("Restaurant:", shahgouse.name)
print("Order Status:", myorder.status)
print("Subtotal:", myorder.subtotal)
print("Discount:", myorder.discount)
print("Delivery Charge:", myorder.delivery_charge)
print("Tax:", myorder.tax)
print("Final Amount:", myorder.total_amount)


print("\n===== RESTAURANT =====")

print("Restaurant Status:", shahgouse.setstatus(myorder))


myorder.update_status("PREPARING")

print("Order Status:", myorder.status)


print("\n===== PAYMENT =====")

mypayment = UPIPayment(myorder)

print("Payment Method: UPI")
print("Amount to Pay:", mypayment.calculate_price())

mypayment.pay()

print("Payment Status:", mypayment.getstatus())


print("\n===== DELIVERY =====")

print(deliveryagent.accept_order(myorder))

print("Order Status:", myorder.status)


print("\n===== DELIVERY COMPLETED =====")

print("Delivery Status:", deliveryagent.setstatus(myorder))

print("Final Order Status:", myorder.getstatus())


print("\n===== ADMIN =====")

admin.manage_system()


print("\n===== RESTAURANT SEARCH =====")

restaurants = [shahgouse, pistahouse]

result = person1.search_restaurant(
    restaurants,
    "House",
    "Hyderabad",
    "Indian"
)

for restaurant in result:
    print(
        restaurant.name,
        "-",
        restaurant.location,
        "-",
        restaurant.cuisine
    )