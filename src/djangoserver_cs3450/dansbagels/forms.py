from django import forms
from django.forms.widgets import NumberInput, HiddenInput
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


class UpdateAccount(forms.Form):
    # this class cant inherit from Account creation since we need the fields to not be required
    firstName = forms.CharField(max_length=200, required=False)
    lastName = forms.CharField(max_length=200, required=False)
    email = forms.EmailField(max_length=200, required=False)
    phone = forms.CharField(max_length=200, required=False)
    username = forms.CharField(max_length=200, required=False)
    password = forms.CharField(max_length=200, required=False)
    accountBalance = forms.DecimalField(max_digits=7, decimal_places=2, required=False)

class OrderBagel(forms.Form):
    itemsOrdered = forms.CharField(max_length=200, widget=HiddenInput())
    pickUpDate = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    pickUpTime = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
