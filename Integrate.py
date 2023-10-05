#main program, run if bat file not working

import PySimpleGUI as sg
import os
import email_receiver
from open_contents import details_window
import shutil
import subprocess

try:
    message = email_receiver.get_inbox(filter1="UNSEEN") 
except: 
    exit()

    

layout = [
    [sg.Text("Welcome to",font=("Arial",14),text_color='purple')],
    [sg.Text("PROMAIL", font=("Helvetica", 24),text_color='purple'), sg.Push(),sg.Button("LOG OUT",button_color='red', size=(10, 2))],
    [sg.Push(),sg.Text("Searchbox",text_color='yellow'),sg.InputText('', key='-SEARCH-', size=(74, 1)),sg.Button("Search")],
    [
        sg.Column([
            [sg.Button("Send a email", size=(15, 2))],
            [sg.Button("Inbox", size=(15, 2))],
            [sg.Button("NEW EMAILS", size=(15, 2))],
            [sg.Button("Sent Emails", size=(15, 2))],
            [sg.Button("Draft Message", size=(15, 2))],
        ], element_justification='left'),
        sg.HSeparator(),
        sg.Column([
            [sg.Listbox(values=([("From:",msg['from'], "Subject:", msg['subject'],"Date:", msg['date']) for msg in message]),
                        size=(80, 15), key="-LIST-", enable_events=True)],
            [sg.StatusBar("Curently in the New Emails Folder", size=60, key="-STAT-")],
            [sg.Button("Close")]
        ])
    ]
]

window = sg.Window("PROMAIL", layout)

current_message_index = 0

def open_sender():
    #os.system('cmd /c "python sender_interface.py"')  //either works, what is different
    #os.system("python sender_interface.py")
    subprocess.Popen(["python", "sender_interface.py"]) 


while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == "Close":
        try:
            path = "Attachments"
            path = os.path.realpath(path)
            shutil.rmtree(path)    #remove all Attachments from the folder
        except:
            pass
        try:
            path = "Saved HTML"
            path = os.path.realpath(path)
            shutil.rmtree(path)    #remove all HTML from the folder
        finally:
            break
    elif event == "-LIST-":
        try:
            selected_email = values["-LIST-"][0][5] # access first element of tuple
        except:
            sg.popup_auto_close('Info','No new emails, come again later.')
        #print(selected_email) #print the message part of time to identify whick to display using details_window 
        for i, msg in enumerate(message):
            if msg['date'] == selected_email:
                current_message_index = i
                details_window(message[current_message_index])
                break
    
    elif event == "Inbox":
            message = email_receiver.get_inbox(filter1="ALL")
            window["-LIST-"].update("")
            window["-LIST-"].update(values=([("From:",msg['from'], "Subject:", msg['subject'],"Date:", msg['date']) for msg in message])) # update listbox
            window['-STAT-'].update("Curently in the Inbox Folder")
    
    elif event == "Send a email":
            print("Sender coming up.")
            open_sender()
    elif event == "NEW EMAILS":
        message = email_receiver.get_inbox(filter1="UNSEEN")
        window["-LIST-"].update("")
        window["-LIST-"].update(values=([("From:",msg['from'], "Subject:", msg['subject'],"Date:", msg['date']) for msg in message]))
        window['-STAT-'].update("Curently in the New Emails Folder")
    elif event == "Sent Emails":
        message = email_receiver.get_sent(filter1="ALL")
        window["-LIST-"].update("")
        window["-LIST-"].update(values=([("To:",msg['to'], "Subject:", msg['subject'],"Date:", msg['date']) for msg in message]))
        window['-STAT-'].update("Curently in the Sent Emails Folder")
    elif event == "Draft Message":
        sg.popup_auto_close('In Development','Very soon to be implemented, before 2024 or 2025.')
    elif event == "Search":
        searchtext = window["-SEARCH-"].get()
        filter1=('BODY "'+searchtext+'"')
        message = email_receiver.get_inbox(filter1)
        window["-LIST-"].update("")
        window["-LIST-"].update(values=([("From:",msg['from'], "Subject:", msg['subject'],"Date:", msg['date']) for msg in message])) # update listbox
        window['-STAT-'].update("Curently displaying the searched term")
    elif event == "LOG OUT":
        os.remove("data.txt")
        sg.popup_auto_close('Info','Logging Out, Start the program agin to LOG IN')
        exit()
        

window.close()


