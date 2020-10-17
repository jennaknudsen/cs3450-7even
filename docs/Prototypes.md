# Prototypes

## Prototype 1

The first prototype is actually composed of two parts: a database migration (importing all old
customers, employees, the menu, etc) and a simple password changing webpage. This prototype
can be tested by doing the following:

### Running the database migration

1. Change the working directory to `src/djangoserver_cs3450/`
2. Run `python manage.py migrate`

As the migration runs, you should be able to see the various database entries populated.

NOTE: If you see any error messages, be sure that Django is up-to-date on your computer. This
project was created using Django version 3.1.2.

### Running the password changing webpage

1. Change the working directory to `src/djangoserver_cs3450/` (same directory as the migration)
2. Run `python manage.py runserver`
3. In a web browser, navigate to `localhost:8000/dansbagels/prototype1/`

You should be able to see a dropdown of all users. You can select "Show Current Password" to get 
the current selected user's password, or use "Set Password" to change that user's password. After
changing that user's password, you can select their username again from the dropdown and select
"Show Current Password" to verify that the password change was successful.

## Prototype 2

The second prototype demonstrates how the app will take information from the database and dispaly 
it on the webpage. It can be tested as follows:

1. Change the working directory to `src/djangoserver_cs3450/` (same directory as the migration)
2. Run `python manage.py runserver`
3. In a web browser, navigate to `localhost:8000/dansbagels/prototype2/`

There are 2 drop down menus. The first is a list of all of the users with accounts. The second is 
the type of data you would like to see (first name, last name, email, etc...). When those are selected, 
press the 'Show Current Info' button. The username and desired info of the person you selected will 
appear at the top of the screen.

Note that for this to work, the data migration in prototype 1 needs to be done in order for the information
to be displayed.
