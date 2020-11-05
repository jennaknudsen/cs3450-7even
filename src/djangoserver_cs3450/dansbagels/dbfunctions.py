from dansbagels.models import *

# Change this variable to True if you want debug messages to print 
printDebugMessages = True

# Check to see if a given username/combination is valid.
# Return true if the username/password combination is in the database, false otherwise.
def verifyLogin(username, password):
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
                  accountType, accountBalance):
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
        person.accountBalance_decimal=accountBalance
        person.accountType = accountType
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


# Print a simple debug message preceded by [DEBUG]
def printDebug(message):
    if printDebugMessages:
        print("[DEBUG] " + str(message))
