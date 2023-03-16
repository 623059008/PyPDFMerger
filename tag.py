import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json

class PDFTagger:
    def __init__(self):
        self.tags = self.load_tags()
        self.selected_files = {}

        self.window = tk.Tk()
        self.window.title("PDF Selector")

        self.create_widgets()
        self.window.mainloop()

    def create_widgets(self):
        select_files_button = tk.Button(self.window, text="Select PDF files", command=self.select_pdf_files)
        select_files_button.pack()

        tk.Label(self.window, text="Selected PDFs and descriptions:").pack()
        self.listbox = tk.Listbox(self.window, width=80, selectmode=tk.EXTENDED)
        self.listbox.pack()

        tk.Label(self.window, text="Enter a description for the selected PDF(s):").pack()

        self.description_var = tk.StringVar()
        description_entry = tk.Entry(self.window, textvariable=self.description_var, width=80)
        description_entry.pack()

        update_description_button = tk.Button(self.window, text="Update description", command=self.update_description)
        update_description_button.pack()

        clear_selected_files_button = tk.Button(self.window, text="Clear selected PDF files", command=self.clear_selected_files)
        clear_selected_files_button.pack()

    def load_tags(self):
        try:
            with open('tags.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_tags(self):
        with open('tags.json', 'w') as f:
            json.dump(self.tags, f)

    def format_listbox_entry(self, file_path, description):
        file_name = os.path.basename(file_path)
        truncated_file_name = (file_name[:20] + '...') if len(file_name) > 20 else file_name
        return f"{truncated_file_name} - {description}"

    def select_pdf_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])

        for file_path in file_paths:
            if file_path and file_path not in self.selected_files:
                self.selected_files[file_path] = self.tags.get(file_path, "")
                self.listbox.insert(tk.END, self.format_listbox_entry(file_path, self.selected_files[file_path]))

    def update_description(self):
        selected_indices = self.listbox.curselection()

        if not selected_indices:
            messagebox.showwarning("Warning", "No PDF file(s) selected.")
            return

        new_description = self.description_var.get()

        for index in selected_indices:
            selected_file_path = list(self.selected_files.keys())[index]
            self.selected_files[selected_file_path] = new_description
            self.tags[selected_file_path] = new_description
            self.listbox.delete(index)
            self.listbox.insert(index, self.format_listbox_entry(selected_file_path, new_description))

        self.save_tags()
        # messagebox.showinfo("Info", f"Updated description for {len(selected_indices)} PDF file(s): {new_description}")

    def clear_selected_files(self):
        self.selected_files.clear()
        self.listbox.delete(0, tk.END)
        # messagebox.showinfo("Info", "Cleared selected PDF files.")

if __name__ == "__main__":
    app = PDFTagger()
