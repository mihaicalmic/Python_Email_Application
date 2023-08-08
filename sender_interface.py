import PySimpleGUI as sg
import sys
import email_sender
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from os.path import basename

# change the theme
if len(sys.argv) > 2:
    email_address_1 = sys.argv[1]
    subject_1 = sys.argv[2]
sg.theme("DarkPurple4")
#create menu layout
menu_def =  [ 
                ["Help",["Versions","About"]]
            ]

layout = [
              [sg.Menu(menu_def)],
              
              [sg.Text("EMAIL ADDRESS:"), sg.Input(key='-EMAIL_ADDRESS-', do_not_clear=True, size=(25, 1))],
              [sg.Text("SUBJECT:"), sg.Input(key='-SUBJECT-', do_not_clear=True, size=(20, 1)),sg.Button('Attach File')],
              [sg.Multiline("", do_not_clear=True, key = '-MESSAGE-', size=(60,12))],
              [sg.StatusBar("", size=60, key="-STAT-")],
              [sg.Button('Send Email'),sg.Button('Clear'),sg.Button('Remove Attachments')]
        ]

window = sg.Window('Python Email Client', layout, finalize=True)
files=[]
receivers=[]
listlength=[]
stat_format=""

def validate(values):
    is_valid = True
    values_invalid = []

    list1 = values['-EMAIL_ADDRESS-']
    recipients = list1.split(" ")
    
    if len(recipients) >= 1:
        print(recipients)
        for email in recipients:
            if '@' not in email:
                response1 = (' ' + email + ' email address')
                values_invalid.append(str(response1))
                is_valid = False
    
    if len(values['-MESSAGE-']) == 0:
        values_invalid.append('MESSAGE')
        is_valid = False

    result = [is_valid, values_invalid]
    return result

def generate_error_message(values_invalid):
    error_message = ''
    for value_invalid in values_invalid:
        error_message += ('\nInvalid' + ':' + value_invalid)

    return error_message
if 'email_address_1' in locals():
    window["-EMAIL_ADDRESS-"].update(email_address_1)
if 'subject_1' in locals():
    window["-SUBJECT-"].update(subject_1)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    
    elif event == 'Send Email':
        validation_result = validate(values)
        if validation_result[0]:
            
            message = MIMEMultipart()
            emailinput = values['-EMAIL_ADDRESS-']
            recipients=[]
            recipients = emailinput.split(" ")
            message['To'] = ", ".join(recipients) 
            message['Subject'] = values['-SUBJECT-']
              
            message.attach(MIMEText(values['-MESSAGE-'], 'plain'))
            if len(files):
                for file in files:
                    with open(file, 'rb') as f:
                        ext = file.split('.')[-1:]
                        attachedfile = MIMEApplication(f.read(), _subtype = ext)
                        attachedfile.add_header('content-disposition', 'attachment', filename=basename(file))
                        message.attach(attachedfile)
                    
            message = message.as_string()

            email_sender.send_email(message, recipients)
            sg.popup_auto_close('EMAIL SENT!')
        else:
            error_message = generate_error_message(validation_result[1])
            sg.popup(error_message)
            
    elif event == "Versions":  # if versions button is pressed
        sg.popup_scrolled("Versions ",sg.get_versions()) #open window with versions data
    #Help - about menu    
    elif event == "About":  #if versions button is pressed
        sg.popup("About","Email Sender Utility GUI created using PySimpleGUI.\nThis program uses the a email sender app to send its data inputed in the fields.\nFor Project 4 final Assigment.\nBy: A00272236")
        #open about data window
    elif event == "Clear":
        window["-EMAIL_ADDRESS-"].update("")
        window["-MESSAGE-"].update("")
        window["-SUBJECT-"].update("")
        receivers=[]
    elif event == "Remove Attachments":
        window["-STAT-"].update("")
        files=[]
        listlength=[]
        stat_format=""
        
    elif event == "Attach File":   #if open button is pressed     
        data_pathname = sg.popup_get_file("Select the file to send\nFiles above 25MB will be dropped by the Gmail servers","Open File")  #open a file selecter
               
        # change the status bar
        try:
            filename = os.path.basename(data_pathname)
            listlength.append(filename)
            if len(listlength) == 1:
                stat_format+=(filename)
            else:
                stat_format+=(", "+filename)
            window["-STAT-"].update("Attached File: "+ stat_format)
            files.append(data_pathname)
            print(data_pathname)
        except:
            pass

window.close()

