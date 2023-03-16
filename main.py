import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfFileReader, PdfFileMerger

class PDFMergerApp:
    def __init__(self):
        self.tags = self.load_tags()
        self.files = []
        self.root = tk.Tk()
        self.root.title("PDF Merger")
        self.create_gui()

    def load_tags(self):
        try:
            with open('tags.json', 'r') as file:
                tags = json.load(file)
        except FileNotFoundError:
            tags = {}
        return tags

    def select_files(self):
        selected_files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        for file in selected_files:
            if file not in self.files:
                self.files.append(file)
        self.update_file_listbox()

    def select_folder(self):
        folder = filedialog.askdirectory()
        for root, _, filenames in os.walk(folder):
            for filename in filenames:
                if filename.lower().endswith(".pdf"):
                    file = os.path.join(root, filename)
                    if file not in self.files:
                        self.files.append(file)
        self.update_file_listbox()

    def update_file_listbox(self):
        self.file_listbox.delete(0, tk.END)
        for file in self.files:
            file_name = os.path.basename(file)
            file_tag = self.tags.get(file, 'No Tags')
            display_name = f"{file_name[:20]}... ({file_tag})"
            self.file_listbox.insert(tk.END, display_name)

    def update_tag_listbox(self):
        self.tag_listbox.delete(0, tk.END)
        self.tag_listbox.insert(tk.END, "No Tags")
        for tag in sorted(set(self.tags.values())):
            self.tag_listbox.insert(tk.END, tag)

    def merge_pdf_files(self):
        selected_tags = [self.tag_listbox.get(idx) for idx in self.tag_listbox.curselection()]

        if not selected_tags:
            messagebox.showerror("Error", "No tags selected.")
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

        if not output_path:
            messagebox.showerror("Error", "No output file selected.")
            return

        merger = PdfFileMerger()

        for file in self.files:
            file_tag = self.tags.get(file)
            if file_tag in selected_tags or (file_tag is None and "No Tags" in selected_tags):
                with open(file, 'rb') as f:
                    merger.append(PdfFileReader(f))

        with open(output_path, "wb") as output_file:
            merger.write(output_file)

        messagebox.showinfo("Success", "PDF files merged successfully.")


    def clear_files(self):
        self.files.clear()
        self.update_file_listbox()

    def create_gui(self):
        tk.Label(self.root, text="PDF Files:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        tk.Button(self.root, text="Select Files", command=self.select_files).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Select Folder", command=self.select_folder).grid(row=0, column=2, padx=10, pady=10)
        tk.Button(self.root, text="Clear", command=self.clear_files).grid(row=0, column=3, padx=10, pady=10)
        self.file_listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE, width=60, height=10)
        self.file_listbox.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        tk.Label(self.root, text="Tags:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.tag_listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE, width=60, height=10)
        self.tag_listbox.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

        tk.Button(self.root, text="Merge PDFs", command=self.merge_pdf_files).grid(row=4, column=1, padx=10, pady=10)

        self.update_tag_listbox()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PDFMergerApp()
    app.run()

