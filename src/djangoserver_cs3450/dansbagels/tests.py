from django.test import TestCase
from dansbagels.models import *
from dansbagels.dbfunctions import *

class OwnerAccountPageTestCase(TestCase):
    def setUp(self):
        # nothing needed for setup
        pass

    def test_create_account(self):
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
                createAccount(firstName, lastName, username, password, email, phoneNumber, accountType))

        # make sure some things saved
        self.assertEqual("fn.ln", Person.objects.get(firstName_text=firstName).username_text)

        # now, try to delete the account with username "fn.ln"
        # make sure it's there to begin with
        self.assertEqual(True, Person.objects.filter(username_text=username).exists())
        # test delete works
        self.assertEqual(True, deleteAccount(username))
        # ensure it deleted
        self.assertEqual(False, Person.objects.filter(username_text=username).exists())
        # test deletion on nonexistent object (should fail)
        self.assertEqual(False, deleteAccount(username))
