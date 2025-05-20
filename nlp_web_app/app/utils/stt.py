import speech_recognition as sr
from fpdf import FPDF
import uuid
import os

def speech_to_text(file):
    recognizer = sr.Recognizer()
    audio_file_path = f"app/static/audio/{uuid.uuid4()}.wav"
    file.save(audio_file_path)

    with sr.AudioFile(audio_file_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)

    # Create PDF
    pdf_path = f"downloads/{uuid.uuid4()}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf.output(pdf_path)

    return text, pdf_path
