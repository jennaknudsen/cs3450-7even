from dansbagels.models import *

# Helper function to return true if the username/password combination is 
# in the database, false otherwise.
def verifyLogin(username, password):
    listOfUsers = []
    allPeople = Person.objects.all()
    for person in allPeople:
        listOfUsers.append((person.username_text, person.password_text))
    return (username, password) in listOfUsers



