from django import forms
from .models import *


class AccountCreation(forms.Form):
    # this is the account creation form for the customer
    firstName = forms.CharField(max_length=200)
    lastName = forms.CharField(max_length=200)
    email = forms.EmailField(max_length=200)
    phone = forms.CharField(max_length=200)
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200)


class ManagerAccountCreation(AccountCreation):
    accountType = forms.ChoiceField(choices=AccountType.ACCOUNT_TYPE_CHOICES)
