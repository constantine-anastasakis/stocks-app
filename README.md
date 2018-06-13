# ROBOT ADVISER 

#Python: 
First, user should check to see if Python3 is already installed on their machine:

# Mac Terminal:
which python3 # check for Python Version 3.x

# Windows Command Prompt:
where python

If Python3 is not installed, user must intall - once installed, user should be able to run python3 and pip3 from the command-line. 

Note: users must check the option, "Add Python 3.6 to PATH" when you are installing Python from the downloaded installer.

#Forking This Repository 
Users must next "fork" this upstream repository under their own control.

Then download their forked version of this repository using the GitHub.com online interface or the Git command-line interface. If you are using command-line Git, you can download it by "cloning" it:

git clone https://github.com/YOUR_USERNAME/stocks-app-py.git
After downloading your forked repository, navigate into its root directory:

cd stocks-app-py/

Install package dependencies using one of the following commands, depending on how you have installed Python and how you are managing packages:

# Pipenv on Mac or Windows:
pipenv install -r requirements.txt

# Homebrew-installed Python 3.x on Mac OS:
pip3 install -r requirements.txt

# All others:
pip install -r requirements.txt
If you are using Pipenv, enter a new virtual environment (pipenv shell) before running any of the commands below.

All commands below assume you are running them from this repository's root directory.

#Running the Script 
After installing Python and downloading this repository, users can run the script "robo_adviser.py" which is found in the /app sub-directory of the stocks-app directory. 

