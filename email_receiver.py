import email
import imaplib
import os
import PySimpleGUI as sg


def authenticate():
    host = 'imap.gmail.com'
    try:
        with open("data.txt", 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip().split(",")
                username = line[0]
                password = line[1]
    except:
        print("You need to authenticate")
        os.system("python login_window.py")  
        
    try:
        mail = imaplib.IMAP4_SSL(host)
        
    except:
        sg.popup_auto_close('Error','Authentication failed.\nCheck Internet Connection and Try Again')
        exit()
        
    mail.login(username, password)
    return mail

def get_inbox(filter1):
    
    try:
        mail = authenticate()
    except imaplib.IMAP4.error:
        print("Invalid credentials. Please check your username and password and try again.")
    typ, data = mail.select('INBOX')
    my_message = return_data(typ, data, mail, filter1,number1=10)
    return my_message

def get_sent(filter1):
    
    try:
        mail = authenticate()
    except imaplib.IMAP4.error:
        print("Invalid credentials. Please check your username and password and try again.")
    typ, data = mail.select('"[Gmail]/Sent Mail"')
    my_message = return_data(typ, data, mail, filter1,number1=10)
    return my_message

def get_filtered(filter1):
    
    try:
        mail = authenticate()
    except imaplib.IMAP4.error:
        print("Invalid credentials. Please check your username and password and try again.")
    typ, data = mail.select()
    my_message = return_data(typ, data, mail, filter1,number1=10)
    return my_message


    
def return_data(typ, data, mail, filter1,number1):
    num_msgs = int(data[0])
    #print('There are %d messages in INBOX' % num_msgs)
    _, search_data = mail.search(None, filter1)  #type ALL to print all inbox mail or UNSEEN
    my_message = []

    for num in search_data[0].split()[-number1:]:
    #for num in search_data[0].split():  //this modification allows us to get the last 10 emails
        #print(num)
        email_data = {}
        list1=[]
        _, data = mail.fetch(num, '(RFC822)')
        #print(data[0])
        _, b = data[0]
        email_message = email.message_from_bytes(b)
        for header in ['subject', 'to', 'from', 'date']:
            #print("{}: {}".format(header, email_message[header]))
            email_data[header] = email_message[header]
        for part in email_message.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                #print('body:',body.decode())  #print body
                email_data['body'] = body.decode('latin-1')      #encoding changes to allow microsoft messages
            elif part.get_content_type() == "text/html":
                html_body = part.get_payload(decode=True)
                email_data['body'] = html_body.decode('latin-1')
               
            elif "attachment" in content_disposition:
                filename = part.get_filename()
                list1.append(filename)
                if filename:
                    folder_name = "Attachments"
                    if not os.path.isdir(folder_name):
                        os.mkdir(folder_name)
                    filepath = os.path.join(folder_name, filename)  
                    open(filepath, "wb").write(part.get_payload(decode=True))  # download attachment and save it
                    
            email_data['files'] = list1
            
        my_message.append(email_data)
        
    return my_message

