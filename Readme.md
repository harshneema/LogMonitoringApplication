# Log monitoring and Reporting Application
## - Prepared by Harsh Neema

This is a log monitoring and reporting tool that will filter logs and report them to the system administrator.

### Instructions before you use -

- Ensure you have Python3 and MySQL installed on your system.
- Turn on the MySQL server before starting the application.

- Run the following commands to install necessary python packages -
    - python3 -m pip install pip
    - python3 -m pip install mysql-connector-python
    - pip install regex
    - pip install pandas

- Use app_setup.py first to enter credentials. (These credentials will remain default until this script is ran again to change)
- If you send the email through a google account, ensure that you enter gmail app specific password instead of what you normally use.
    - App specific password instructions can be found here - 
            https://support.google.com/accounts/answer/185833?hl=en
- info.pkl keeps these credentials stored. 

- Now drop the Log files in the directory named Dropfiles (For testing purposes, it already has some sample files)
- Run the log_tool.py file.
- Enter keywords you want to look for (NOTE: They're case sensitive)
- The script might take a few seconds to analyze. 
- If it takes a lot of time then use Ctrl+C to abort.
- The csv file can also be accessed inside the Final folder.

- Now , check your email for the csv file with all the information.
- Application has run successfully !!


If any other difficulty is faced then please contact at - 
f20200878@pilani.bits-pilani.ac.in
