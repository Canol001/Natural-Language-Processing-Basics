from flask import Flask
from core.routes import main

app = Flask(__name__)
app.register_blueprint(main)

# if __name__ == '__main__':
#     app.run(debug=True)
