# from ttkthemes import ThemedTk
# import tkinter as tk

# def create_dropdowns_frame(main_window_root):
#     dropdowns_frame = tk.ttk.Label(main_window_root, background='light cyan')
#     dropdowns_frame.pack(fill='both', side='left', ipadx=(10))
#     dropdowns_frame.configure(relief='groove', borderwidth=3)

#     for i, recording_name in enumerate(recordings_toggle):
#         create_recording_label(dropdowns_frame, recording_name, i)
#         create_dropdowns(dropdowns_frame, recorded_actions_availability, i, status, recording_name,
#                                     dropdowns_arr, on_select)
#         create_buttons(dropdowns_frame, i, status, recording_name, on_button_click, buttons_arr)

#     return dropdowns_frame


# def create_recording_label(dropdowns_frame, recording_name, i):
#     recording_name_label = tk.ttk.Label(dropdowns_frame, text=recording_name)
#     recording_name_label.grid(row=i, column=0, padx=5, pady=5)
#     recording_name_label.config(font=("Helvetica", 14))
#     recording_name_label.configure(relief='groove', borderwidth=1, width=15)


# def create_dropdowns(dropdowns_frame, recorded_actions_availability, i, status, recording_name, dropdowns_arr, on_select):
#     actions = [action for action, available in recorded_actions_availability.items() if available]
#     action_var = tk.StringVar()
#     action_dropdown = tk.ttk.Combobox(dropdowns_frame, textvariable=action_var)
#     action_dropdown['values'] = actions
#     action_dropdown.grid(row=i, column=1, padx=5, pady=5)
#     action_dropdown.config(font=("Helvetica", 14))
#     action_dropdown.set(status.get("dropdowns", {}).get(recording_name, {}).get("value", "none"))
#     dropdowns_arr[recording_name] = (action_var, action_dropdown, recording_name)

#     action_dropdown.bind('<<ComboboxSelected>>',
#                          lambda event, action_var=action_var, last_action=[None], element=recording_name: on_select(
#                              event,
#                              action_var,
#                              last_action,
#                              element))


# def create_buttons(dropdowns_frame, i, status, recording_name, on_button_click, buttons_arr):
#     button_frame = tk.ttk.Frame(dropdowns_frame)  # Place button frame inside 'frame' instead of 'root'
#     button_frame.grid(row=i, column=2, padx=5, pady=5, sticky='w')  # Adjust row and column, add padding

#     start_text = "deactivate" if status.get("dropdowns", {}).get(recording_name, {}).get("active", True) else "activate"
#     button_var = tk.StringVar()
#     button_var.set(start_text)
#     start_color = "green" if status.get("dropdowns", {}).get(recording_name, {}).get("active", True) else "red"

#     button = tk.Button(button_frame, textvariable=button_var, command=lambda recording_name=recording_name: on_button_click(recording_name),
#                        background=start_color, relief="raised")  # Set the relief to "round" for a more rounded appearance
#     button.pack(side='left')

#     buttons_arr[recording_name] = button