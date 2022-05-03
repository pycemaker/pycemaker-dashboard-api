from app import get_flask_app
# from flask_cors import CORS

app = get_flask_app()

if __name__ == '__main__':
    # Main entry point when run in stand-alone mode.
    # CORS(app)
    app.run(debug=True)
