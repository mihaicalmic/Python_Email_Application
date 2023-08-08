#main program, run if bat file not working

import PySimpleGUI as sg
import os
import email_receiver
import webbrowser
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

def details_window(message):
    layout = [
                [sg.Text('From:'), sg.Text('', key='from')],
                [sg.Text('To:'), sg.Text('', key='to')],
                [sg.Text('Subject:'), sg.Text('', key='subject')],
                [sg.Text('Date:'), sg.Text('', key='date')],
                [sg.Multiline('', key='body', size=(80, 10), disabled=True)],
                [sg.StatusBar("", size=60, key="-STAT-",visible=False)],
                [sg.Button("Replay"),sg.Button('Open HTML',visible=False),sg.Button('Open Atachements',visible=False)],
            ]

    window = sg.Window('Email Viewer', layout, finalize=True)
    window['from'].update(message['from'])
    window['to'].update(message['to'])
    window['subject'].update(message['subject'])
    window['date'].update(message['date'])
    window['body'].update(message['body'])
    body = message['body']
    if "<!DOCTYPE html>" or "<div dir" in body: #Checks weather the content is HTML
        window.find_element('Open HTML').Update(visible=True)#Enables HTML Viewer Button
    if message['files']:
        window.find_element('-STAT-').Update(visible=True)
        window.find_element('Open Atachements').Update(visible=True)
        text1 = "Files attached:"
        for file in message['files']:
            text1 += " " + file
        window['-STAT-'].update(text1)
        
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            if 'path' in  locals():   #removes the fitered file folder if exists
                path = "filtered_files"
                shutil.rmtree(path)
            break
        elif event == "Open Atachements":
            #sg.popup_auto_close('Files','This will open the folder with the donwloaded files.')
            files = message['files']
            path = "Attachments"
            path = os.path.realpath(path)
            #os.startfile(path)
            new_dir = os.path.join(os.getcwd(), "filtered_files")
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)

            for file in os.listdir(path):
                if file in files:
                    shutil.copy(os.path.join(path, file), new_dir)

            os.startfile(new_dir) # open the new directory in File Explorer
            
        elif event == "Open HTML":
            folder_name = "Saved HTML"
            if not os.path.isdir(folder_name):
                # make a folder for this email (named after the subject)
                os.mkdir(folder_name)
                
            filename = "Page.html"
            filepath = os.path.join(folder_name, filename)
            check_file = os.path.isfile(filepath)
            if check_file != "True":
                filename = "Page.html"
                filepath = os.path.join(folder_name, filename)
                # write the file
                
                with open(filepath, "w", encoding="latin-1") as f:
                    f.write(body)
                # open in the default browser
                webbrowser.open(filepath)
            if check_file == "True":
                webbrowser.open(filepath)
        elif event == "Replay":
            to12 = message['from']
            sub12 = message['subject']
            subprocess.Popen(["python", "sender_interface.py", to12, sub12]) 
    

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


