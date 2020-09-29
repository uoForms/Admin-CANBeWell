# Admin-CANBeWell
CANBeWell Admin Site

1. pip install pipenv
    You can install django in the virtual enviroment with pipenv.

2. pipenv shell
    In order to run code in a virtual environment.
    This is going to create a new file named "Pipfile" which contains all the dependencies.
    And this will open a python shell and run project on the virtual env.

Install Packages
1. pipenv install django
    Install django package on the Python shell you just created.

2. pipenv install python-firebase
    Install python-firebase dependency and update Pipfile on virtual env.

3. pipenv install python_jwt
    Install python_jwt dependency and update Pipfile on virtual env.

4. pipenv install gcloud
    Install gcloud dependency and update Pipfile on virtual env.

5. pipenv install sseclient
    Install sseclient dependency and update Pipfile on virtual env.

6. pipenv install pycryptodome
    Install pycryptodome dependency and update Pipfile on virtual env.
    
    PS: cd to site-packages, change folder crypto to upercase Crypto, Python is case sensitive. You may want to check that.

7. pipenv install requests-toolbelt
    Install requests-toolbelt dependency and update Pipfile on virtual env.

8. pipenv install pandas 
    Install pandas dependency and update Pipfile on virtual env.

9. pipenv install pyrebase
    Install pyrebase dependency and update Pipfile on virtual env.

Then you have finished installation!!

To run the project:

1. python manage.py runserver

2. python manage.py migrate
    IF you have unapplied migration.

