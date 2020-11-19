from dansbagels.models import *
from decimal import Decimal

# Change this variable to True if you want debug messages to print 
printDebugMessages = True

# Check to see if a given username/combination is valid.
# Return true if the username/password combination is in the database, false otherwise.
def verifyLoginDB(username, password):
    listOfUsers = []
    allPeople = Person.objects.all()
    for person in allPeople:
        listOfUsers.append((person.username_text, person.password_text))
    return (username, password) in listOfUsers


# Create an account given proper input parameters.
# Return true if account was created, false otherwise.
# An accountType object can be obtained by:
# AccountType.objects.get(pk=[1/2/3/4])
# All other parameters are strings.
def createAccountDB(firstName, lastName, username, password, email, phoneNumber,
                  accountType, accountBalance=100.00):
    if checkUsernameDB(username):
        printDebug("User " + username + " already exists. Refusing to create new account. Aborting")
        return False
    try:
        person = Person()
        person.firstName_text = firstName
        person.lastName_text = lastName
        person.username_text = username
        person.password_text = password
        person.email_email = email
        person.phoneNumber_text = phoneNumber
        person.accountBalance_decimal=accountBalance
        person.accountType = accountType
        person.save()
        printDebug("Account for " + firstName + " " + lastName + " created successfully")
        return True
    except Exception as e:
        printDebug("Failed to create account for " + firstName + " " + lastName)
        printDebug(str(e))
        return False


# Delete an account given a username.
# Return true if account was successfully deleted, false otherwise.
def deleteAccountDB(username):
    try:
        Person.objects.get(username_text=username).delete()
        printDebug("Account " + username + " deleted successfully")
        return True
    except Exception as e:
        printDebug("Failed to delete account " + username)
        printDebug(str(e))
        return False


# Update an account given proper input parameters.
# This function searches for a user with username_text == oldUsername
# Having two username parameters allows the function to support updating a username
# Return true if the update was successful, false otherwise.
def updateAccountDB(oldUsername, firstName, lastName, username, password, email, phoneNumber, 
                    accountBalance):
    # don't allow the user to take the username of another user that already exists
    if oldUsername != username and checkUsernameDB(username):
        printDebug("User " + username + " already exists. Refusing to update account. Aborting")
        return False
    try:
        person = Person.objects.get(username_text=oldUsername)
        person.firstName_text = firstName
        person.lastName_text = lastName
        person.username_text = username
        person.password_text = password
        person.email_email = email
        person.phoneNumber_text = phoneNumber
        person.accountBalance_decimal = accountBalance
        person.save()
        printDebug("Account for " + firstName + " " + lastName + " updated successfully")
        return True
    except Exception as e:
        printDebug("Failed to update account for " + firstName + " " + lastName)
        printDebug(str(e))
        return False


# Check to see if an account exists, given a username.
def checkUsernameDB(username):
    listOfUsernames = []
    allPeople = Person.objects.all()
    for person in allPeople:
        listOfUsernames.append(person.username_text)
    return username in listOfUsernames


# Create an order in the database.
#
# The order is created FIRST, and then OrderLineItems are added to the order. 
#
# The OrderLineItems MUST be added one-by-one by calling the createOrderLineItemDB() function
# afer calling this function.
#
# Function expects a Person object as an input (this can be easily obtained
# using a Function such as Person.objects.get(username_text="<username>")
#
# Function also expects a pickUpTime DateTimeField as an input. This can be
# obtained with a function such as datetime(year, month, day, hour, min, second, tzinfo=pytz.UTC)
#
# Make sure to import:
# from datetime import datetime
# from django.utils import timezone
# import pytz
#
# Returns True if created successfully, False otherwise.
def createOrderDB(pickUpTime, orderInstructions, orderCost, personOrdered, currentStatus):
    try:
        order = Order()
        order.pickUpTime = pickUpTime
        order.orderInstructions_text = orderInstructions
        order.orderCost_decimal = orderCost
        order.personOrdered = personOrdered
        order.currentStatus = currentStatus     # order.currentStatus should be of type OrderStatus
        order.save()

        # if the order cost is set correctly, then deduct the balance from the user
        personOrdered.accountBalance_decimal -= Decimal(orderCost)
        personOrdered.save()

        printDebug("Order for " + str(personOrdered.username_text) + " created successfully.")
        return order
    except Exception as e:
        printDebug("Failed to create order for " + str(personOrdered.username_text))
        printDebug(str(e))
        return None


# Creates an order line item.
# This function MUST be called for each line item that is added to an order.
# This line item must be tied to an Order and a MenuItem at creation. 
# When the order is created, decrement the total count of the menu item.
# Returns True if created successfully, False otherwise.
def createOrderLineItemDB(itemOrdered, order, orderQuantity):
    try:
        # first, make sure order quantity is valid
        if not checkOrderQuantityValidDB(itemOrdered, orderQuantity):
            return False

        # create the item
        orderLineItem = OrderLineItem()
        orderLineItem.itemOrdered = itemOrdered
        orderLineItem.order = order
        orderLineItem.orderQuantity_int = orderQuantity
        orderLineItem.save()

        # now, decrement the total count of the MenuItem
        # itemOrdered input parameter is a MenuItem, so we can edit it directly
        itemOrdered.inventoryQuantity_int -= orderQuantity
        itemOrdered.save()

        printDebug("OrderLineItem for order " + str(order) + " created successfully.")
        return True
    except Exception as e:
        printDebug("Failed to create order line item of item " + str(itemOrdered)
                + " and quantity " + str(orderQuantity))
        printDebug(str(e))
        return False


# Check to ensure that an order quantity is valid.
def checkOrderQuantityValidDB(itemOrdered, orderQuantity):
    if orderQuantity == 0:
        printDebug("Order quantity 0 is invalid.")
        return False
    elif orderQuantity > itemOrdered.inventoryQuantity_int:
        printDebug("Order quantity " + str(orderQuantity) + " is invalid: There are only "
                + str(itemOrdered.inventoryQuantity_int) + " left.")
        return False
    else:
        printDebug("Order quantity " + str(orderQuantity) + " is valid.")
        return True


# modifies order status in the database
# newOrderStatus should be of type OrderStatus
# this can be obtained by using a Function such as OrderStatus.objects.get(pk=<key>)
def modifyOrderStatusDB(order, newOrderStatus):
    try:
        order.currentStatus = newOrderStatus
        order.save()
        return True
    except Exception as e:
        printDebug("Failed to modify order status for order " + str(order))
        printDebug(e)
        return False


# deletes an order from the database
# if we need to issue a refund, then we can specify True for issueRefund
def cancelOrderDB(order, issueRefund):
    try:
        if issueRefund:
            order.personOrdered.accountBalance_decimal += Decimal(order.orderCost_decimal)
            order.personOrdered.save()

        # regardless of refund or not, delete the order
        order.delete()
        return True

    except Exception as e:
        printDebug("Failed to delete order " + str(order))
        printDebug(e)
        return False


# Print a simple debug message preceded by [DEBUG]
def printDebug(message):
    if printDebugMessages:
        print("[DEBUG] " + str(message))
