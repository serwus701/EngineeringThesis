import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import json
import constans


def read_status_from_json():
    try:
        with open('status.json', 'r') as f:
            status_json = json.load(f)
    except FileNotFoundError:
        status_json = {}
    return status_json


status = read_status_from_json()
global app_status_toggle
app_status_toggle = status.get("app_status", constans.app_status_toggle)
button_colors = constans.button_colors
buttons = []
dropdowns = []
recordings = constans.recordings
recorded_actions_availability = constans.recorded_actions_availability
recorded_actions_availability.update(status.get("action_availability", {}))

recordings_toggle = {}
for recording in recordings:
    recordings_toggle.update({recording: status.get("dropdowns", {}).get(recording, {}).get("active", "True")})


def add_new_recording_onclick():
    new_recording_name = new_recording_name_var.get()
    print("The name is : " + new_recording_name)
    new_recording_name_var.set("")

def on_close():
    save_status()
    root.destroy()


def app_status_onclick(on_button):
    global app_status_toggle
    app_status_toggle = not app_status_toggle
    app_status = "On" if app_status_toggle else "Off"
    on_button.config(text=app_status)


def save_status():
    status = {}
    dropdowns_status = {}
    recorded_actions_availability_status = {}

    for var, dropdown, element in dropdowns:
        dropdown_details = {}
        dropdown_details["value"] = var.get()
        dropdown_details["active"] = recordings_toggle.get(element)
        dropdowns_status[element] = dropdown_details
    for action, action_availability in recorded_actions_availability.items():
        recorded_actions_availability_status[action] = action_availability

    status["dropdowns"] = dropdowns_status
    status["action_availability"] = recorded_actions_availability_status
    status["app_status"] = app_status_toggle
    with open('status.json', 'w') as f:
        json.dump(status, f)


def on_button_click(i):
    recordings_toggle[recordings[i]] = not recordings_toggle[recordings[i]]
    next_color = "green" if recordings_toggle[recordings[i]] else "red"
    buttons[i].config(background=next_color)
    btn_text = "deactivate" if recordings_toggle[recordings[i]] else "activate"
    btn_text_var = tk.StringVar()
    btn_text_var.set(btn_text)
    buttons[i].config(textvariable=btn_text_var)


def on_select(event, action_var, last_action, element):
    new_action = action_var.get()
    old_action = last_action[0]
    if old_action is not None:
        recorded_actions_availability[old_action] = True
    else:
        recorded_actions_availability[status.get("dropdowns", {}).get(element, {}).get("value", "none")] = True
    if new_action != 'none':
        recorded_actions_availability[new_action] = False
    last_action[0] = new_action
    for var, dropdown, _ in dropdowns:
        dropdown['values'] = [action for action, available in recorded_actions_availability.items() if available]


# Utwórz okno główne
root = ThemedTk(theme="arc")  # Użyj motywu "arc"
root.geometry('600x800')  # Ustaw rozmiar okna
root.resizable(False, False)  # Uniemożliw zmianę rozmiaru okna
root.configure(bg='gray')  # Ustaw tło aplikacji na szare

# Utwórz ramkę do przechowywania widgetów
frame = ttk.Label(root, background='white')
frame.pack(fill='both', side='left')  # Przesuń ramkę na lewą stronę okna
frame.configure(relief='groove', borderwidth=6)  # Dodaj zaokrąglone rogi do ramki

for i, element in enumerate(recordings):
    label = ttk.Label(frame, text=element)
    label.grid(row=i, column=0, padx=5, pady=5)
    label.config(font=("Helvetica", 14))

    actions = [action for action, available in recorded_actions_availability.items() if available]
    action_var = tk.StringVar()
    action_dropdown = ttk.Combobox(frame, textvariable=action_var)
    action_dropdown['values'] = actions
    action_dropdown.grid(row=i, column=1, padx=5, pady=5)
    action_dropdown.config(font=("Helvetica", 14))
    action_dropdown.set(status.get("dropdowns", {}).get(element, {}).get("value", "none"))
    dropdowns.append((action_var, action_dropdown, element))

    button_frame = ttk.Frame(frame)  # Place button frame inside 'frame' instead of 'root'
    button_frame.grid(row=i, column=2, padx=5, pady=5, sticky='w')  # Adjust row and column, add padding

    start_text = "deactivate" if status.get("dropdowns", {}).get(element, {}).get("active", True) else "activate"
    button_var = tk.StringVar()
    button_var.set(start_text)
    start_color = "green" if status.get("dropdowns", {}).get(element, {}).get("active", True) else "red"

    button = tk.Button(button_frame, textvariable=button_var, command=lambda i=i: on_button_click(i),
                       background=start_color)
    button.pack(side='left')

    buttons.append(button)

    action_dropdown.bind('<<ComboboxSelected>>',
                         lambda event, action_var=action_var, last_action=[None], element=element: on_select(event,
                                                                                                             action_var,
                                                                                                             last_action,
                                                                                                             element))

# Add on/off button
on_button_frame = ttk.Frame(root)
app_status = "On" if app_status_toggle else "Off"
on_button_frame.pack(side='top', fill='x', pady=(20, 0))
on_button = tk.Button(on_button_frame, text=app_status)
on_button.config(command=lambda on_button=on_button: app_status_onclick(on_button))
on_button.pack(side='bottom', fill='both', padx=(30, 30), pady=(20, 20))

# Add new recording button
add_button_frame = ttk.Frame(root)
add_button_frame.pack(side='top', fill='x', pady=(20, 20))
add_button = tk.Button(add_button_frame, text="Add new recorded action", command=add_new_recording_onclick)
add_button.pack(side='bottom', fill='both', padx=(30, 30), pady=(5, 20))
new_recording_name_var = tk.StringVar()
name_entry = tk.Entry(add_button_frame, textvariable=new_recording_name_var, font=('calibre', 10, 'normal'))
name_entry.pack(side='bottom', fill='both', padx=(30, 30), pady=(5, 5))

text_var = tk.StringVar()
text_var.set("Fill name of new recording\nthen add new recording")
label = tk.Label(add_button_frame, textvariable=text_var)
label.pack(side='top', fill='both', padx=(30, 30), pady=(20, 5))

# Create a frame for the save button
save_button_frame = ttk.Frame(root)
save_button_frame.pack(side='bottom', fill='x', pady=(20, 40))

# Create the save button
save_button = tk.Button(save_button_frame, text="Save settings", command=save_status)
save_button.pack(side='bottom', fill='both', padx=(30, 30), pady=(20, 20))

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
