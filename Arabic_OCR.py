import tkinter as tk
from tkinter import filedialog, Text, Scrollbar
from tkinterdnd2 import DND_FILES, TkinterDnD
from pdf2image import convert_from_path
from pytesseract import image_to_string
from PIL import Image

def extract_text_from_image(image_path, lang='ara'):
    return image_to_string(Image.open(image_path), lang=lang)

def extract_text_from_pdf(pdf_path, lang='ara'):
    images = convert_from_path(pdf_path)
    text_output = ""
    for image in images:
        text = image_to_string(image, lang=lang)
        text_output += text + "\n\n"
    return text_output

def upload_file(file_path=None):
    if not file_path:
        file_path = filedialog.askopenfilename()
    if file_path:
        if file_path.lower().endswith('.pdf'):
            extracted_text = extract_text_from_pdf(file_path)
        else:
            extracted_text = extract_text_from_image(file_path)

        text_display.delete(1.0, tk.END)
        text_display.insert(tk.END, extracted_text)
        copy_to_clipboard(extracted_text)

def drop(event):
    file_path = event.data
    if file_path:
        upload_file(file_path.strip('{}'))

def copy_to_clipboard(text):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()  # Keeps the clipboard content even after the application is closed

# Set up the main application window
root = TkinterDnD.Tk()
root.title("OCR Text Extractor")

# Create a frame for the text display with a scrollbar
text_frame = tk.Frame(root)
text_frame.pack(fill=tk.BOTH, expand=True)

# Add a scrollbar to the text frame
scrollbar = Scrollbar(text_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a text widget to display the extracted text
text_display = Text(text_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
text_display.pack(fill=tk.BOTH, expand=True)
text_display.tag_configure("right", justify='right')
scrollbar.config(command=text_display.yview)

# Create a button to upload and process the file
upload_button = tk.Button(root, text="Upload File", command=upload_file)
upload_button.pack(pady=20)

# Bind the drag-and-drop event to the drop function
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', drop)

# Run the application
root.geometry("800x600")
root.mainloop()
