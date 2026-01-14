# Pinecone operations for the AI-Based Smart File Assistant
import os
import re
import time
from pinecone import Pinecone
from config import Config
from database import get_db

# Initialize Pinecone
pc = Pinecone(api_key=Config.PINECONE_API_KEY)

def create_user_pinecone_index(user_id, email):
    """Create a unique Pinecone index for a user based on their email"""
    try:
        # Create a unique index name using email
        email_name = email.split('@')[0].replace('.', '').replace('-', '').replace('_', '')
        # Use only the email part, make it shorter and more unique
        index_name = f"{email_name}-docs".lower()
        
        # Ensure index name follows Pinecone naming conventions
        index_name = re.sub(r'[^a-z0-9-]', '', index_name)
        
        # Ensure index name is not too long (max 45 characters for Pinecone)
        if len(index_name) > 45:
            index_name = index_name[:45]
        
        # Check if index already exists (with timeout)
        try:
            existing_indexes = pc.list_indexes()
            existing_names = [idx.name for idx in existing_indexes]
        except Exception as e:
            print(f"⚠️  Could not list existing indexes: {str(e)}")
            # Return a fallback index name without creating
            return index_name
        
        if index_name not in existing_names:
            # Create the index with appropriate dimensions (with timeout handling)
            try:
                pc.create_index(
                    name=index_name,
                    dimension=Config.EMBEDDING_DIMENSION,
                    metric="cosine",
                    spec={
                        "serverless": {
                            "cloud": "aws",
                            "region": "us-east-1"
                        }
                    }
                )
                print(f"✅ Created Pinecone index: {index_name} for {email}")
            except Exception as create_error:
                print(f"⚠️  Could not create Pinecone index: {str(create_error)}")
                # Return the index name anyway - it might exist or be created later
                return index_name
        else:
            print(f"ℹ️  Pinecone index already exists: {index_name} for {email}")
        
        return index_name
    except Exception as e:
        print(f"❌ Error creating Pinecone index for {email}: {str(e)}")
        # Return a fallback index name based on user_id
        fallback_name = f"user{user_id}-docs"
        print(f"🔄 Using fallback index name: {fallback_name}")
        return fallback_name

def get_user_pinecone_index(user_id):
    """Get the Pinecone index for a specific user"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT index_name FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0]:
            return pc.Index(result[0])
        return None
    except Exception as e:
        print(f"❌ Error getting user Pinecone index: {str(e)}")
        return None

def delete_user_pinecone_index(index_name):
    """Delete a user's Pinecone index"""
    try:
        if index_name:
            pc.delete_index(index_name)
            print(f"🗑️  Deleted Pinecone index: {index_name}")
            return True
    except Exception as e:
        print(f"❌ Error deleting Pinecone index {index_name}: {str(e)}")
        return False

def check_user_pinecone_stats(user_id):
    """Check statistics of user's Pinecone index"""
    try:
        index = get_user_pinecone_index(user_id)
        if not index:
            return {"error": "No Pinecone index found"}
        
        # Get index stats
        stats = index.describe_index_stats()
        
        return {
            "total_vectors": stats.total_vector_count,
            "dimension": stats.dimension,
            "index_fullness": stats.index_fullness,
            "namespaces": stats.namespaces
        }
    except Exception as e:
        return {"error": str(e)}

def ensure_all_users_have_indexes():
    """Ensure all users in the database have individual Pinecone indexes"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Get all users without Pinecone indexes
        cursor.execute("SELECT id, email FROM users WHERE index_name IS NULL OR index_name = ''")
        users_without_indexes = cursor.fetchall()
        
        print(f"🔍 Found {len(users_without_indexes)} users without Pinecone indexes")
        
        for user in users_without_indexes:
            user_id, email = user
            print(f"🔧 Creating Pinecone index for user {user_id} ({email})")
            
            index_name = create_user_pinecone_index(user_id, email)
            
            if index_name:
                cursor.execute("UPDATE users SET index_name = ? WHERE id = ?", (index_name, user_id))
                print(f"✅ Created index {index_name} for user {user_id}")
            else:
                print(f"❌ Failed to create index for user {user_id}")
        
        conn.commit()
        conn.close()
        
        print(f"🎉 Finished ensuring all users have Pinecone indexes")
        return True
        
    except Exception as e:
        print(f"❌ Error ensuring users have indexes: {str(e)}")
        return False