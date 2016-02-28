To install.

1. install the python tools required.

    $ sudo apt-get -y install git
    
    $ sudo apt-get -y install python-pip python-dev build-essential
    
    $ sudo pip install --upgrade pip
    
    $ sudo pip install --upgrade virtualenv


2. Pull from git.

3. Run these commands to setup.

    $ cd healthshare

    $ virtualenv flask

    $ source flask/bin/activate

    $ pip install -r requirements.txt

    $ mkdir tmp

    $ ./db_create.py

4. run a http server to test
        
    To run use the python built in server, ./run.py

    Access at localhost:5000

5. Create a user to test out the features.
    
    You'll first have to create a user by entering any email address at the login prompt.
    
Andrew Rowe (c) 2016