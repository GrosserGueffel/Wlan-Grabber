import PySimpleGUI as sg
import subprocess
import os

sg.theme("Dark Grey")

helptext = (
    "there is no help *evil laughing*\n\nmade by Grosser_Gueffel (https://github.com/GrosserGueffel)"
)

data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="ignore").split('\n')
profiles = [i.split(":")[1][1:-1] for i in data if "Profil" in i]
profiles.pop(0)

layout = [
    [sg.Text("Wlan Grabber V1 by GG", size=(25, 1),font=("Fixedsys",22),relief=sg.RELIEF_RIDGE,text_color="lime")],
    [sg.Listbox(values=profiles,key="choosen",size=(40,len(profiles)))],
    [sg.InputText("<nothing selected>", key = "output_password",size = (42,1)),sg.Button("Copy",key="copy")],
    [sg.Button("Get",key="start"),sg.Button("Close",key="close"),sg.Text(),sg.Button("Help",key="help")]    
]

window = sg.Window('Wlan Grabber', layout, auto_size_text=False, auto_size_buttons=False, default_element_size=(20,1), text_justification='left',font=("Fixedsys"))

while True:
    event, values = window.read()

    if event in ('Exit', 'Quit','close', None):
        print("Debug: Exit")
        break

    elif event == "start":
        print("Debug: Get")
        choosen = str(values.get("choosen")).replace("['","").replace("']","").replace('["',"").replace('"]',"")
        print(choosen)
        if choosen != "[]":
            try:
                password = subprocess.check_output(f'netsh wlan show profiles "{choosen}" key=clear').decode("utf-8", errors="ignore").strip().split("\n")[31].split(":")
            except subprocess.CalledProcessError as error:
                sg.popup(f"A fatal Error occured\n{error}")
                print(f"ERROR: {error}")
                exit()
            try:
                password = str(password[1]).replace(" ","")
            except IndexError:
                password = "<no password set>"
        else: 
            password = "<nothing selected>"
        window["output_password"].update(password)
        window.refresh()

    elif event == "copy":
        print("Debug: Copy")
        if values.get("output_password") not in ["<nothing selected>","<no password set>"]:
            os.system(f"echo {str(password)} | clip")

    elif event == "help":
        print("Debug: Help")
        sg.popup(helptext,title="Help")