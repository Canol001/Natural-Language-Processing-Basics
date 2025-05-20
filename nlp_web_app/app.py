from flask import Flask
from core.routes import main

os.makedirs('static/audio', exist_ok=True)
os.makedirs('static/pdfs', exist_ok=True)

app = Flask(__name__)
app.register_blueprint(main)
