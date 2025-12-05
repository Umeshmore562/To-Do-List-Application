import customtkinter as ctk
from tkinter import messagebox
import json
import os

ctk.set_appearance_mode("Dark") 
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("Futuristic To-Do Dashboard")
root.geometry("550x650")

TASK_FILE = "tasks.json"

if os.path.exists(TASK_FILE):
    with open(TASK_FILE, "r") as f:
        tasks = json.load(f)
else:
    tasks = []

def save_tasks():
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f)

def refresh_tasks():
    for widget in tasks_frame.winfo_children():
        widget.destroy()

    for idx, task in enumerate(tasks):
        frame = ctk.CTkFrame(tasks_frame, corner_radius=15, fg_color="#2b2b3c")
        frame.pack(pady=8, fill="x", padx=10)

        label_text = f"✔ {task['task']}" if task.get("done") else task['task']
        label = ctk.CTkLabel(frame, text=label_text, anchor="w", font=("Orbitron", 14))
        label.pack(side="left", padx=10, pady=10, expand=True, fill="x")

        btn_done = ctk.CTkButton(
            frame,
            text="Done" if not task.get("done") else "Undo",
            width=70,
            fg_color="#00ffea" if not task.get("done") else "#ffcc00",
            hover_color="#00ffe0" if not task.get("done") else "#ffd633",
            command=lambda i=idx: toggle_done(i)
        )
        btn_done.pack(side="right", padx=5)

        btn_remove = ctk.CTkButton(
            frame,
            text="Remove",
            width=70,
            fg_color="#ff007f",
            hover_color="#ff4db8",
            command=lambda i=idx: remove_task(i)
        )
        btn_remove.pack(side="right", padx=5)

def add_task():
    task_name = entry_task.get().strip()
    if task_name:
        tasks.append({"task": task_name, "done": False})
        entry_task.delete(0, ctk.END)
        save_tasks()
        refresh_tasks()
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

def remove_task(index):
    removed = tasks.pop(index)
    save_tasks()
    refresh_tasks()
    messagebox.showinfo("Removed", f"Task '{removed['task']}' removed!")

def toggle_done(index):
    tasks[index]["done"] = not tasks[index]["done"]
    save_tasks()
    refresh_tasks()

label = ctk.CTkLabel(root, text="To-Do Dashboard", font=("Orbitron", 24))
label.pack(pady=20)

frame_input = ctk.CTkFrame(root)
frame_input.pack(pady=10, fill="x", padx=10)

entry_task = ctk.CTkEntry(frame_input, placeholder_text="Enter new task")
entry_task.pack(side="left", padx=10, pady=10, fill="x", expand=True)

btn_add = ctk.CTkButton(frame_input, text="Add", width=80, fg_color="#00ffea",
                        hover_color="#00ffe0", command=add_task)
btn_add.pack(side="left", padx=5)

tasks_frame = ctk.CTkScrollableFrame(root, width=500, height=450)
tasks_frame.pack(pady=10)

entry_task.bind("<Return>", lambda e: add_task())

refresh_tasks()
root.mainloop()
