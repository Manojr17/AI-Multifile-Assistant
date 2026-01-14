# Main Flask application for AI-Based Smart File Assistant
# Refactored and organized version

from flask import Flask
from flask_cors import CORS
import os

# Import configuration
from config import Config
# Import database initialization
from database import init_db

# Import route modules
from routes.main_routes import register_main_routes
from routes.api_routes import register_api_routes
from routes.auth_routes import register_auth_routes

# Import OpenAI client initialization
from openai import OpenAI

# Initialize Flask app
app = Flask(__name__)
CORS(app)
# Configure Flask app
app.secret_key = Config.SECRET_KEY

# Ensure upload folder exists
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

# Initialize OpenAI client
if Config.OPENAI_API_KEY:
    client = OpenAI(api_key=Config.OPENAI_API_KEY)
    print("✅ OpenAI client initialized")
else:
    client = None
    print("⚠️  OpenAI API key not found - running in demo mode")

# Register all routes
register_main_routes(app)
register_api_routes(app)
register_auth_routes(app)

# Initialize database
print("🔧 Initializing database...")
init_db()

if __name__ == "__main__":
    # Ensure all existing users have individual Pinecone indexes
    print("🔧 Ensuring all users have individual Pinecone indexes...")
    # from pinecone_manager import ensure_all_users_have_indexes
    # ensure_all_users_have_indexes()  # Temporarily commented out
    
    # Run with reloader disabled to prevent interruptions during processing
    print("🚀 Starting Flask app without auto-reloader...")
    app.run(debug=True, use_reloader=False, host="127.0.0.1", port=5000)