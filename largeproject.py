class User:
    def __init__(self, id, name, gmail):
        self.id = id
        self.name = name
        self.gmail = gmail


class Customer(User):
    def __init__(self, id, name, gmail):
        super().__init__(id, name, gmail)
        self.orderitems = []

    def additem(self, item, quantity):
        self.orderitems.append([item, quantity])

    def getstatus(self, myorder):
        return myorder.status


class Restaurant:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.menucard = []

    def addmenuitem(self, menu):
        self.menucard.append(menu)

    def setstatus(self, myorder):
        myorder.status = "waiting for delivery man"
        return myorder.status


class Order:
    def __init__(self, menu, orderitems, deliveryagent):
        self.menu = menu
        self.items = orderitems
        self.deliveryagent = deliveryagent
        self.status = "preparing"
        self.subtotal = self.calculate_subtotal()
        self.tax_rate = 0.05
        self.tax = self.subtotal * self.tax_rate
        self.final_price = self.subtotal + self.tax

    def calculate_subtotal(self):
        total = 0
        for item, quantity in self.items:
            total += item.price * quantity
        return total

    def getstatus(self):
        return self.status

    def getfinalprice(self):
        return self.final_price


class OrderItem:
    def __init__(self, name, price, ratings):
        self.name = name
        self.price = price
        self.ratings = ratings


class Delivery(User):
    def __init__(self, id, name, gmail):
        super().__init__(id, name, gmail)

    def setstatus(self, myorder):
        myorder.status = f"{self.name} has delivered the order"
        return myorder.status


class Payment:
    def __init__(self, type, order):
        self.type = type
        self.status = "pending"
        self.order = order

    def calculate_price(self):
        return self.order.final_price

    def getstatus(self):
        return self.status

    def setstatus(self, newstatus):
        self.status = newstatus


pizza = OrderItem("pizza", 89, 4.5)
burger = OrderItem("burger", 70, 5.5)
shawarma = OrderItem("shawarma", 79, 5.0)
nahari = OrderItem("nahari", 129, 4.8)

shahgouse = Restaurant("shahgouse", "hyderabad")
pistahouse = Restaurant("pistahouse", "hyderabad")

pistahouse.addmenuitem(nahari)
pistahouse.addmenuitem(shawarma)
shahgouse.addmenuitem(pizza)
shahgouse.addmenuitem(burger)

person1 = Customer(1, "syed kashif", "syedkashif2405@gmail.com")
deliveryagent = Delivery(555, "mohan", "mohan@129.gmail.com")

person1.additem(pizza, 3)
person1.additem(burger, 4)

myorder = Order(shahgouse.menucard, person1.orderitems, deliveryagent)

print("Order Status:", person1.getstatus(myorder))
print("Subtotal:", myorder.subtotal)
print("Tax:", myorder.tax)
print("Final Price:", myorder.final_price)

print("Restaurant Status:", shahgouse.setstatus(myorder))

print("Delivery Status:", deliveryagent.setstatus(myorder))
print("Final Order Status:", myorder.getstatus())

mypayment = Payment("upi", myorder)

print("Payment Status:", mypayment.getstatus())
print("Amount to Pay:", mypayment.calculate_price())

mypayment.setstatus("payment is done")
print("Payment Status:", mypayment.getstatus())
