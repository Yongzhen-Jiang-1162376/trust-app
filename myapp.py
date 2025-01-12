from waitress import serve
from app import create_app
from dotenv import load_dotenv

# load_dotenv()

app = create_app()

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8080)
