### By C.A. ###
# Works by finding the term "a/b" (ie. 3/20) on the last line of each page, deletes all duplicates but the last one, leaving the final "phased in" PDF
# Should function propeerly as long as you maintain the page counter on the bottom right corner of the slides.
# Last line defined as bottommost line when read, ie ('MECH-383 (F A 2024), McGill University', 'Applied Electronics and Instrumentation22/26'])
import os
import re
import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfReader, PdfWriter

def get_downloads_folder():
    return os.path.join(os.path.expanduser('~'), 'Downloads')

def upload_pdf():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select a PDF file", 
        filetypes=[("PDF files", "*.pdf")]
    )
    return file_path

def process_pdf(input_path, output_path):
    reader = PdfReader(input_path)
    writer = PdfWriter()
    slide_seen = {}

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        lines = text.splitlines()

        if len(lines) > 0:
            last_lines = lines[-1:]
            
            for line in last_lines:
                match = re.search(r'(\d+)/(\d+)', line)
                if match:
                    slide_num = int(match.group(1))
                    total_slides = int(match.group(2))

                    if slide_num not in slide_seen:
                        slide_seen[slide_num] = i
                    else:
                        slide_seen[slide_num] = i

    for slide_num in sorted(slide_seen):
        writer.add_page(reader.pages[slide_seen[slide_num]])

    with open(output_path, 'wb') as output_pdf:
        writer.write(output_pdf)

if __name__ == "__main__":
    pdf_path = upload_pdf()

    if pdf_path:
        downloads_folder = get_downloads_folder()
        base_filename = os.path.basename(pdf_path)
        filename_without_ext = os.path.splitext(base_filename)[0]
        output_pdf_path = os.path.join(downloads_folder, f'{filename_without_ext}_cleaned.pdf')
        process_pdf(pdf_path, output_pdf_path)
        print(f"Processed PDF saved to: {output_pdf_path}")
    else:
        print("No file selected.")
