from ttkthemes import ThemedTk
import tkinter as tk

def validate_integer(value):
    if not value or value == "Num":
        return True
    try:
        int(value)
        return True
    except ValueError:
        return False

def on_entry_click(event, entry_widget, placeholder_text):
    if entry_widget.get() == placeholder_text:
        entry_widget.delete(0, "end")
        entry_widget.config(fg='black')  # Set text color to black

def on_focus_out(event, entry_widget, placeholder_text):
    if entry_widget.get() == "":
        entry_widget.insert(0, placeholder_text)
        entry_widget.config(fg='grey')  # Set text color to grey

def create_main_window():
    root = ThemedTk(theme="arc")  # Użyj motywu "arc"
    root.geometry('800x800')  # Ustaw rozmiar okna
    root.resizable(False, False)  # Uniemożliw zmianę rozmiaru okna
    root.configure(bg='royal blue')  # Ustaw tło aplikacji na szare
    root.title("Settings")  # Ustaw tytuł okna

    return root


def create_on_button_panel(main_window_root, app_status_toggle, app_status_onclick):
    on_button_frame = tk.ttk.Frame(main_window_root)
    on_button_frame.configure(borderwidth=3)
    app_status = "On" if app_status_toggle else "Off"
    on_button_frame.pack(side='top', fill='x', pady=(20, 0))
    on_button = tk.Button(on_button_frame, text=app_status)
    on_button.config(command=lambda on_button=on_button: app_status_onclick(on_button))
    on_button.pack(side='bottom', fill='both', padx=(30, 30), pady=(20, 20))


def create_add_recording_panel(main_window_root, add_new_recording_onclick, new_recording_name_var, repetitions_num_var):
    add_button_frame = tk.Frame(main_window_root)
    add_button_frame.pack(side='top', fill='x', pady=(20, 20))

    top_add_button_frame = tk.Frame(add_button_frame)
    top_add_button_frame.pack(side='top', fill='both', padx=(30, 30), pady=(20, 5), expand=True)

    text_var = tk.StringVar()
    text_var.set("Fill name of new recording\nand repetitions number\nthen add new recording")
    label = tk.Label(top_add_button_frame, textvariable=text_var)
    label.pack(side='left') # 
    # label.config(font=("Helvetica", 10))

    placeholder_text_num = "Num"
    placeholder_text = "Your gesture name"

    repetitions_num_var.set(placeholder_text_num)
    repetitions_num_entry = tk.Entry(
        top_add_button_frame,
        textvariable=repetitions_num_var, 
        validate="key", 
        validatecommand=(top_add_button_frame.register(validate_integer), '%P'),
        font=('calibre', 10, 'normal'), 
        fg='grey'
    )
    repetitions_num_entry.pack(side='right', fill='both', padx=(10, 10), pady=(5, 5))
    repetitions_num_entry.configure(font=("Helvetica", 14))
    repetitions_num_entry.bind('<FocusIn>', lambda event: on_entry_click(event, repetitions_num_entry, placeholder_text_num))
    repetitions_num_entry.bind('<FocusOut>', lambda event: on_focus_out(event, repetitions_num_entry, placeholder_text_num))

    add_button = tk.Button(add_button_frame, text="Add new recorded action", command=add_new_recording_onclick)
    add_button.pack(side='bottom', fill='both', padx=(30, 30), pady=(5, 20))

    new_recording_name_var.set(placeholder_text)
    name_entry = tk.Entry(
        add_button_frame, 
        textvariable=new_recording_name_var, 
        font=('calibre', 10, 'normal'), 
        fg='grey'
    )
    name_entry.pack(side='bottom', fill='both', padx=(30, 30), pady=(5, 5))
    name_entry.config(font=("Helvetica"))
    name_entry.bind('<FocusIn>', lambda event: on_entry_click(event, name_entry, placeholder_text))
    name_entry.bind('<FocusOut>', lambda event: on_focus_out(event, name_entry, placeholder_text))



def create_save_button_panel(main_window_root, save_status):
    save_button_frame = tk.ttk.Frame(main_window_root)
    save_button_frame.pack(side='bottom', fill='x', pady=(20, 40))

    save_button = tk.Button(save_button_frame, text="Save settings", command=save_status)
    save_button.pack(side='bottom', fill='both', padx=(30, 30), pady=(20, 20))

#\\\\\\\\\\\\\\\\\\\\

def create_dropdowns_frame(main_window_root):
    dropdowns_frame = tk.ttk.Label(main_window_root, background='light sky blue')
    dropdowns_frame.pack(fill='both', side='left', ipadx=(10))
    dropdowns_frame.configure(relief='groove', borderwidth=3)

    return dropdowns_frame


def create_recording_label(dropdowns_frame, recording_name, i):
    recording_name_label = tk.ttk.Label(dropdowns_frame, text=recording_name)
    recording_name_label.grid(row=i, column=0, padx=5, pady=5)
    recording_name_label.config(font=("Helvetica", 14))
    recording_name_label.configure(relief='groove', borderwidth=1, width=15)


def create_dropdowns(dropdowns_frame, recorded_actions_availability, i, status, recording_name, dropdowns_arr, on_select):
    actions = [action for action, available in recorded_actions_availability.items() if available]
    action_var = tk.StringVar()
    action_dropdown = tk.ttk.Combobox(dropdowns_frame, textvariable=action_var)
    action_dropdown['values'] = actions
    action_dropdown.grid(row=i, column=1, padx=5, pady=5)
    action_dropdown.config(font=("Helvetica", 14))
    action_dropdown.set(status.get("dropdowns", {}).get(recording_name, {}).get("value", "none"))
    dropdowns_arr[recording_name] = (action_var, action_dropdown, recording_name)

    action_dropdown.bind('<<ComboboxSelected>>',
                         lambda event, action_var=action_var, last_action=[None], element=recording_name: on_select(
                             event,
                             action_var,
                             last_action,
                             element))


def create_buttons(dropdowns_frame, i, status, recording_name, on_button_click, buttons_arr):
    button_frame = tk.ttk.Frame(dropdowns_frame)  # Place button frame inside 'frame' instead of 'root'
    button_frame.grid(row=i, column=2, padx=5, pady=5, sticky='w')  # Adjust row and column, add padding

    start_text = "deactivate" if status.get("dropdowns", {}).get(recording_name, {}).get("active", True) else "activate"
    button_var = tk.StringVar()
    button_var.set(start_text)
    start_color = "green" if status.get("dropdowns", {}).get(recording_name, {}).get("active", True) else "red"

    button = tk.Button(button_frame, textvariable=button_var, command=lambda recording_name=recording_name: on_button_click(recording_name),
                       background=start_color, relief="raised")  # Set the relief to "round" for a more rounded appearance
    button.pack(side='left')

    buttons_arr[recording_name] = button
