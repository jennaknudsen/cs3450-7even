from django.db import models
import datetime
from django.utils import timezone


# this class holds account types (Customer, Cashier, Chef, Manager)
class AccountType(models.Model):
    CUSTOMER = 1
    CASHIER = 2
    CHEF = 3
    MANAGER = 4
    ACCOUNT_TYPE_CHOICES = [
        (MANAGER, "Manager"),
        (CHEF, "Chef"),
        (CASHIER, "Cashier"),
        (CUSTOMER, "Customer")
    ]
    accountType_text = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPE_CHOICES
    )

    def __str__(self):
        return self.accountType_text


# This class holds user accounts
class Person(models.Model):
    # store username and password as CharFields
    username_text = models.CharField(max_length=200)
    password_text = models.CharField(max_length=200)

    firstName_text = models.CharField(max_length=200)
    lastName_text = models.CharField(max_length=200)
    email_email = models.EmailField(max_length=200)
    phoneNumber_text = models.CharField(max_length=200)

    # the account can't have more than $99999.99 in it due to DB constraints
    accountBalance_decimal = models.DecimalField(max_digits=7, decimal_places=2)

    # each user in the database will be assigned an accountType
    # many-to-one relationship
    accountType = models.ForeignKey(
        AccountType,
        null=True,
        on_delete=models.SET_NULL,      # if for some reason, an account type is deleted,
                                        # keep the Person objects alive, but set their accountType
                                        # to just be NULL instead
    )

    def __str__(self):
        return self.username_text + " (" + self.accountType.accountType_text + ")"


# this class will hold menu items
class MenuItem(models.Model):
    itemName_text = models.CharField(max_length=20)
    inventoryQuantity_int = models.IntegerField()

    # max item price is $99.99
    itemPrice_decimal = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.itemName_text


# this class holds order statuses (Ordered, In Preparation, Ready, Completed)
class OrderStatus(models.Model):
    orderStatus_text = models.CharField(max_length=20)

    def __str__(self):
        return self.orderStatus_text


# this class will hold orders
class Order(models.Model):
    # pickup time is specified as a Python DateTime
    pickUpTime = models.DateTimeField()

    # used to provide order instructions
    # (e.g, which condiment goes on which bagel)
    orderInstructions_text = models.CharField(max_length=200, default="")

    # each order will be tied to a single Person
    # many-to-one relationship 
    personOrdered = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,       # if for some reason, a person's account is deleted,
                                        # delete all orders that person had placed
    )

    # each order will have a single OrderStatus
    # many-to-one relationship
    currentStatus = models.ForeignKey(
        OrderStatus,
        null=True,
        on_delete=models.SET_NULL,      # if for some reason, an order status is deleted,
                                        # keep those orders but set their status to NULL
    )

    def __str__(self):
        return str(self.personOrdered) + "'s order"


# this class will be used to hold an item ordered and its quantity
class OrderLineItem(models.Model):
    # each line item is tied to a single MenuItem
    itemOrdered = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
    )

    # likewise, each line item is tied to a single parent Order
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )

    orderQuantity_int = models.IntegerField()

    def __str__(self):
        return "Item: " + str(self.itemOrdered) + " | Quantity: " + str(self.orderQuantity_int)

