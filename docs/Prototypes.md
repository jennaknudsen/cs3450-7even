# Prototypes

## Prototype 1

The first prototype is actually composed of two parts: a database migration (importing all old
customers, employees, the menu, etc) and a simple password changing webpage. This prototype
can be tested by doing the following:

### Running the database migration

1. Change the working directory to `src/djangoserver_cs3450/`
2. Run `python manage.py migrate`

As the migration runs, you should be able to see the various database entries populated.

### Running the password changing webpage

1. Change the working directory to `src/djangoserver_cs3450/` (same directory as the migration)
2. Run `python manage.py runserver`
3. In a web browser, navigate to `localhost:8000/dansbagels/prototype1/`

You should be able to see a dropdown of all users. You can select "Show Current Password" to get 
the current selected user's password, or use "Set Password" to change that user's password. After
changing that user's password, you can select their username again from the dropdown and select
"Show Current Password" to verify that the password change was successful.

## Prototype 2

...
