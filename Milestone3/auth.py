# Authentication functionality for the AI-Based Smart File Assistant
from flask import request, jsonify, session, redirect, url_for
from database import get_db, hash_password, verify_password
from pinecone_manager import create_user_pinecone_index

def signup():
    """Handle user registration"""
    conn = None
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        first_name = data.get("first_name", "").strip()
        last_name = data.get("last_name", "").strip()
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")
        
        # Validation
        if not all([first_name, last_name, email, password]):
            return jsonify({"success": False, "message": "All fields are required"}), 400
        
        if len(password) < 6:
            return jsonify({"success": False, "message": "Password must be at least 6 characters"}), 400
        
        # Check if email already exists
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            conn.close()
            return jsonify({"success": False, "message": "Email already registered"}), 409
        
        # Hash password and create user
        hashed_password = hash_password(password)
        
        cursor.execute("""
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (?, ?, ?, ?)
        """, (first_name, last_name, email, hashed_password))
        
        user_id = cursor.lastrowid
        conn.commit()
        
        print(f"✅ User created successfully: {email} (ID: {user_id})")
        
        # Create individual Pinecone index for the user (non-blocking)
        print(f"🔧 Creating Pinecone index for new user {user_id} ({email})")
        try:
            index_name = create_user_pinecone_index(user_id, email)
            
            if index_name:
                # Update user record with Pinecone index name
                cursor.execute("UPDATE users SET index_name = ? WHERE id = ?", (index_name, user_id))
                conn.commit()
                print(f"✅ Pinecone index created and linked: {index_name}")
            else:
                print(f"⚠️  Failed to create Pinecone index for user {user_id} - user can still use the system")
        except Exception as pinecone_error:
            print(f"⚠️  Pinecone index creation failed for user {user_id}: {str(pinecone_error)} - user can still use the system")
        
        conn.close()
        
        # Set session
        session["user_id"] = user_id
        session["user_name"] = first_name
        session["user_email"] = email
        
        return jsonify({
            "success": True, 
            "message": "Account created successfully", 
            "redirect": "/dashboard"
        }), 201
        
    except Exception as e:
        if conn:
            conn.close()
        print(f"❌ Signup error: {str(e)}")
        return jsonify({"success": False, "message": f"Registration failed: {str(e)}"}), 500

def login():
    """Handle user login"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")
        
        if not email or not password:
            return jsonify({"success": False, "message": "Email and password are required"}), 400
        
        # Check credentials
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, first_name, last_name, email, password FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        if user and verify_password(password, user["password"]):
            # Set session
            session["user_id"] = user["id"]
            session["user_name"] = user["first_name"]
            session["user_email"] = user["email"]
            
            conn.close()
            print(f"✅ User logged in successfully: {email}")
            return jsonify({"success": True, "message": "Login successful", "redirect": "/dashboard"}), 200
        else:
            conn.close()
            return jsonify({"success": False, "message": "Invalid credentials"}), 401
            
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        return jsonify({"success": False, "message": f"Login failed: {str(e)}"}), 500

def logout():
    """Handle user logout"""
    session.clear()
    return redirect(url_for("home"))

def require_auth(f):
    """Decorator to require authentication for routes"""
    def decorated_function(*args, **kwargs):
        if "user_name" not in session:
            return jsonify({"error": "Authentication required"}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function