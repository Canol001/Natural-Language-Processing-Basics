import os
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import time
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet



def speech_to_text(audio_file):
    PDF_DIR = os.path.join('static', 'pdfs')
    os.makedirs(PDF_DIR, exist_ok=True)
    timestamp = int(time.time())
    pdf_filename = f"stt_output_{timestamp}.pdf"
    pdf_filepath = os.path.join(PDF_DIR, pdf_filename)
    
    # Save uploaded file to temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix='.tmp') as temp_file:
        audio_file.save(temp_file.name)
        temp_filepath = temp_file.name
    
    try:
        # Check file size (limit to 10MB to avoid memory issues)
        if os.path.getsize(temp_filepath) > 10 * 1024 * 1024:
            raise ValueError("Audio file is too large (max 10MB)")
        
        # Load audio with pydub
        audio = AudioSegment.from_file(temp_filepath)
        wav_filepath = temp_filepath + '.wav'
        
        # Export as WAV with consistent settings
        audio = audio.set_channels(1).set_frame_rate(16000)  # Mono, 16kHz for SpeechRecognition
        audio.export(wav_filepath, format='wav')
        
        # Transcribe audio
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_filepath) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
        
        # Generate PDF
        doc = SimpleDocTemplate(pdf_filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        story = [
            Paragraph("NLP Tool Suite: Speech-to-Text", styles['Title']),
            Paragraph(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']),
            Paragraph(text.replace('\n', '<br/>'), styles['BodyText'])
        ]
        doc.build(story)
        
        # Clean up temporary files
        os.remove(temp_filepath)
        os.remove(wav_filepath)
        
        return text, pdf_filename  # Return filename, not full path
    except ValueError as ve:
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)
        if os.path.exists(wav_filepath):
            os.remove(wav_filepath)
        raise ValueError(str(ve))
    except Exception as e:
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)
        if os.path.exists(wav_filepath):
            os.remove(wav_filepath)
        raise Exception(f"Speech-to-Text failed: {str(e)}")