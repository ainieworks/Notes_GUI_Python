# Step 1: Import required libraries
import json
from tkinter import *
from tkinter import messagebox
from datetime import datetime

# Step 2: Create main window
root = Tk()
root.title("Simple Notes App")
root.geometry("600x500")

# Step 3: Load existing notes
try:
    with open("data.json", "r") as file:
        notes = json.load(file)
except (FileNotFoundError, json.decoder.JSONDecodeError):
    notes = []

# Step 4: Create Entry widget for note input
entry = Entry(root, width=40, font=("Segoe UI", 12))
entry.pack(pady=10, padx=10)

# Step 5: Save or Update Note
editing_index = None  # global tracker

def save_note():
    global editing_index
    note = entry.get()
    if note.strip() == "":
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    if editing_index is not None:
        # Update existing note
        notes[editing_index]["text"] = note
        notes[editing_index]["timestamp"] = timestamp
        messagebox.showinfo("Updated", "Note updated successfully!")
        editing_index = None
        save_btn.config(text="Add Note")
    else:
        # Add new note
        note_obj = {
            "text": note,
            "timestamp": timestamp
        }
        notes.append(note_obj)
        messagebox.showinfo("Saved", "Your note was saved")

    with open("data.json", "w") as file:
        json.dump(notes, file, indent=2)

    entry.delete(0, END)
    load_notes(highlight_index=len(notes) - 1)

# Save button
save_btn = Button(root, text="Add Note", command=save_note, bg="#007acc", fg="white")
save_btn.pack(pady=5)

# Step 6: Delete note
def delete_note():
    selected_index = listbox.curselection()
    if not selected_index:
        messagebox.showwarning("No selection", "Please select a note to delete")
        return

    index = selected_index[0]
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this note?")
    if confirm:
        del notes[index]
        with open("data.json", "w") as file:
            json.dump(notes, file, indent=2)
        load_notes()
        messagebox.showinfo("Deleted", "Note deleted successfully!")

# Step 7: Edit note
def edit_note():
    global editing_index
    selected_index = listbox.curselection()
    if not selected_index:
        messagebox.showwarning("No selection", "Please select a note to edit")
        return

    index = selected_index[0]
    editing_index = index
    entry.delete(0, END)
    entry.insert(0, notes[index]["text"])
    save_btn.config(text="Update Note")

# Buttons for edit and delete
edit_button = Button(root, text="Edit Selected Note", command=edit_note, bg="#007acc", fg="white")
edit_button.pack(pady=5)

delete_btn = Button(root, text="Delete Selected Note", command=delete_note, bg="#007acc", fg="white")
delete_btn.pack(pady=5)

# Step 8: Display list of notes
frame = Frame(root)
frame.pack()

scrollbar = Scrollbar(frame, orient=VERTICAL)
listbox = Listbox(frame, width=50, yscrollcommand=scrollbar.set)
listbox.pack(side=LEFT, padx=10, pady=10)
scrollbar.pack(side=RIGHT, fill=Y)
scrollbar.config(command=listbox.yview)

# Step 9: Load notes into listbox
def load_notes(highlight_index=None):
    listbox.delete(0, END)
    for idx, note in enumerate(notes):
        display_text = note["text"]
        timestamp = note["timestamp"]
        listbox.insert(END, f"{idx+1}. {display_text} ({timestamp})")
        if highlight_index is not None and idx == highlight_index:
            listbox.itemconfig(idx, {'bg': 'yellow'})
            root.after(1000, lambda i=idx: listbox.itemconfig(i, {'bg': listbox.cget('background')}))

load_notes()

# Step 10: Start the GUI loop
root.mainloop()
