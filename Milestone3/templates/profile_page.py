# Profile page template for the AI-Based Smart File Assistant

def get_profile_page_html(user):
    """Generate the profile page HTML"""
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
        <meta http-equiv="Pragma" content="no-cache">
        <meta http-equiv="Expires" content="0">
        <title>Profile - AI-Based Smart File Assistant</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 25%, #f1f5f9 50%, #e2e8f0 75%, #f8fafc 100%);
                min-height: 100vh; 
                color: #333; 
                line-height: 1.6; 
                padding-top: 80px;
                padding-bottom: 60px;
            }}
            
            .header {{ background: #ffffff; padding: 16px 0; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); position: fixed; top: 0; left: 0; right: 0; z-index: 1000; }}
            .header-content {{ max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; padding: 0 24px; }}
            .logo {{ display: flex; align-items: center; gap: 8px; font-size: 20px; font-weight: 700; color: #2563eb; }}
            .logo-icon {{ width: 32px; height: 32px; background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 16px; font-weight: bold; }}
            .nav-menu {{ display: flex; align-items: center; gap: 32px; }}
            .nav-link {{ color: #64748b; text-decoration: none; font-weight: 500; font-size: 15px; transition: all 0.2s; padding: 8px 16px; border-radius: 6px; }}
            .nav-link:hover {{ color: #2563eb; background: rgba(37, 99, 235, 0.1); }}
            .btn-secondary {{ background: #f8fafc; color: #2563eb; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-weight: 500; transition: all 0.2s; border: 1px solid #e2e8f0; }}
            .btn-secondary:hover {{ background: #f1f5f9; }}
            
            .container {{ max-width: 800px; margin: 0 auto; padding: 40px 24px; }}
            .profile-card {{ background: #ffffff; border-radius: 20px; padding: 40px; border: 1px solid #e2e8f0; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); }}
            .profile-header {{ text-align: center; margin-bottom: 40px; }}
            .profile-avatar {{ width: 120px; height: 120px; border-radius: 50%; background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 48px; margin: 0 auto 20px; border: 4px solid #e2e8f0; overflow: hidden; }}
            .profile-avatar img {{ width: 100%; height: 100%; object-fit: cover; }}
            .profile-title {{ font-size: 28px; font-weight: 700; color: #1e293b; margin-bottom: 8px; }}
            .profile-subtitle {{ font-size: 16px; color: #64748b; }}
            
            .profile-form {{ display: grid; gap: 24px; }}
            .form-group {{ display: grid; gap: 8px; }}
            .form-label {{ font-size: 14px; font-weight: 600; color: #374151; }}
            .form-input {{ padding: 12px 16px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 14px; transition: all 0.2s; }}
            .form-input:focus {{ outline: none; border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1); }}
            .form-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
            
            .btn-primary {{ background: #2563eb; color: white; padding: 12px 24px; border-radius: 8px; border: none; font-weight: 600; font-size: 14px; cursor: pointer; transition: all 0.2s; }}
            .btn-primary:hover {{ background: #1d4ed8; }}
            
            /* Ensure no footer elements can appear - AGGRESSIVE REMOVAL */
            footer, .footer, [class*="footer"], [id*="footer"] {{ 
                display: none !important; 
                visibility: hidden !important;
                opacity: 0 !important;
                height: 0 !important;
                overflow: hidden !important;
                position: absolute !important;
                left: -9999px !important;
            }}
            body {{ overflow-x: hidden; }}
            html {{ overflow-x: hidden; }}
            
            /* Ensure page ends cleanly */
            body::after {{ 
                content: ''; 
                display: block; 
                clear: both; 
                height: 0; 
            }}
            
            @media (max-width: 768px) {{
                .form-row {{ grid-template-columns: 1fr; }}
                .nav-menu {{ display: none; }}
            }}
        </style>
    </head>
    <body>
        <header class="header">
            <div class="header-content">
                <div class="logo">
                    <div class="logo-icon">📄</div>
                    AI-Based Smart File Assistant
                </div>
                
                <nav class="nav-menu">
                    <a href="/dashboard" class="nav-link">Dashboard</a>
                    <a href="/dashboard#upload" class="nav-link">Upload</a>
                    <a href="/dashboard#query" class="nav-link">Query</a>
                </nav>
                
                <div>
                    <a href="/dashboard" class="btn-secondary">Back to Dashboard</a>
                </div>
            </div>
        </header>

        <main class="container">
            <div class="profile-card">
                <div class="profile-header">
                    <div class="profile-avatar">
                        {user["profile_picture"] and f'<img src="{user["profile_picture"]}" alt="Profile Picture">' or user["first_name"][0].upper() if user["first_name"] else "U"}
                    </div>
                    <h1 class="profile-title">Profile Settings</h1>
                    <p class="profile-subtitle">Manage your account information and preferences</p>
                    <div id="message-container" style="margin-top: 20px;"></div>
                </div>
                
                <form class="profile-form" method="POST">
                    <div class="form-row">
                        <div class="form-group">
                            <label class="form-label" for="firstName">First Name</label>
                            <input type="text" id="firstName" name="firstName" class="form-input" value="{user['first_name']}" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label" for="lastName">Last Name</label>
                            <input type="text" id="lastName" name="lastName" class="form-input" value="{user['last_name']}" required>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label" for="email">Email Address</label>
                        <input type="email" id="email" name="email" class="form-input" value="{user['email']}" required>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label" for="currentPassword">Current Password</label>
                        <input type="password" id="currentPassword" name="currentPassword" class="form-input" placeholder="Enter current password to make changes" required>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label class="form-label" for="newPassword">New Password (Optional)</label>
                            <input type="password" id="newPassword" name="newPassword" class="form-input" placeholder="Leave blank to keep current password">
                        </div>
                        <div class="form-group">
                            <label class="form-label" for="confirmPassword">Confirm New Password</label>
                            <input type="password" id="confirmPassword" name="confirmPassword" class="form-input" placeholder="Confirm new password">
                        </div>
                    </div>
                    
                    <button type="submit" class="btn-primary">Update Profile</button>
                </form>
            </div>
        </main>
        
        <script>
            document.querySelector('.profile-form').addEventListener('submit', function(e) {{
                e.preventDefault();
                
                var formData = new FormData(this);
                var submitBtn = document.querySelector('.btn-primary');
                var messageContainer = document.getElementById('message-container');
                
                submitBtn.disabled = true;
                submitBtn.textContent = 'Updating...';
                messageContainer.innerHTML = '';
                
                fetch('/profile', {{
                    method: 'POST',
                    body: formData
                }})
                .then(function(response) {{
                    if (response.redirected) {{
                        window.location.reload();
                        return;
                    }}
                    return response.json();
                }})
                .then(function(data) {{
                    if (data && data.error) {{
                        messageContainer.innerHTML = '<div style="color: #ef4444; background: #fef2f2; padding: 16px; border-radius: 8px; border: 1px solid #fecaca; font-weight: 500;">' + data.error + '</div>';
                    }} else if (data && data.message) {{
                        messageContainer.innerHTML = '<div style="color: #10b981; background: #f0fdf4; padding: 16px; border-radius: 8px; border: 1px solid #bbf7d0; font-weight: 500; text-align: center;">✅ ' + data.message + '</div>';
                        // Clear the form password fields
                        document.getElementById('currentPassword').value = '';
                        document.getElementById('newPassword').value = '';
                        document.getElementById('confirmPassword').value = '';
                        // Auto-hide success message after 3 seconds
                        setTimeout(function() {{ 
                            messageContainer.innerHTML = '';
                        }}, 3000);
                    }}
                }})
                .catch(function(error) {{
                    console.error('Error:', error);
                    messageContainer.innerHTML = '<div style="color: #ef4444; background: #fef2f2; padding: 12px; border-radius: 8px; border: 1px solid #fecaca;">An error occurred while updating your profile.</div>';
                }})
                .finally(function() {{
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Update Profile';
                }});
            }});
        </script>
    </body>
    </html>
    '''