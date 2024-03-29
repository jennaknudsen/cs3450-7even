# Generated by Django 3.0.3 on 2020-02-24 17:00

from django.db import migrations
from django.utils import timezone
from datetime import datetime
import pytz

def populate_db(apps, schema_editor):
    """
    This is a new function that I define myself.  It takes two parameters.

    The first parameter `apps` is an application registry which enables access
    to my models without needing to use the import statement.  The details are
    a bit involved, but the application registry lets me access previous
    versions of my models; importing the classes via the import statement would
    only let me use those classes as they exist right now.

    The second parameter `schema_editor` may be used when I change the layout
    of fields in a model.  Since we are only interested in creating new
    records right now, we can ignore it.
    """

    print(" ")
    print("Now running custom migration populate_AccountType")
    AccountType = apps.get_model('dansbagels', 'AccountType')

    print("Adding Customer, Cashier, Chef, Manager")
    customer = AccountType(accountType_text="Customer")
    customer.save()
    cashier = AccountType(accountType_text="Cashier")
    cashier.save()
    chef = AccountType(accountType_text="Chef")
    chef.save()
    manager = AccountType(accountType_text="Manager")
    manager.save()


    print("\nDone adding Customer, Chef, Cashier, Manager")

class Migration(migrations.Migration):

    dependencies = [
        ('dansbagels', '0002_auto_20201016_2046'),
    ]

    operations = [
        migrations.RunPython(populate_db)
    ]
