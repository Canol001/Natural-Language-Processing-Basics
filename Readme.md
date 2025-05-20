# 🧠 NLP Tool Suite

A sleek and powerful web-based NLP toolkit that unleashes the power of language technologies like Text-to-Speech (TTS), Speech-to-Text (STT), Sentiment Analysis, and Language Detection — all wrapped in a stylish Tailwind UI.

## 🌐 Live Demo
*(Coming Soon – deploy it with platforms like Render, Vercel, or Heroku)*

---

## 🚀 Features

### 🎤 Text-to-Speech (TTS)
- Converts input text into human-like speech.
- Audio plays directly in the browser.
- Downloadable `.mp3` audio file provided after playback.

### 🎧 Speech-to-Text (STT)
- Uploads `.wav`, `.mp3`, or other supported audio formats.
- Converts speech to human-readable text.
- Generates a downloadable PDF transcript.

### 💬 Sentiment Analysis
- Detects whether input text is **Positive**, **Negative**, or **Neutral**.
- Powered by `TextBlob`.

### 🌍 Language Detection
- Detects the language of input text.
- Converts ISO codes into readable language names (e.g., `en` → English).

---

## 🛠️ Tech Stack

| Layer       | Technology                            |
|-------------|----------------------------------------|
| Frontend    | HTML, Tailwind CSS, Font Awesome       |
| Backend     | Python, Flask                          |
| NLP Engine  | `gTTS`, `SpeechRecognition`, `pydub`, `langdetect`, `textblob`, `reportlab` |
| Audio Tools | `ffmpeg`                               |
| Storage     | Local file system (`static/audio`, `static/pdfs`) |

---

## 📁 Project Structure