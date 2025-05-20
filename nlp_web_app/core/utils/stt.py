import os
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import time
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def speech_to_text(audio_file):
    """
    Convert audio file to text and save as a PDF.
    
    Args:
        audio_file: The uploaded audio file (Flask file object).
    
    Returns:
        tuple: (transcription text, path to saved PDF file)
    """
    # Ensure static/pdfs/ directory exists
    PDF_DIR = os.path.join('static', 'pdfs')
    os.makedirs(PDF_DIR, exist_ok=True)
    
    # Generate unique filename for PDF
    timestamp = int(time.time())
    pdf_filename = f"stt_output_{timestamp}.pdf"
    pdf_filepath = os.path.join(PDF_DIR, pdf_filename)
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.tmp') as temp_file:
        audio_file.save(temp_file.name)
        temp_filepath = temp_file.name
    
    try:
        # Convert audio to WAV using pydub
        audio = AudioSegment.from_file(temp_filepath)
        wav_filepath = temp_filepath + '.wav'
        audio.export(wav_filepath, format='wav')
        
        # Initialize recognizer
        recognizer = sr.Recognizer()
        
        # Transcribe audio
        with sr.AudioFile(wav_filepath) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
        
        # Create PDF with transcription
        doc = SimpleDocTemplate(pdf_filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        style = styles['BodyText']
        story = [Paragraph(text.replace('\n', '<br/>'), style)]
        doc.build(story)
        
        # Clean up temporary files
        os.remove(temp_filepath)
        os.remove(wav_filepath)
        
        return text, pdf_filepath
    
    except Exception as e:
        # Clean up temporary files if they exist
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)
        if os.path.exists(wav_filepath):
            os.remove(wav_filepath)
        raise Exception(f"Speech-to-Text failed: {str(e)}")