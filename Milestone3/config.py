# Configuration settings for the AI-Based Smart File Assistant
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask settings
    SECRET_KEY = "supersecretkey"
    
    # Database settings
    DB_NAME = "database.db"
    
    # File upload settings
    UPLOAD_FOLDER = "static/uploads"
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx'}
    
    # API Keys
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Document processing configuration
    CHUNK_CONFIG = {
        "chunk_size": 2000,
        "chunk_overlap": 200,
        "min_chunk_length": 100,
        "max_chunks_per_doc": 500
    }
    
    # Embedding settings
    EMBEDDING_DIMENSION = 384  # MiniLM dimension
    
    # Demo mode (when no OpenAI API key)
    DEMO_MODE = not bool(OPENAI_API_KEY)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS