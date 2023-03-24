import pickle

print("Fill the details of database below \n")
host_name = input("Host :")
user_name = input("User :")
DB_password = input("Password :")
Senders_mail = input("Mail address of sender :")
Senders_pwd = input("Mail specific password of the sender (if using gmail, use the gmail app specific password) :")
Reciever_mail = input("Recievers mail address :")

class setup_variables:

    # The init method or constructor
    def __init__(self, host, usr , pwd ,sndr , rcvr , mail_pwd):
     
        # Instance Variable    
        self.host = host
        self.user = usr
        self.pwd = pwd
        self.sender = sndr 
        self.reciever = rcvr
        self.mail_pwd = mail_pwd

Default_variables = setup_variables(host_name,user_name,DB_password,Senders_mail,Reciever_mail,Senders_pwd)
file = "info.pkl"
fileobj = open(file , 'wb')
pickle.dump(Default_variables,fileobj)
fileobj.close()


