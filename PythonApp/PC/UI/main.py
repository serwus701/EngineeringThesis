import tkinter as tk
import json
import constans
import add_new_recording
import structures

global new_recording_name_var
global app_status_toggle
global status
global recorded_actions_availability
global listed_recordings
buttons_arr = []
dropdowns_arr = []
recordings_toggle = {}
status_file_path = './status.json'


def read_status_from_json():
    try:
        with open(status_file_path, 'r') as f:
            status_json = json.load(f)
    except FileNotFoundError:
        status_json = {}
    return status_json

def train_and_send_new_model():
    pass


def add_new_recording_onclick():
    new_recording_name = new_recording_name_var.get()
    add_new_recording.collect_data(new_recording_name, 10)
    add_new_recording.build_and_train_NN(new_recording_name, 10)
    new_recording_name_var.set("")


def on_close(root):
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

    for var, dropdown, element in dropdowns_arr:
        dropdown_details = {}
        dropdown_details["value"] = var.get()
        dropdown_details["active"] = recordings_toggle.get(element)
        dropdowns_status[element] = dropdown_details
    for action, action_availability in recorded_actions_availability.items():
        recorded_actions_availability_status[action] = action_availability

    status["dropdowns"] = dropdowns_status
    status["action_availability"] = recorded_actions_availability_status
    status["app_status"] = app_status_toggle
    with open(status_file_path, 'w') as f:
        json.dump(status, f)


def on_button_click(i):
    recordings_toggle[listed_recordings[i]] = not recordings_toggle[listed_recordings[i]]
    next_color = "green" if recordings_toggle[listed_recordings[i]] else "red"
    buttons_arr[i].config(background=next_color)
    btn_text = "deactivate" if recordings_toggle[listed_recordings[i]] else "activate"
    btn_text_var = tk.StringVar()
    btn_text_var.set(btn_text)
    buttons_arr[i].config(textvariable=btn_text_var)


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
    for var, dropdown, _ in dropdowns_arr:
        dropdown['values'] = [action for action, available in recorded_actions_availability.items() if available]


if __name__ == '__main__':
    status = read_status_from_json()
    app_status_toggle = status.get("app_status", constans.app_status_toggle)
    listed_recordings = constans.listed_recordings
    recorded_actions_availability = constans.recorded_actions_availability
    recorded_actions_availability.update(status.get("action_availability", {}))

    for recording in listed_recordings:
        recordings_toggle.update({recording: status.get("dropdowns", {}).get(recording, {}).get("active", "True")})

    main_window_root = structures.create_main_window()

    dropdowns_frame = structures.create_dropdowns_frame(main_window_root)
    for i, recording_name in enumerate(listed_recordings):
        structures.create_recording_label(dropdowns_frame, recording_name, i)
        structures.create_dropdowns(dropdowns_frame, recorded_actions_availability, i, status, recording_name,
                                    dropdowns_arr, on_select)
        structures.create_buttons(dropdowns_frame, i, status, recording_name, on_button_click, buttons_arr)

    structures.create_on_button_panel(main_window_root, app_status_toggle, app_status_onclick)
    new_recording_name_var = tk.StringVar()

    structures.create_add_recording_panel(main_window_root, add_new_recording_onclick, new_recording_name_var)
    structures.create_save_button_panel(main_window_root, save_status)

    main_window_root.protocol("WM_DELETE_WINDOW", lambda root=main_window_root: on_close(root))
    main_window_root.mainloop()