from gtts import gTTS
import os

def text_to_speech(text, filepath):
    """
    Convert text to speech and save to the specified filepath.
    
    Args:
        text (str): The text to convert to speech.
        filepath (str): The path where the audio file should be saved (e.g., 'static/audio/tts_output_123.mp3').
    
    Returns:
        str: The filepath where the audio was saved.
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Create TTS object and save to filepath
    tts = gTTS(text=text, lang='en')
    tts.save(filepath)
    
    return filepath