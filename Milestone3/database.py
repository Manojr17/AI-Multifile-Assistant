# Database operations for the AI-Based Smart File Assistant
import sqlite3
import hashlib
from config import Config

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(Config.DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            profile_picture TEXT,
            index_name TEXT
        )
    """)
    
    # Add index_name column if it doesn't exist (for existing databases)
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN index_name TEXT")
        print("Added index_name column to existing users table")
    except sqlite3.OperationalError:
        # Column already exists
        pass
    
    # Documents table for file uploads
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            filename TEXT NOT NULL,
            original_filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            file_size INTEGER,
            file_type TEXT,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            processing_stats TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    # Add processing_stats column if it doesn't exist (for existing databases)
    try:
        cursor.execute("ALTER TABLE documents ADD COLUMN processing_stats TEXT")
        print("Added processing_stats column to existing documents table")
    except sqlite3.OperationalError:
        # Column already exists
        pass
    
    # Chat history table for user-specific chat storage
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message_type TEXT NOT NULL,
            message_content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed_password):
    """Verify password against hash"""
    return hash_password(password) == hashed_password

def save_chat_message(user_id, message_type, message_content):
    """Save chat message to user's chat history"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO chat_history (user_id, message_type, message_content)
            VALUES (?, ?, ?)
        """, (user_id, message_type, message_content))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error saving chat message: {str(e)}")
        return False

def get_user_chat_history(user_id, limit=50):
    """Get user's chat history"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT message_type, message_content, timestamp
            FROM chat_history
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (user_id, limit))
        
        messages = []
        for row in cursor.fetchall():
            messages.append({
                'type': row[0],
                'content': row[1],
                'timestamp': row[2]
            })
        
        conn.close()
        return list(reversed(messages))  # Return in chronological order
    except Exception as e:
        print(f"❌ Error getting chat history: {str(e)}")
        return []

def check_user_has_documents(user_id):
    """Check if user has uploaded any documents"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM documents WHERE user_id = ?", (user_id,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    except Exception as e:
        print(f"❌ Error checking user documents: {str(e)}")
        return False