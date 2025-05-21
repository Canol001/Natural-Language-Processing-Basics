from pydub import AudioSegment
import speech_recognition as sr
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import time  # Import time module
import tempfile
import traceback
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def speech_to_text(audio_file):
    logger.debug(f"Processing audio file: {audio_file.filename}")
    
    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
        audio_file.save(temp_file.name)
        temp_path = temp_file.name
        logger.debug(f"Saved temporary file: {temp_path}")

    try:
        # Load and normalize audio with pydub
        logger.debug("Loading audio with pydub...")
        try:
            audio = AudioSegment.from_file(temp_path)
        except Exception as e:
            logger.error(f"Pydub failed to load audio: {str(e)}")
            raise Exception(f"Pydub error: {str(e)}")
        
        logger.debug("Normalizing audio...")
        audio = audio.set_channels(1).set_frame_rate(16000)  # Optimize for speech recognition
        audio.export(temp_path, format="wav")
        logger.debug("Audio exported as WAV")

        # Transcribe audio
        logger.debug("Initializing speech recognizer...")
        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_path) as source:
            logger.debug("Recording audio data...")
            audio_data = recognizer.record(source)
            logger.debug("Transcribing with Google API...")
            try:
                text = recognizer.recognize_google(audio_data)
            except sr.UnknownValueError:
                logger.error("Google API could not understand audio")
                raise Exception("Speech not recognized")
            except sr.RequestError as e:
                logger.error(f"Google API request failed: {str(e)}")
                raise Exception(f"Transcription service error: {str(e)}")
            logger.debug(f"Transcription: {text}")

        # Generate PDF
        logger.debug("Generating PDF...")
        pdf_dir = os.path.join('static', 'pdfs')
        os.makedirs(pdf_dir, exist_ok=True)
        pdf_filename = f"stt_output_{int(time.time())}.pdf"  # Fixed: os.time() → time.time()
        pdf_path = os.path.join(pdf_dir, pdf_filename)
        try:
            c = canvas.Canvas(pdf_path, pagesize=letter)
            c.drawString(100, 750, "Speech-to-Text Transcript")
            text_lines = text.split('\n')
            y = 700
            for line in text_lines:
                c.drawString(100, y, line[:80])  # Truncate long lines
                y -= 20
            c.save()
            logger.debug(f"PDF created: {pdf_path}")
        except Exception as e:
            logger.error(f"PDF generation failed: {str(e)}")
            raise Exception(f"PDF creation error: {str(e)}")

        # Clean up
        try:
            os.remove(temp_path)
            logger.debug(f"Deleted temporary file: {temp_path}")
        except Exception as e:
            logger.warning(f"Failed to delete temp file: {str(e)}")

        return text, pdf_filename

    except Exception as e:
        logger.error(f"Speech-to-text failed: {str(e)}")
        logger.error(traceback.format_exc())
        try:
            os.remove(temp_path)
        except:
            pass
        raise Exception(f"Speech-to-Text failed: {str(e)}")