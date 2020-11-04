from django.test import TestCase
from dansbagels.models import *
from dansbagels.dbfunctions import *

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

        # make sure some things saved
        self.assertEqual("fn.ln", Person.objects.get(firstName_text=firstName).username_text)

        # now, try to delete the account with username "fn.ln"
        # make sure it's there to begin with
        username = "fn.ln"

        self.assertEqual(True, Person.objects.filter(username_text=username).exists())
        # test delete works
        self.assertEqual(True, deleteAccount(username))
        # ensure it deleted
        self.assertEqual(False, Person.objects.filter(username_text=username).exists())
        # test deletion on nonexistent object (should fail)
        self.assertEqual(False, deleteAccount(username))


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
                updateAccount("fn2.ln2", self.firstName, self.lastName, "new.username", self.password,
                              self.email, self.phoneNumber, self.accountType, 50.00))
        self.assertEqual(50.00, Person.objects.get(username_text="new.username").accountBalance_decimal)

        # make sure the account with username "fn2.ln2" does not exist anymore
        self.assertEqual(False, Person.objects.filter(username_text="fn2.ln2").exists())

