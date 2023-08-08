from email_receiver import authenticate
import PySimpleGUI as sg
import os
import webbrowser

sg.theme("Topanga")
#create menu layout
menu_def =  [ 
                ["Help",["About","Can't Authenticate?","Access Website"]]
            ]

# Define the layout of the login window
layout = [
    [sg.Menu(menu_def,background_color='grey')],
    [sg.Image('logo1.png', size=(150,75))], 
    [sg.Text("Sign in",font=("Helvetica", 18),justification="center")],
    [sg.Text("Use your Google Account",font=("Helvetica", 15))],
    [sg.Push(),sg.Text('Email:'), sg.InputText(key='-username-')],
    [sg.Text('Password:'), sg.InputText(password_char='*',key='-password-')],
    [sg.Button('Login'), sg.Button('Register')]
]

# Create the login window
window = sg.Window('Login Window', layout)
auth=0
# Event loop for the login window
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        window.close()
        exit()
    elif event == 'Login':
        email = window["-username-"].get()
        password = window["-password-"].get()
        with open("data.txt", 'w') as file:
            file.write(email + "," + password + "\n")
        try:
            mail = authenticate()
            auth = 1
        except:
           sg.popup_auto_close('Error','Incorect login details, Try Again')
        
        if auth == 1:
            os.system("python Integrate.py")
            break
        
    elif event == 'Register':
        webbrowser.open("https://accounts.google.com/SignUp")
        
    elif event == 'About':
        sg.popup("About","Welcome to PROMAIL.\nAuthentication for GMAIL acounts only.\nEnjoy this professional software, brought to you by Mihail Calmic.")
    elif event == 'Can\'t Authenticate?':
        sg.popup("Instructions","1.)Create a Gmail account by clicking Register.\n2.)Enable 2-Step Verification on the Security section of Manage your Google Account.\n3.)Create an App passwords and use that for authentication.\n4.)For more details click in Access Website under Help.")
    elif event == 'Access Website':
        webbrowser.open('https://support.google.com/mail/answer/185833?hl=en')



