from qa327 import create_app

FLASK_PORT = 8081

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=FLASK_PORT)
