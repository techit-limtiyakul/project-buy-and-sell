#How to setup the Django Project:

1. Be sure you have python3 installed. Just google how to get it for your OS if not.

2. Using pip install a virtual environment program `pip install virtualenv`. Be sure that your pip version is updated "pip install --upgrade pip"

3. Now create the virtual environment. You can either do this outside of the gitproject or add it to an ignore list, just be sure you don't add the environment folder to your commits. Use the commands `virtualenv ENVIRONMENT_NAME` to create it, `source ENVIRONMENT_NAME/bin/activate` to enable it and `deactivate` to stop it. Depending on your OS you may need to run a batch or executable files at ENVIRONMENT_NAME/Scripts instead to turn it on and off.

4. While in the virtual environment run the command `pip install -r requirements.txt` in the project folder. This should install all the packages you need for the project. If you install a new package later on be sure to remake the requirements.txt file with the command `pip freeze > requirements.txt`

5 Once that is setup you should be able to run the command `python manage.py runserver` in the UCSDBuyAndSell folder and see the django project running locally. To connect just copy the ip it gives into any browser. By default it should be http://127.0.0.1:8000/.