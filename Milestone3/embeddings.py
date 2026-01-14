# Embedding generation functionality for the AI-Based Smart File Assistant
import random
from config import Config

# Try to import sentence transformers and pre-load model
SENTENCE_TRANSFORMERS_AVAILABLE = False
embedding_model = None

def get_embedding_model():
    """Get or initialize the embedding model"""
    global embedding_model
    if embedding_model is None:
        try:
            from sentence_transformers import SentenceTransformer
            print("🔄 Loading MiniLM embedding model...")
            embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
            print("✅ MiniLM embedding model loaded successfully")
            global SENTENCE_TRANSFORMERS_AVAILABLE
            SENTENCE_TRANSFORMERS_AVAILABLE = True
        except Exception as e:
            print(f"⚠️  Failed to load MiniLM model: {e}")
            embedding_model = None
    return embedding_model

def generate_embedding_miniLM(text):
    """Generate embedding using MiniLM model (same as Milestone2) with fallback"""
    try:
        model = get_embedding_model()
        if model and SENTENCE_TRANSFORMERS_AVAILABLE:
            embedding = model.encode(text).tolist()
            print(f"✅ Generated MiniLM embedding (length: {len(embedding)})")
            return embedding
        else:
            # Fallback to mock embedding with correct dimensions
            random.seed(hash(text) % (2**32))
            mock_embedding = [random.uniform(-1, 1) for _ in range(Config.EMBEDDING_DIMENSION)]
            print(f"🔧 Generated mock embedding (length: {len(mock_embedding)})")
            return mock_embedding
    except Exception as e:
        print(f"❌ Error generating embedding: {str(e)}")
        # Final fallback
        random.seed(hash(text) % (2**32))
        mock_embedding = [random.uniform(-1, 1) for _ in range(Config.EMBEDDING_DIMENSION)]
        return mock_embedding

# Pre-load the model at startup to avoid issues during processing
# Commented out to speed up startup - model will be loaded on first use
# print("🔧 Pre-loading embedding model at startup...")
# get_embedding_model()