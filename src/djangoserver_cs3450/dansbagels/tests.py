from django.test import TestCase
from dansbagels.models import *
from dansbagels.dbfunctions import *
from datetime import datetime
from django.utils import timezone
import pytz

class OwnerAccountPageTestCase(TestCase):
    def setUp(self):
        # nothing needed for setup
        pass

    def test_create_and_delete_account(self):
        # set up the account parameters
        firstName = "FN"
        lastName = "LN"
        username = "fn.ln"
        password = "test-password"
        email = "test@test.com"
        phoneNumber = "123-456-7890"
        accountType = AccountType.objects.get(pk=2)

        # create the account
        self.assertEqual(True,
                createAccountDB(firstName, lastName, username, password, email, phoneNumber, accountType))

        # creating a duplicate account should fail
        self.assertEqual(False,
                createAccountDB(firstName, lastName, username, password, email, phoneNumber, accountType))

        # make sure some things saved
        self.assertEqual("fn.ln", Person.objects.get(firstName_text=firstName).username_text)

        # now, try to delete the account with username "fn.ln"
        # make sure it's there to begin with
        username = "fn.ln"

        self.assertEqual(True, Person.objects.filter(username_text=username).exists())
        # test delete works
        self.assertEqual(True, deleteAccountDB(username))
        # ensure it deleted
        self.assertEqual(False, Person.objects.filter(username_text=username).exists())
        # test deletion on nonexistent object (should fail)
        self.assertEqual(False, deleteAccountDB(username))

        # creating the account after deletion should work again
        self.assertEqual(True,
                createAccountDB(firstName, lastName, username, password, email, phoneNumber, accountType))


class ViewAccountInfoPageTestCase(TestCase):
    def setUp(self):
        # set up the account parameters
        self.firstName = "FN"
        self.lastName = "LN"
        self.username = "fn2.ln2"
        self.password = "test-password"
        self.email = "test@test.com"
        self.phoneNumber = "123-456-7890"
        self.accountType = AccountType.objects.get(pk=2)
        # we already know that createAccount works, so just use it here
        createAccountDB(self.firstName, self.lastName, self.username, self.password,
                      self.email, self.phoneNumber, self.accountType)

    def test_update_account(self):
        # we will reset the username from "fn2.ln2" to "new.username"
        # we will also set the account balance to 50.00
        self.assertEqual(True, 
                updateAccountDB("fn2.ln2", self.firstName, self.lastName, "new.username", self.password,
                              self.email, self.phoneNumber, self.accountType, 50.00))
        self.assertEqual(50.00, Person.objects.get(username_text="new.username").accountBalance_decimal)

        # make sure the account with username "fn2.ln2" does not exist anymore
        self.assertEqual(False, Person.objects.filter(username_text="fn2.ln2").exists())

        # create another user with the initial parameters (again)
        createAccountDB(self.firstName, self.lastName, self.username, self.password,
                      self.email, self.phoneNumber, self.accountType)
        # make sure that updating the account to a username that already exists fails
        self.assertEqual(False,
                updateAccountDB("fn2.ln2", self.firstName, self.lastName, "new.username", self.password,
                              self.email, self.phoneNumber, self.accountType, 50.00))


class CreateOrderPageTestCase(TestCase):
    def setUp(self):
        # don't need any initial setup
        pass

    def test_create_and_populate_order(self):
        # pickup time: 2020-Nov-10, 19:30:54, UTC time
        pickUpTime = datetime(2020, 11, 10, 19, 30, 54, tzinfo=pytz.UTC)
        personOrdered = Person.objects.get(username_text="AbeLincoln")

        # should work with a custom order status as well as the default first order status
        self.assertEqual(True,
                createOrderDB(pickUpTime, personOrdered))

        currentStatus = OrderStatus.objects.get(pk=3)
        self.assertEqual(True,
                createOrderDB(pickUpTime, personOrdered, currentStatus))

        # now, add an order line item to each order
        itemOrdered = []
        itemOrdered.append(MenuItem.objects.get(itemName_text="Plain Bagel"))
        itemOrdered.append(MenuItem.objects.get(itemName_text="Cheesy Bagel"))
        itemOrdered.append(MenuItem.objects.get(itemName_text="Honey Nut Smear"))

        # demonstrating getting all orders for a person
        AbeOrders = []
        allOrders = Order.objects.all()
        for order in allOrders:
            if (order.personOrdered.username_text == "AbeLincoln"):
                AbeOrders.append(order)

        initialQuantities = [itemOrdered[0].inventoryQuantity_int, itemOrdered[1].inventoryQuantity_int,
                itemOrdered[2].inventoryQuantity_int]
        orderQuantities = [2, 4, 1]

        # add itemOrdered_1 to first order, _2 and _3 to second order
        self.assertEqual(True,
                createOrderLineItemDB(itemOrdered[0], AbeOrders[0], orderQuantities[0]))
        self.assertEqual(True,
                createOrderLineItemDB(itemOrdered[1], AbeOrders[1], orderQuantities[1]))
        # make sure that creating a 0 quantity order and an order that's way too big are both not allowed
        self.assertEqual(False,
                createOrderLineItemDB(itemOrdered[2], AbeOrders[1], 0))
        self.assertEqual(False,
                createOrderLineItemDB(itemOrdered[2], AbeOrders[1], 10000000))
        self.assertEqual(True,
                createOrderLineItemDB(itemOrdered[2], AbeOrders[1], orderQuantities[2]))

        # now make sure that inventory quantities decreased correctly
        for i in range (0, 3):
            self.assertEqual(orderQuantities[i],
                    initialQuantities[i] - itemOrdered[i].inventoryQuantity_int)

