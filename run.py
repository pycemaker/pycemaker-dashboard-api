from app import get_flask_app
# from flask_cors import CORS

if __name__ == '__main__':
    # Main entry point when run in stand-alone mode.
    app = get_flask_app()
    # CORS(app)
    app.run(debug=True)
