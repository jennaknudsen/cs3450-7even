from django import forms
from django.forms.widgets import NumberInput, HiddenInput
from .models import *


class AccountCreation(forms.Form):
    # this is the account creation form for the customer
    # Site used to figure out placeholder stuff: https://stackoverflow.com/questions/4101258/how-do-i-add-a-placeholder-on-a-charfield-in-django
    firstName = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'First Name'}), max_length=200)
    lastName = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}), max_length=200)
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email'}), max_length=200)
    phone = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}), max_length=200)
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Username'}), max_length=200)
    password = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Password'}), max_length=200)


class ManagerAccountCreation(AccountCreation):
    accountType = forms.ChoiceField(choices=AccountType.ACCOUNT_TYPE_CHOICES)


class UpdateAccount(forms.Form):
    # this class cant inherit from Account creation since we need the fields to not be required
    firstName = forms.CharField(max_length=200, required=False, widget=HiddenInput())
    lastName = forms.CharField(max_length=200, required=False, widget=HiddenInput())
    email = forms.EmailField(max_length=200, required=False, widget=HiddenInput())
    phone = forms.CharField(max_length=200, required=False, widget=HiddenInput())
    username = forms.CharField(max_length=200, required=False, widget=HiddenInput())
    password = forms.CharField(max_length=200, required=False, widget=HiddenInput())
    accountBalance = forms.DecimalField(max_digits=7, decimal_places=2, required=False, widget=HiddenInput())


class OrderBagel(forms.Form):
    itemsOrdered = forms.CharField(max_length=200, widget=HiddenInput())
    orderCost = forms.DecimalField(max_digits=7, widget=HiddenInput())
    pickUpDate = forms.DateField(label="Pick-Up Date", widget=NumberInput(attrs={'type': 'date'}))
    pickUpTime = forms.TimeField(label="Pick-Up Time", widget=forms.TimeInput(attrs={'type': 'time'}))
    orderInstruction = forms.CharField(max_length=200, widget=forms.Textarea(attrs={"rows": 5, "cols": 50, "placeholder":
    	"Please place special instructions in this field, i.e. which toppings go with which bagel"}))	


class Reorder(forms.Form):
    pickUpDate = forms.DateField(label="Pick-Up Date", widget=NumberInput(attrs={'type': 'date'}))
    pickUpTime = forms.TimeField(label="Pick-Up Time", widget=forms.TimeInput(attrs={'type': 'time'}))


class UpdateOrder(forms.Form):
    orderStatus = forms.ChoiceField(choices=OrderStatus.ORDER_STATUS_CHOICES)


class CreateMenuItem(forms.Form):
    itemName = forms.CharField(max_length=200)
    itemPrice = forms.DecimalField(max_digits=4, decimal_places=2)
    initialQuantity = forms.IntegerField()
