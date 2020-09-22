from qa327.frontend import app
import webbrowser
import os

FLASK_PORT = 8081

if __name__ == "__main__":
    app.run(debug=True, port=FLASK_PORT)
