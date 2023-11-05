import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import json

# Load status from file
try:
    with open('status.json', 'r') as f:
        status = json.load(f)
except FileNotFoundError:
    status = {}

# Hardkodowana lista elementów
recordings = ['rec1', 'rec2', 'rec3', 'rec4']
recordings_toggle = {}
for recording in recordings:
    recordings_toggle.update({recording: status.get("dropdowns", {}).get(recording, {}).get("active", "True")})

button_colors = ['red', 'green']
buttons = []
dropdowns = []

# Dostępność zarejestrowanych działań
recorded_actions_availability = {
    'act1': True,
    'act2': True,
    'act3': True,
    'act4': True,
    'none': True,
}

recorded_actions_availability.update(status.get("action_availability", {}))

# Utwórz okno główne
root = ThemedTk(theme="arc")  # Użyj motywu "arc"
root.geometry('600x800')  # Ustaw rozmiar okna
root.resizable(False, False)  # Uniemożliw zmianę rozmiaru okna
root.configure(bg='gray')  # Ustaw tło aplikacji na szare

# Utwórz ramkę do przechowywania widgetów
frame = ttk.Label(root, background='white')
frame.pack(fill='both', side='left')  # Przesuń ramkę na lewą stronę okna
frame.configure(relief='groove', borderwidth=6)  # Dodaj zaokrąglone rogi do ramki


def on_button_click(i):
    recordings_toggle[recordings[i]] = not recordings_toggle[recordings[i]]
    next_color = "green" if recordings_toggle[recordings[i]] else "red"
    buttons[i].config(background=next_color)


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

    button_var = tk.StringVar()
    button_var.set(element)

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


#
# # Utwórz przyciski, które zmieniają swoją wartość po każdym kliknięciu
# button_texts = ['App active', 'Button 2', 'Button 3', 'Button 4', 'Button 5']
# button_colors = ['red', 'green']
# buttons = []
# for i, button_text in enumerate(button_texts):
#     button_frame = ttk.Frame(root)
#     button_frame.pack(side='top', padx=10, pady=10)  # Umieść ramkę przycisku na górze okna z paddingiem
#
#     button_var = tk.StringVar()
#     button_var.set(button_text)
#
#
#     def on_button_click(i=i):
#         current_color = buttons[i].cget("background")
#         next_color = button_colors[1] if current_color == button_colors[0] else button_colors[0]
#         buttons[i].config(background=next_color)
#
#
#     button = tk.Button(button_frame, textvariable=button_var, command=on_button_click,
#                        background=status.get("buttons", {}).get(button_text, button_colors[0]))
#     button.pack(side='left')  # Umieść przycisk po lewej stronie ramki przycisku
#
#     label = ttk.Label(button_frame, text=button_text)
#     label.pack(side='right')  # Umieść etykietę po prawej stronie ramki przycisku
#
#     buttons.append(button)


def on_close():
    save_status()
    root.destroy()


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
    with open('status.json', 'w') as f:
        json.dump(status, f)


# Create a frame for the save button
save_button_frame = ttk.Frame(root)
save_button_frame.pack(side='right', fill='x')  # Place the save button frame at the top of the window with padding

# Create a label for the save button
save_button_label = ttk.Label(save_button_frame, text="Save Settings")
save_button_label.pack(side='top', fill='both')  # Place the label at the top of the save button frame

# Create the save button
save_button = tk.Button(save_button_frame, text="Save", command=save_status)
save_button.pack(side='bottom', fill='both')  # Place the button at the bottom of the save button frame

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
