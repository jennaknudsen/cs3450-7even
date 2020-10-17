## CS 3450 - 7even

This is the Git repo for Team 7even for CS 3450.

## Organization and name scheme for the workspace

All documentation will be stored in a folder called `docs/`. All project source
code will be stored in a folder called `src/mysite/`. As the program is being written, 
we expect the `src/mysite/` folder to become subdivided into more subfolders (Django 
will generate many of these automatically).

## Version control procedures

We are using the Git version control system and the GitHub repository hosting
service. 

In Git, whenever a change needs to be made, we will do the following:

* Create a new branch at the tip of `master`
* Make all changes necessary on this branch, pushing the commits to our shared
  GitHub repo
* Once all changes are validated as working, merge back into `master`

If we run into a merge conflict, the individuals who pushed up the code that conflicts
will work with each other to get that conflict solved (unless there's an obvious fix).

## Tool stack description and setup procedure

We are using the Django web framework for this project. 

Django download location is found here: https://www.djangoproject.com/download/ 

Django setup location is found here: https://docs.djangoproject.com/en/3.1/intro/install/ 

We are not deviating from the official setup guide, so it would be unnecessary to repeat
what is stated in the official documentation already.

## Build instructions

Python is an interpreted language and as such, we do not need a complicated build system
for this assignment.

To set up the server on a new computer, perform the following steps:

1. Open a new command-line shell (we used Git Bash)
2. Change the working directoy to the `src/mysite/` directory 
3. When running the program for the first time, the database will be empty. To populate 
the database for the first time, run `python manage.py migrate`.
4. Once the database has been populated, run `python manage.py runserver` to run the 
webserver. The website can be visited at `localhost:8000`.

To run the server on a computer every time after setup, perform steps 1, 2, and 4.

## Unit testing instructions

Unit tests for the database will be stored in a folder called `tests.py` in the `src/mysite` 
directory. To run these unit tests, cd into the directory containing `manage.py` and then 
run `python manage.py test`. This will report any unit test failures and a test summary.

## System testing instructions

For system testing, we are not using any formal framework. Rather, we will have a database
migration set up that can be ran to set the database up in a testable way. Then, we will simulate 
creating/removing user accounts, making transactions, adding/removing orders, etc. If all 
outputs report proper values, then we will consider the system testing as a pass.

## Notes

This description of the process was created before any acutal code was written for this 
assignment. Once we start writing code, we may find a need to modify some of the steps listed 
here. 
