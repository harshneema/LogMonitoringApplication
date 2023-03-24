import re
import mysql.connector 
import pandas as pd
from array import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pickle
import datetime
import glob
import os
#current date and time
ct = datetime.datetime.now()


print("Welcome to Log Monitoring & Reporting tool \n ")
print("Ensure you've filled the local MySQL Database information and dropped the log files in Dropfiles directory. \n")
log_status = input("Are the files in :- \n 1. .log format \n 2. .txt format \n Answer as (1/2) \n")
Keywords_var = list(input("Enter the keywords here split by comma (Case sensitive) :"). split(","))

if log_status == "2" :
  encode_var = "utf-16"
else :
  encode_var = "utf-8"

# Default variables class
class setup_variables:
    def __init__(self, host, usr , pwd ,sndr , rcvr):
        # Instance Variable    
        self.host = host
        self.user = usr
        self.pwd = pwd
        self.sender = sndr 
        self.reciever = rcvr

# Loads default variables for the setup of the application
file = "info.pkl"
fileobj = open(file , 'rb')
default_var = pickle.load(fileobj)


# Creates Database if it does not exist with the credentials provided
mydb2 = mysql.connector.connect(
  host= default_var.host, 
  user= default_var.user,
  password= default_var.pwd
)
# Drops the database if it already exists to make a new one
mycursor2 = mydb2.cursor()
# Makes a new database named logtool with a table named logs
mycursor2 = mydb2.cursor()
mycursor2.execute("CREATE DATABASE IF NOT EXISTS logtool") 
mydb2.close()

# Connects to the MySQL server with database
mydb = mysql.connector.connect(
  host= default_var.host, 
  user= default_var.user,
  password= default_var.pwd,
  database= "logtool"
)

mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS logs (log_lines TEXT , timestamp varchar(255) , Keyword varchar(255) )")
mycursor.execute("DELETE FROM logs")
   
   
# absolute path to search all log files inside a Dropfiles folder
path = r'./Dropfiles/**/*.log'
files = glob.glob(path, recursive=True)
new_file_name = []

# Renames .log files to .txt so as to make searching through easier
for file in files:
    new_file_name.append(file.replace('.log','.txt'))
    old_file_index = files.index(file)
    old_name = file
    new_name = new_file_name[old_file_index]
    os.rename(old_name, new_name)


# absolute path to search all text files inside the Dropfiles folder
path2 = r'./Dropfiles/**/*.txt'
files2 = glob.glob(path2, recursive=True)
 
# For each log file the search algorithm runs and records it in database
for current_file in files2:
    # Opens the log file for filtering
  with open( current_file ,encoding= encode_var) as log_file:
    searchlines = log_file.readlines()
    lst=[]
    lineno=[]
    log_lines = []
    log_timestamp = []
    keyword_foreach = []
  log_file.close()


  #checking if keyword is in the file
  for i,line in enumerate(searchlines):
      for key_var in Keywords_var:
          if key_var in line:
              for l in searchlines[i:i+1]: 
                keyword_foreach.append(key_var),
                log_timestamp.append(re.findall(r'((Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{1,2} \d{2}:\d{2}:\d{2})', str(l)))
              new_lst=(','.join(searchlines[i:i+1]))
              log_lines.append(new_lst) 
         

  #Filtered logs are stored in the database
  for itm in log_lines:
    indx = log_lines.index(itm)
    time = log_timestamp[indx][0][0]
    keyword_db = keyword_foreach[indx]
    sql = "INSERT INTO logs (log_Lines , timestamp , Keyword) VALUES (%s,%s,%s) ;"
    val = (itm,time,keyword_db,)
    mycursor.execute(sql,val)
    mydb.commit()



# Converting database into a csv file for usage
mycursor = mydb.cursor()
mycursor.execute("SELECT log_lines , timestamp , Keyword FROM logs")
result = mycursor.fetchall()

all_log_lines = []
all_log_timestamp = []
all_log_keywords = []

for log_line , timestamp_csv , keyword_csv in result:
    all_log_lines.append(log_line)
    all_log_timestamp.append(timestamp_csv)
    all_log_keywords.append(keyword_csv)
dic = {'timestamp': all_log_timestamp , 'log lines': all_log_lines , 'keyword found': all_log_keywords}
df = pd.DataFrame(dic)
df_csv = df.to_csv('./final/result_log.csv')


# Script to send an email
fromaddr = default_var.sender
toaddr = default_var.reciever

msg = MIMEMultipart()  
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Your filtered logs taken at " + str(ct)
body = "The filtered logs with the following keywords: \n" + ', '.join(Keywords_var) + " \n which were taken at " + str(ct) + " is attached below as a csv file. \n"
msg.attach(MIMEText(body, 'plain'))

filename = "result_Log.csv"
attachment = open("./final/result_log.csv", "rb")
p = MIMEBase('application', 'octet-stream')
p.set_payload((attachment).read())
encoders.encode_base64(p)
p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
msg.attach(p)

# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
# start TLS for security
s.starttls()
# Authentication
s.login(fromaddr, default_var.mail_pwd)
# Converts the Multipart msg into a string
text = msg.as_string()

# sending the mail
s.sendmail(fromaddr, toaddr, text)
s.quit()

# absolute path to search all log files inside a Dropfiles folder
path3 = r'./Dropfiles/**/*.txt'
files3 = glob.glob(path3, recursive=True)

old_file_name = []
for file in files3:
    old_file_name.append(file.replace('.txt','.log'))
    old_file_index = files3.index(file)
    old_name = file
    new_name = old_file_name[old_file_index]
    os.rename(old_name, new_name)

print("Mail has been sent succesfully!!")

