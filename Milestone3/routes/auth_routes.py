# Authentication routes for the AI-Based Smart File Assistant
from auth import signup, login, logout

def register_auth_routes(app):
    """Register authentication routes"""
    
    @app.route("/logout")
    def logout_route():
        """Logout route"""
        return logout()

    @app.route("/signup", methods=["POST"])
    def signup_route():
        """Signup route"""
        return signup()

    @app.route("/api/register", methods=["POST"])
    def api_register():
        """API route for frontend compatibility"""
        return signup()

    @app.route("/login", methods=["POST"])
    def login_route():
        """Login route"""
        return login()

    @app.route("/api/login", methods=["POST"])
    def api_login():
        """API route for frontend compatibility"""
        return login()