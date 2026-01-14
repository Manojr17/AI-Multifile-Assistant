# Main routes for the AI-Based Smart File Assistant
from flask import render_template, redirect, url_for, session, request, jsonify
from auth import require_auth
from database import get_db
from templates.landing_page import get_landing_page_html
from templates.dashboard_page import get_dashboard_page_html
from templates.profile_page import get_profile_page_html
import time

def register_main_routes(app):
    """Register main application routes"""
    
    @app.route("/test-landing")
    def test_landing():
        """Test route that always shows the landing page regardless of login status"""
        return get_landing_page_html()

    @app.route("/")
    def home():
        """Home page - redirect to dashboard if logged in, otherwise show landing page"""
        if "user_name" in session:
            return redirect(url_for("dashboard"))
        return get_landing_page_html()

    @app.route("/auth")
    def auth():
        """Authentication page"""
        if "user_name" in session:
            return redirect(url_for("dashboard"))
        
        # Get the mode from query parameter (login or signup)
        from flask import request
        mode = request.args.get('mode', 'login')  # default to login
        return render_template("auth.html", mode=mode)

    @app.route("/dashboard")
    def dashboard():
        """Main dashboard page"""
        if "user_name" not in session:
            return redirect(url_for("auth"))
        
        # Get complete user information from database
        conn = get_db()
        cursor = conn.cursor()
        
        # Use user_id if available, otherwise fall back to first_name
        if "user_id" in session:
            cursor.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],))
        else:
            cursor.execute("SELECT * FROM users WHERE first_name = ?", (session["user_name"],))
        
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            # If user not found, clear session and redirect to auth
            session.clear()
            return redirect(url_for("auth"))
        
        return get_dashboard_page_html(user)

    @app.route("/profile", methods=["GET", "POST"])
    def profile():
        """User profile page"""
        if "user_name" not in session:
            return redirect(url_for("auth"))
        
        # Get user information
        conn = get_db()
        cursor = conn.cursor()
        
        if "user_id" in session:
            cursor.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],))
        else:
            cursor.execute("SELECT * FROM users WHERE first_name = ?", (session["user_name"],))
        
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            session.clear()
            return redirect(url_for("auth"))
        
        # Handle POST request (profile update)
        if request.method == "POST":
            from werkzeug.utils import secure_filename
            from database import hash_password, verify_password
            import os
            import time
            
            # Get form data
            first_name = request.form.get('firstName', '').strip()
            last_name = request.form.get('lastName', '').strip()
            email = request.form.get('email', '').strip()
            current_password = request.form.get('currentPassword', '')
            new_password = request.form.get('newPassword', '')
            confirm_password = request.form.get('confirmPassword', '')
            
            # Validate required fields
            if not all([first_name, last_name, email, current_password]):
                conn.close()
                return jsonify({"error": "All fields except new password are required"}), 400
            
            # Verify current password
            if not verify_password(current_password, user['password']):
                conn.close()
                return jsonify({"error": "Current password is incorrect"}), 400
            
            # Validate new password if provided
            if new_password:
                if new_password != confirm_password:
                    conn.close()
                    return jsonify({"error": "New passwords do not match"}), 400
                if len(new_password) < 6:
                    conn.close()
                    return jsonify({"error": "New password must be at least 6 characters"}), 400
            
            # Update user in database
            try:
                if new_password:
                    hashed_password = hash_password(new_password)
                    cursor.execute("""
                        UPDATE users 
                        SET first_name = ?, last_name = ?, email = ?, password = ?
                        WHERE id = ?
                    """, (first_name, last_name, email, hashed_password, user['id']))
                else:
                    cursor.execute("""
                        UPDATE users 
                        SET first_name = ?, last_name = ?, email = ?
                        WHERE id = ?
                    """, (first_name, last_name, email, user['id']))
                
                conn.commit()
                
                # Update session
                session['user_name'] = first_name
                session['user_id'] = user['id']
                
                conn.close()
                
                # Return success response for AJAX
                return jsonify({"message": "Profile updated successfully!"}), 200
                    
            except Exception as e:
                conn.close()
                print(f"❌ Error updating profile: {str(e)}")
                return jsonify({"error": f"Failed to update profile: {str(e)}"}), 500
        
        conn.close()
        return get_profile_page_html(user)

    # Additional routes for dropdown menu items
    @app.route("/documents")
    def documents():
        """Documents page - redirect to dashboard upload section"""
        if "user_name" not in session:
            return redirect(url_for("auth"))
        return redirect(url_for("dashboard") + "#upload")

    @app.route("/history")
    def history():
        """History page - redirect to dashboard query section"""
        if "user_name" not in session:
            return redirect(url_for("auth"))
        return redirect(url_for("dashboard") + "#query")

    @app.route("/billing")
    def billing():
        """Billing page - redirect to dashboard"""
        if "user_name" not in session:
            return redirect(url_for("auth"))
        return redirect(url_for("dashboard"))

    @app.route("/help")
    def help_support():
        """Help page - redirect to dashboard contact section"""
        if "user_name" not in session:
            return redirect(url_for("auth"))
        return redirect(url_for("dashboard") + "#contact")

    # Redirect routes to dashboard sections
    @app.route("/upload")
    def upload():
        """Upload page - redirect to dashboard upload section"""
        if "user_name" not in session:
            return redirect(url_for("auth"))
        return redirect(url_for("dashboard") + "#upload")

    @app.route("/how-it-works")
    def how_it_works():
        """How it works page - redirect to dashboard section"""
        if "user_name" not in session:
            return redirect(url_for("auth"))
        return redirect(url_for("dashboard") + "#how-it-works")

    @app.route("/contact")
    def contact():
        """Contact page - redirect to dashboard contact section"""
        if "user_name" not in session:
            return redirect(url_for("auth"))
        return redirect(url_for("dashboard") + "#contact")