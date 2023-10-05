import PySimpleGUI as sg
import os
import webbrowser
import shutil
import subprocess

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
  