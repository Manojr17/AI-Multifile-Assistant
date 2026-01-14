# Dashboard page template for the AI-Based Smart File Assistant

def get_dashboard_page_html(user):
    """Generate the dashboard page HTML"""
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard - AI-Based Smart File Assistant</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 25%, #f1f5f9 50%, #e2e8f0 75%, #f8fafc 100%);
                min-height: 100vh; 
                color: #333; 
                line-height: 1.6; 
                padding-top: 80px; 
                position: relative;
                overflow-x: hidden;
            }}
            
            .header {{ background: #ffffff; padding: 16px 0; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); position: fixed; top: 0; left: 0; right: 0; z-index: 1000; }}
            .header-content {{ max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; padding: 0 24px; flex-wrap: nowrap; }}
            .logo {{ display: flex; align-items: center; gap: 8px; font-size: 20px; font-weight: 700; color: #2563eb; white-space: nowrap; flex-shrink: 0; }}
            .logo-icon {{ width: 32px; height: 32px; background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 16px; font-weight: bold; }}
            .nav-menu {{ display: flex; align-items: center; gap: 32px; }}
            .nav-link {{ color: #64748b; text-decoration: none; font-weight: 500; font-size: 15px; transition: all 0.2s; padding: 8px 16px; border-radius: 6px; position: relative; white-space: nowrap; }}
            .nav-link:hover {{ color: #2563eb; background: rgba(37, 99, 235, 0.1); }}
            .nav-link.active {{ color: #2563eb; background: rgba(37, 99, 235, 0.15); }}
            .user-info {{ display: flex; align-items: center; gap: 16px; position: relative; }}
            .user-profile-header {{ display: flex; align-items: center; gap: 12px; }}
            .user-avatar-small {{ width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); display: flex; align-items: center; justify-content: center; color: white; font-weight: 600; font-size: 16px; border: 2px solid rgba(255, 255, 255, 0.3); overflow: hidden; }}
            .user-avatar-small img {{ width: 100%; height: 100%; object-fit: cover; }}
            .welcome-text {{ color: #64748b; font-weight: 500; }}
            .container {{ max-width: 1200px; margin: 0 auto; padding: 0 24px; position: relative; z-index: 10; }}
            .main-content {{ padding: 40px 0; }}
            .dashboard-grid {{ display: grid; grid-template-columns: 300px 1fr; gap: 30px; margin-bottom: 40px; }}
            .profile-section {{ background: #ffffff; border-radius: 20px; padding: 30px; border: 1px solid #e2e8f0; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); height: fit-content; }}
            .profile-avatar {{ width: 100px; height: 100px; border-radius: 50%; background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 36px; margin: 0 auto 20px; border: 4px solid #e2e8f0; overflow: hidden; box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1); }}
            .profile-avatar img {{ width: 100%; height: 100%; object-fit: cover; }}
            .profile-info {{ text-align: center; }}
            .profile-name {{ font-size: 20px; font-weight: 600; color: #1e293b; margin-bottom: 8px; }}
            .profile-email {{ font-size: 14px; color: #64748b; margin-bottom: 20px; }}
            .profile-stats {{ display: flex; flex-direction: column; gap: 12px; }}
            .stat-item {{ display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #f1f5f9; }}
            .stat-label {{ font-size: 13px; color: #64748b; }}
            .stat-value {{ font-size: 14px; font-weight: 600; color: #1e293b; }}
            .edit-profile-btn {{ width: 100%; background: #f8fafc; color: #2563eb; padding: 12px 20px; border-radius: 10px; text-decoration: none; font-weight: 600; font-size: 14px; transition: all 0.3s ease; border: 2px solid #e2e8f0; display: block; text-align: center; margin-top: 20px; }}
            .edit-profile-btn:hover {{ background: #f1f5f9; transform: translateY(-2px); border-color: #2563eb; }}
            .project-header {{ background: #ffffff; border-radius: 20px; padding: 40px; border: 1px solid #e2e8f0; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); }}
            .project-title {{ font-size: 36px; font-weight: 700; color: #1e293b; line-height: 1.3; margin-bottom: 20px; }}
            .project-subtitle {{ font-size: 16px; color: #111827; line-height: 1.6; margin-bottom: 20px; font-weight: 600; }}
            .project-description {{ font-size: 16px; color: #64748b; line-height: 1.6; margin-bottom: 20px; }}
            .action-buttons {{ display: flex; gap: 16px; flex-wrap: wrap; }}
            .btn-primary {{ background: #2563eb; color: white; padding: 14px 24px; border-radius: 10px; text-decoration: none; font-weight: 600; font-size: 14px; transition: all 0.3s ease; border: none; cursor: pointer; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3); }}
            .btn-primary:hover {{ background: #1d4ed8; transform: translateY(-2px); box-shadow: 0 8px 20px rgba(37, 99, 235, 0.4); }}
            .btn-secondary {{ background: #f8fafc; color: #2563eb; padding: 14px 24px; border-radius: 10px; text-decoration: none; font-weight: 600; font-size: 14px; transition: all 0.3s ease; border: 2px solid #e2e8f0; }}
            .btn-secondary:hover {{ background: #f1f5f9; transform: translateY(-2px); border-color: #2563eb; }}
            .features-overview {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px; margin-top: 40px; }}
            .feature-card {{ background: #ffffff; border-radius: 16px; padding: 30px 24px; border: 1px solid #e2e8f0; transition: all 0.3s ease; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05); }}
            .feature-card:hover {{ transform: translateY(-4px); background: #ffffff; box-shadow: 0 8px 25px rgba(37, 99, 235, 0.15); border-color: #2563eb; }}
            .feature-icon {{ width: 60px; height: 60px; border-radius: 12px; display: flex; align-items: center; justify-content: center; margin: 0 auto 16px; font-size: 24px; color: white; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); }}
            .feature-icon.upload {{ background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); }}
            .feature-icon.query {{ background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%); }}
            .feature-icon.extract {{ background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%); }}
            .feature-icon.context {{ background: linear-gradient(135deg, #10b981 0%, #2563eb 100%); }}
            .feature-card h3 {{ font-size: 18px; font-weight: 600; color: #1e293b; margin-bottom: 12px; text-align: center; }}
            .feature-card p {{ color: #64748b; font-size: 14px; line-height: 1.5; text-align: center; }}
            
            /* Upload Section Styles */
            .upload-section {{ padding: 80px 0; background: #f8fafc; }}
            .section-content {{ max-width: 1200px; margin: 0 auto; padding: 0 24px; }}
            .section-title {{ font-size: 36px; font-weight: 700; color: #1e293b; text-align: center; margin-bottom: 16px; }}
            .section-subtitle {{ font-size: 18px; color: #64748b; text-align: center; margin-bottom: 60px; max-width: 600px; margin-left: auto; margin-right: auto; }}
            .upload-area {{ max-width: 800px; margin: 0 auto; }}
            .upload-box {{ background: #ffffff; border-radius: 20px; padding: 40px; border: 1px solid #e2e8f0; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); }}
            .upload-header {{ text-align: center; margin-bottom: 30px; }}
            .upload-icon {{ width: 80px; height: 80px; background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); border-radius: 16px; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px; font-size: 32px; color: white; }}
            .upload-dropzone {{ border: 2px dashed #e2e8f0; border-radius: 16px; padding: 60px 40px; text-align: center; cursor: pointer; transition: all 0.3s ease; margin-bottom: 30px; }}
            .upload-dropzone:hover {{ border-color: #2563eb; background: rgba(37, 99, 235, 0.05); }}
            .dropzone-content {{ display: flex; flex-direction: column; align-items: center; gap: 16px; }}
            .dropzone-icon {{ font-size: 48px; opacity: 0.6; }}
            .supported-formats {{ display: flex; gap: 12px; flex-wrap: wrap; justify-content: center; margin-top: 16px; }}
            .format {{ background: #f1f5f9; color: #2563eb; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }}
            .upload-status {{ margin-bottom: 20px; }}
            .upload-status.success {{ color: #10b981; }}
            .upload-status.error {{ color: #ef4444; }}
            .upload-status.processing {{ color: #f59e0b; }}
            .documents-section {{ margin-top: 40px; }}
            .documents-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }}
            .refresh-btn {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 8px 12px; cursor: pointer; transition: all 0.2s; }}
            .refresh-btn:hover {{ background: #f1f5f9; }}
            .documents-list {{ display: flex; flex-direction: column; gap: 16px; }}
            .document-item {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; display: flex; justify-content: space-between; align-items: center; }}
            .document-info {{ display: flex; align-items: center; gap: 16px; flex: 1; }}
            .document-icon {{ width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 20px; color: white; }}
            .file-type-pdf {{ background: #dc3545; }}
            .file-type-docx {{ background: #2563eb; }}
            .file-type-txt {{ background: #10b981; }}
            .document-details {{ flex: 1; }}
            .document-name {{ font-weight: 600; color: #1e293b; margin-bottom: 4px; }}
            .document-meta {{ font-size: 12px; color: #64748b; display: flex; gap: 16px; }}
            .processing-stats {{ margin-top: 8px; display: flex; gap: 16px; }}
            .stats-row {{ display: flex; gap: 8px; }}
            .stat-label {{ font-size: 11px; color: #64748b; }}
            .stat-value {{ font-size: 11px; font-weight: 600; color: #1e293b; }}
            .document-actions {{ display: flex; gap: 8px; }}
            .delete-btn {{ background: #fee2e2; color: #dc2626; border: 1px solid #fecaca; border-radius: 6px; padding: 6px 12px; font-size: 12px; cursor: pointer; transition: all 0.2s; }}
            .delete-btn:hover {{ background: #fecaca; }}
            .no-documents {{ text-align: center; padding: 60px 20px; color: #64748b; }}
            
            /* Chat Section Styles */
            .chatbot-section {{ padding: 80px 0; background: #ffffff; }}
            .chatbot-container {{ max-width: 1100px; margin: 0 auto; background: #ffffff; border-radius: 20px; border: 1px solid #e2e8f0; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); overflow: hidden; min-height: 850px; }}
            .chat-header {{ background: #f8fafc; padding: 20px; border-bottom: 1px solid #e2e8f0; display: flex; align-items: center; gap: 16px; }}
            .chat-avatar {{ width: 50px; height: 50px; background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; color: white; }}
            .chat-info {{ flex: 1; }}
            .chat-info h3 {{ font-size: 18px; font-weight: 600; color: #1e293b; margin-bottom: 4px; }}
            .chat-status {{ font-size: 14px; color: #64748b; }}
            .chat-actions {{ display: flex; gap: 8px; }}
            .clear-chat-btn {{ background: #fee2e2; color: #dc2626; border: none; border-radius: 6px; padding: 8px 12px; font-size: 12px; cursor: pointer; transition: all 0.2s; }}
            .clear-chat-btn:hover {{ background: #fecaca; }}
            .chat-messages {{ height: 650px; overflow-y: auto; padding: 20px; }}
            .message {{ display: flex; gap: 12px; margin-bottom: 20px; }}
            .message-avatar {{ width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 16px; flex-shrink: 0; }}
            .bot-message .message-avatar {{ background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; }}
            .user-message .message-avatar {{ background: #e2e8f0; color: #64748b; }}
            .message-content {{ flex: 1; }}
            .message-text {{ background: #f8fafc; padding: 16px 20px; border-radius: 12px; margin-bottom: 4px; font-size: 15px; line-height: 1.6; }}
            .user-message .message-text {{ background: #2563eb; color: white; }}
            .message-time {{ font-size: 11px; color: #64748b; }}
            .chat-input-container {{ padding: 25px; border-top: 1px solid #e2e8f0; background: #ffffff; }}
            .chat-input-wrapper {{ display: flex; gap: 12px; margin-bottom: 12px; }}
            .chat-input {{ flex: 1; padding: 16px 20px; border: 1px solid #e2e8f0; border-radius: 12px; font-size: 16px; }}
            .send-btn {{ background: #2563eb; color: white; border: none; border-radius: 12px; padding: 16px 24px; cursor: pointer; transition: all 0.2s; font-weight: 600; font-size: 16px; }}
            .send-btn:hover {{ background: #1d4ed8; }}
            .quick-questions {{ display: flex; gap: 8px; flex-wrap: wrap; }}
            .quick-btn {{ background: #f1f5f9; color: #2563eb; border: 1px solid #e2e8f0; border-radius: 20px; padding: 6px 12px; font-size: 12px; cursor: pointer; transition: all 0.2s; }}
            .quick-btn:hover {{ background: #e2e8f0; }}
            
            /* How It Works Section Styles */
            .how-it-works-section {{ padding: 80px 0; background: #f8fafc; }}
            .steps-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 40px; margin-top: 60px; }}
            .step-card {{ background: #ffffff; padding: 30px; border-radius: 16px; text-align: center; border: 1px solid #e2e8f0; }}
            .step-number {{ width: 50px; height: 50px; background: #2563eb; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; font-weight: 700; margin: 0 auto 20px; }}
            .step-card h3 {{ font-size: 18px; font-weight: 600; color: #1e293b; margin-bottom: 12px; }}
            .step-card p {{ color: #64748b; line-height: 1.6; }}
            
            /* Contact Section Styles */
            .contact-section {{ padding: 80px 0; background: #ffffff; }}
            .contact-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px; margin-top: 60px; }}
            .contact-card {{ background: #f8fafc; padding: 30px; border-radius: 16px; text-align: center; border: 1px solid #e2e8f0; transition: all 0.3s ease; }}
            .contact-card:hover {{ transform: translateY(-5px); box-shadow: 0 10px 30px rgba(37, 99, 235, 0.1); }}
            .contact-icon {{ width: 60px; height: 60px; background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px; font-size: 24px; color: white; }}
            .contact-card h3 {{ font-size: 18px; font-weight: 600; color: #1e293b; margin-bottom: 12px; }}
            .contact-card p {{ color: #64748b; line-height: 1.6; margin-bottom: 8px; }}
            .contact-card p:last-child {{ font-size: 14px; opacity: 0.8; }}
            
            @media (max-width: 768px) {{ 
                .dashboard-grid {{ grid-template-columns: 1fr; gap: 20px; }} 
                .project-title {{ font-size: 28px; }} 
                .features-overview {{ grid-template-columns: 1fr; gap: 20px; }} 
                .action-buttons {{ flex-direction: column; }} 
                .header-content {{ flex-direction: column; gap: 16px; }} 
                .user-profile-header {{ flex-direction: column; text-align: center; }} 
                .nav-menu {{ display: none; }} 
                .section-title {{ font-size: 28px; }} 
                .steps-grid {{ grid-template-columns: 1fr; }}
                .use-cases-grid {{ grid-template-columns: 1fr; }}
                .contact-grid {{ grid-template-columns: 1fr; }}
            }}
            
            /* Footer Styles */
            .footer {{ background: #1e293b; color: #e2e8f0; padding: 60px 0 30px; margin-top: 80px; }}
            .footer-content {{ max-width: 1200px; margin: 0 auto; padding: 0 24px; }}
            .footer-grid {{ display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 40px; margin-bottom: 40px; }}
            .footer-section h3 {{ color: #ffffff; font-size: 18px; font-weight: 600; margin-bottom: 20px; }}
            .footer-section p {{ color: #94a3b8; line-height: 1.6; margin-bottom: 16px; }}
            .footer-links {{ display: flex; flex-direction: column; gap: 12px; }}
            .footer-link {{ color: #94a3b8; text-decoration: none; transition: color 0.2s; }}
            .footer-link:hover {{ color: #ffffff; }}
            .footer-bottom {{ border-top: 1px solid #334155; padding-top: 30px; display: flex; justify-content: space-between; align-items: center; }}
            .footer-bottom p {{ color: #94a3b8; margin: 0; }}
            .social-links {{ display: flex; gap: 16px; }}
            .social-link {{ color: #94a3b8; font-size: 20px; transition: color 0.2s; }}
            .social-link:hover {{ color: #ffffff; }}
            
            @media (max-width: 768px) {{
                .footer-grid {{ grid-template-columns: 1fr; gap: 30px; }}
                .footer-bottom {{ flex-direction: column; gap: 20px; text-align: center; }}
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
                
                <nav class="nav-menu" id="main-navbar">
                    <a href="/dashboard" class="nav-link">Home</a>
                    <a href="#upload" class="nav-link" onclick="scrollToSection('upload'); return false;">Upload</a>
                    <a href="#query" class="nav-link" onclick="scrollToSection('query'); return false;">Query</a>
                    <a href="#how-it-works" class="nav-link" onclick="scrollToSection('how-it-works'); return false;">How It Works</a>
                    <a href="#contact" class="nav-link" onclick="scrollToSection('contact'); return false;">Contact</a>
                </nav>
                
                <div class="user-info">
                    <div class="user-profile-header">
                        <div class="user-avatar-small">
                            {user["profile_picture"] and f'<img src="{user["profile_picture"]}" alt="Profile">' or user["first_name"][0].upper()}
                        </div>
                        <span class="welcome-text">Welcome, {user["first_name"]}!</span>
                    </div>
                    <a href="/logout" class="btn-secondary">Logout</a>
                </div>
            </div>
        </header>

        <main class="container">
            <div class="main-content">
                <div id="home" class="dashboard-grid">
                    <div class="profile-section">
                        <div class="profile-avatar">
                            {user["profile_picture"] and f'<img src="{user["profile_picture"]}" alt="Profile Picture">' or user["first_name"][0].upper()}
                        </div>
                        
                        <div class="profile-info">
                            <div class="profile-name">{user["first_name"]} {user["last_name"]}</div>
                            <div class="profile-email">{user["email"]}</div>
                            
                            <div class="profile-stats">
                                <div class="stat-item">
                                    <span class="stat-label">Documents Uploaded</span>
                                    <span class="stat-value">0</span>
                                </div>
                                <div class="stat-item">
                                    <span class="stat-label">Queries Made</span>
                                    <span class="stat-value">0</span>
                                </div>
                                <div class="stat-item">
                                    <span class="stat-label">Account Type</span>
                                    <span class="stat-value">Free</span>
                                </div>
                                <div class="stat-item">
                                    <span class="stat-label">Member Since</span>
                                    <span class="stat-value">Today</span>
                                </div>
                            </div>
                            
                            <a href="/profile" class="edit-profile-btn">Edit Profile</a>
                        </div>
                    </div>

                    <div class="project-header">
                        <h1 class="project-title">AI-Based Smart File Assistant</h1>
                        <p class="project-subtitle">
                            For Contextual Querying And Efficient Information Extraction From Multiple Documents
                        </p>
                        <p class="project-description">
                            Transform your document workflow with intelligent AI that understands context, extracts key information, 
                            and provides instant answers from your uploaded files. Whether you're working with legal documents, 
                            research papers, or business reports, our smart assistant makes information retrieval effortless.
                        </p>
                        
                        <div class="action-buttons">
                            <a href="#upload" class="btn-primary">Upload Documents</a>
                            <a href="#query" class="btn-secondary">Start Querying</a>
                        </div>
                    </div>
                </div>

                <div class="features-overview">
                    <div class="feature-card">
                        <div class="feature-icon upload">📁</div>
                        <h3>Smart File Upload</h3>
                        <p>Upload multiple document formats including PDF, DOCX, PPT, and TXT. Our system automatically processes and indexes your content for intelligent querying.</p>
                    </div>
                    
                    <div class="feature-card">
                        <div class="feature-icon query">🔍</div>
                        <h3>Contextual Querying</h3>
                        <p>Ask natural language questions about your documents. Our AI understands context and provides accurate, relevant answers from your uploaded content.</p>
                    </div>
                    
                    <div class="feature-card">
                        <div class="feature-icon extract">📊</div>
                        <h3>Information Extraction</h3>
                        <p>Efficiently extract key information, summaries, and insights from large documents. Save time with automated analysis and data extraction.</p>
                    </div>
                    
                    <div class="feature-card">
                        <div class="feature-icon context">🔗</div>
                        <h3>Multi-Document Analysis</h3>
                        <p>Analyze relationships and connections across multiple documents. Get comprehensive insights from your entire document collection.</p>
                    </div>
                </div>
            </div>
            
            <!-- Upload Section -->
            <section id="upload" class="upload-section">
                <div class="section-content">
                    <h2 class="section-title">Upload Your Documents</h2>
                    <p class="section-subtitle">
                        Upload multiple document formats and let our AI process them for intelligent querying.
                    </p>
                    
                    <div class="upload-area">
                        <div class="upload-box">
                            <div class="upload-header">
                                <div class="upload-icon">📁</div>
                                <h3>Upload Documents</h3>
                                <p>Upload your files to start intelligent document analysis</p>
                            </div>
                            
                            <!-- File Upload Dropzone -->
                            <div class="upload-dropzone" id="uploadDropzone" onclick="document.getElementById('fileInput').click()">
                                <input type="file" id="fileInput" multiple accept=".txt,.pdf,.doc,.docx,.ppt,.pptx,.xls,.xlsx" style="display: none;">
                                <div class="dropzone-content">
                                    <div class="dropzone-icon">📁</div>
                                    <h4>Upload Files</h4>
                                    <p>Click here or drop files to upload</p>
                                    <div class="supported-formats">
                                        <span class="format">PDF</span>
                                        <span class="format">DOCX</span>
                                        <span class="format">PPT</span>
                                        <span class="format">TXT</span>
                                        <span class="format">XLS</span>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="upload-status" id="uploadStatus"></div>
                            
                            <!-- Uploaded Documents List -->
                            <div class="documents-section">
                                <div class="documents-header">
                                    <h4>📋 Uploaded Documents</h4>
                                    <button class="refresh-btn" onclick="loadUserDocuments();">🔄</button>
                                </div>
                                <div class="documents-list" id="documentsList">
                                    <div class="loading-documents">Loading documents...</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            
            <!-- Chatbot Section -->
            <section id="query" class="chatbot-section">
                <div class="section-content">
                    <h2 class="section-title">AI Document Assistant</h2>
                    <p class="section-subtitle">
                        Chat with your documents using natural language. Get instant answers powered by AI.
                    </p>
                    
                    <div class="chatbot-container">
                        <div class="chat-header">
                            <div class="chat-avatar">🤖</div>
                            <div class="chat-info">
                                <h3>AI Assistant</h3>
                                <p class="chat-status">Ready to help with your documents</p>
                            </div>
                            <div class="chat-actions">
                                <button class="clear-chat-btn" onclick="clearChat()" title="Clear Chat">🗑️</button>
                            </div>
                        </div>
                        
                        <div class="chat-messages" id="chatMessages">
                            <div class="message bot-message">
                                <div class="message-avatar">🤖</div>
                                <div class="message-content">
                                    <div class="message-text">
                                        Hello! I'm your AI document assistant. Upload some documents and ask me questions about them. I can help you:
                                        <ul>
                                            <li>📋 Summarize document content</li>
                                            <li>🔍 Find specific information</li>
                                            <li>📊 Extract key data and statistics</li>
                                            <li>❓ Answer questions about your files</li>
                                        </ul>
                                    </div>
                                    <div class="message-time">Just now</div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="chat-input-container">
                            <div class="chat-input-wrapper">
                                <input type="text" id="chatInput" class="chat-input" placeholder="Ask a question about your documents..." onkeypress="handleChatKeyPress(event)">
                                <button class="send-btn" onclick="sendMessage()" id="sendBtn">
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                        <line x1="22" y1="2" x2="11" y2="13"></line>
                                        <polygon points="22,2 15,22 11,13 2,9"></polygon>
                                    </svg>
                                </button>
                            </div>
                            <div class="quick-questions">
                                <button class="quick-btn" onclick="sendQuickQuestion('Summarize my documents')">📋 Summarize</button>
                                <button class="quick-btn" onclick="sendQuickQuestion('What are the key findings?')">🔍 Key Findings</button>
                                <button class="quick-btn" onclick="sendQuickQuestion('Extract important data')">📊 Extract Data</button>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            
            <!-- How It Works Section -->
            <section id="how-it-works" class="how-it-works-section">
                <div class="section-content">
                    <h2 class="section-title">How It Works</h2>
                    <p class="section-subtitle">
                        Get started with our AI assistant in just four simple steps and transform your document workflow.
                    </p>
                    <div class="steps-grid">
                        <div class="step-card">
                            <div class="step-number">1</div>
                            <h3>Upload Documents</h3>
                            <p>Upload your files in various formats. Our system automatically processes and indexes your content for intelligent analysis.</p>
                        </div>
                        <div class="step-card">
                            <div class="step-number">2</div>
                            <h3>AI Processing</h3>
                            <p>Our advanced AI algorithms analyze your documents, extract key information, and create contextual embeddings.</p>
                        </div>
                        <div class="step-card">
                            <div class="step-number">3</div>
                            <h3>Ask Questions</h3>
                            <p>Query your documents using natural language. Ask questions and get accurate, contextual answers instantly.</p>
                        </div>
                        <div class="step-card">
                            <div class="step-number">4</div>
                            <h3>Get Insights</h3>
                            <p>Receive comprehensive answers and insights based on your document content with relevant information extraction.</p>
                        </div>
                    </div>
                </div>
            </section>
            
            <!-- Contact Section -->
            <section id="contact" class="contact-section">
                <div class="section-content">
                    <h2 class="section-title">Contact Us</h2>
                    <p class="section-subtitle">
                        Get in touch with our support team for any questions or assistance with our AI-powered document assistant.
                    </p>
                    <div class="contact-grid">
                        <div class="contact-card">
                            <div class="contact-icon">📧</div>
                            <h3>Email Support</h3>
                            <p>support@docai.com</p>
                            <p>We'll respond within 24 hours</p>
                        </div>
                        <div class="contact-card">
                            <div class="contact-icon">📞</div>
                            <h3>Phone Support</h3>
                            <p>+1 (555) 123-4567</p>
                            <p>Mon-Fri, 9AM-6PM EST</p>
                        </div>
                        <div class="contact-card">
                            <div class="contact-icon">📍</div>
                            <h3>Office Location</h3>
                            <p>123 AI Street</p>
                            <p>Tech City, TC 12345</p>
                        </div>
                    </div>
                </div>
            </section>
        </main>
        
        <script>
            // Simple scroll function for inline onclick handlers
            function scrollToSection(sectionId) {{
                console.log('🎯 Inline scroll to:', sectionId);
                const targetSection = document.getElementById(sectionId);
                if (targetSection) {{
                    const headerHeight = 80;
                    const targetPosition = targetSection.offsetTop - headerHeight - 20;
                    window.scrollTo({{
                        top: Math.max(0, targetPosition),
                        behavior: 'smooth'
                    }});
                    console.log('✅ Inline scroll successful');
                }} else {{
                    console.error('❌ Section not found:', sectionId);
                }}
            }}
            
            // Chat functionality
            let chatHistory = [];
            
            function handleChatKeyPress(event) {{
                if (event.key === 'Enter' && !event.shiftKey) {{
                    event.preventDefault();
                    sendMessage();
                }}
            }}
            
            async function sendMessage() {{
                const input = document.getElementById('chatInput');
                const message = input.value.trim();
                
                if (!message) return;
                
                // Add user message to chat
                addMessage(message, 'user');
                input.value = '';
                
                // Disable send button and show typing
                const sendBtn = document.getElementById('sendBtn');
                sendBtn.disabled = true;
                showTypingIndicator();
                
                try {{
                    // Call the query API
                    const response = await fetch('/api/query', {{
                        method: 'POST',
                        headers: {{
                            'Content-Type': 'application/json',
                        }},
                        body: JSON.stringify({{
                            query: message,
                            document_ids: []
                        }}),
                        credentials: 'same-origin'
                    }});
                    
                    const result = await response.json();
                    
                    // Remove typing indicator
                    removeTypingIndicator();
                    
                    if (response.ok) {{
                        const botResponse = formatBotResponse(result, message);
                        addMessage(botResponse, 'bot');
                    }} else {{
                        addMessage("Sorry, I encountered an error while processing your question. Please try again.", 'bot');
                    }}
                    
                }} catch (error) {{
                    console.error("Chat error:", error);
                    removeTypingIndicator();
                    addMessage("Sorry, I'm having trouble connecting right now. Please try again later.", 'bot');
                }} finally {{
                    sendBtn.disabled = false;
                }}
            }}
            
            function sendQuickQuestion(question) {{
                const input = document.getElementById('chatInput');
                input.value = question;
                sendMessage();
            }}
            
            function addMessage(content, type) {{
                const messagesContainer = document.getElementById('chatMessages');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${{type}}-message`;
                
                const avatar = type === 'user' ? '👤' : '🤖';
                const time = new Date().toLocaleTimeString([], {{hour: '2-digit', minute:'2-digit'}});
                
                messageDiv.innerHTML = `
                    <div class="message-avatar">${{avatar}}</div>
                    <div class="message-content">
                        <div class="message-text">${{content}}</div>
                        <div class="message-time">${{time}}</div>
                    </div>
                `;
                
                messagesContainer.appendChild(messageDiv);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
                
                // Store in chat history
                chatHistory.push({{type, content, time}});
            }}
            
            function showTypingIndicator() {{
                const messagesContainer = document.getElementById('chatMessages');
                const typingDiv = document.createElement('div');
                typingDiv.className = 'message bot-message';
                typingDiv.id = 'typing-indicator';
                
                typingDiv.innerHTML = `
                    <div class="message-avatar">🤖</div>
                    <div class="message-content">
                        <div class="message-text">Typing...</div>
                    </div>
                `;
                
                messagesContainer.appendChild(typingDiv);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }}
            
            function removeTypingIndicator() {{
                const typingIndicator = document.getElementById('typing-indicator');
                if (typingIndicator) {{
                    typingIndicator.remove();
                }}
            }}
            
            function formatBotResponse(result, originalQuery) {{
                if (result.answer) {{
                    return result.answer;
                }}

                if (result.results && result.results.length > 0) {{
                    let response = `<div style="margin-bottom: 16px;">
                        <strong>📋 Based on your documents, here's what I found:</strong>
                    </div>`;
                    
                    result.results.slice(0, 3).forEach((item, index) => {{
                        response += `
                            <div style="background: #f8fafc; padding: 12px; border-radius: 8px; margin: 8px 0; border-left: 3px solid #2563eb;">
                                <div style="font-size: 13px; color: #64748b; margin-bottom: 4px;">
                                    📄 ${{item.filename}} (Relevance: ${{(item.score * 100).toFixed(1)}}%)
                                </div>
                                <div style="font-size: 14px; line-height: 1.4;">
                                    ${{item.text.substring(0, 200)}}${{item.text.length > 200 ? '...' : ''}}
                                </div>
                            </div>
                        `;
                    }});
                    
                    if (result.results.length > 3) {{
                        response += `<div style="font-size: 13px; color: #64748b; margin-top: 8px;">
                            And ${{result.results.length - 3}} more relevant sections found.
                        </div>`;
                    }}
                    
                    return response;
                }} else {{
                    return `I couldn't find specific information about "${{originalQuery}}" in your uploaded documents. Try rephrasing your question or upload more relevant documents.`;
                }}
            }}
            
            function clearChat() {{
                const messagesContainer = document.getElementById('chatMessages');
                const initialMessage = messagesContainer.querySelector('.message.bot-message');
                messagesContainer.innerHTML = '';
                if (initialMessage) {{
                    messagesContainer.appendChild(initialMessage);
                }}
                chatHistory = [];
            }}
            
            // File Upload Functionality
            document.addEventListener('DOMContentLoaded', function() {{
                const fileInput = document.getElementById('fileInput');
                const uploadStatus = document.getElementById('uploadStatus');
                const uploadDropzone = document.getElementById('uploadDropzone');
                
                // Load user documents on page load
                loadUserDocuments();
                
                // File input change handler
                if (fileInput) {{
                    fileInput.addEventListener('change', function(e) {{
                        const files = Array.from(e.target.files);
                        if (files.length > 0) {{
                            uploadFiles(files);
                        }}
                    }});
                }}
                
                // Drag and drop functionality
                if (uploadDropzone) {{
                    uploadDropzone.addEventListener('dragover', function(e) {{
                        e.preventDefault();
                        uploadDropzone.classList.add('dragover');
                    }});
                    
                    uploadDropzone.addEventListener('dragleave', function(e) {{
                        e.preventDefault();
                        uploadDropzone.classList.remove('dragover');
                    }});
                    
                    uploadDropzone.addEventListener('drop', function(e) {{
                        e.preventDefault();
                        uploadDropzone.classList.remove('dragover');
                        
                        const files = Array.from(e.dataTransfer.files);
                        if (files.length > 0) {{
                            uploadFiles(files);
                        }}
                    }});
                }}
                
                async function uploadFiles(files) {{
                    const formData = new FormData();
                    files.forEach(file => {{
                        formData.append('files', file);
                    }});
                    
                    uploadStatus.innerHTML = '<div class="upload-status processing">📤 Uploading and processing files...</div>';
                    
                    try {{
                        const response = await fetch('/api/upload', {{
                            method: 'POST',
                            body: formData,
                            credentials: 'same-origin'
                        }});
                        
                        const result = await response.json();
                        
                        if (response.ok) {{
                            uploadStatus.innerHTML = `<div class="upload-status success">✅ ${{result.message}}</div>`;
                            
                            // Clear file input
                            fileInput.value = '';
                            
                            // Reload documents list
                            setTimeout(() => {{
                                loadUserDocuments();
                                uploadStatus.innerHTML = '';
                            }}, 2000);
                            
                        }} else {{
                            uploadStatus.innerHTML = `<div class="upload-status error">❌ ${{result.error || 'Upload failed'}}</div>`;
                        }}
                        
                    }} catch (error) {{
                        console.error("Upload error:", error);
                        uploadStatus.innerHTML = '<div class="upload-status error">❌ Network error. Please try again.</div>';
                    }}
                }}
            }});
            
            // Load user documents function
            async function loadUserDocuments() {{
                const documentsList = document.getElementById('documentsList');
                
                if (!documentsList) return;
                
                try {{
                    documentsList.innerHTML = '<div class="loading-documents">Loading documents...</div>';
                    
                    const response = await fetch('/api/documents', {{
                        method: 'GET',
                        credentials: 'same-origin'
                    }});
                    
                    const result = await response.json();
                    
                    if (response.ok) {{
                        if (result.documents && result.documents.length > 0) {{
                            documentsList.innerHTML = '';
                            result.documents.forEach(doc => {{
                                const docItem = document.createElement('div');
                                docItem.className = 'document-item';
                                
                                // Format processing stats
                                let processingInfo = '';
                                if (doc.processing_stats && doc.processing_stats.success) {{
                                    const stats = doc.processing_stats;
                                    processingInfo = `
                                        <div class="processing-stats">
                                            <div class="stats-row">
                                                <span class="stat-label">📊 Pinecone Records:</span>
                                                <span class="stat-value">${{stats.pinecone_records || 0}}</span>
                                            </div>
                                            <div class="stats-row">
                                                <span class="stat-label">🔪 Chunks:</span>
                                                <span class="stat-value">${{stats.processed_chunks || 0}}</span>
                                            </div>
                                        </div>
                                    `;
                                }} else {{
                                    processingInfo = '<div class="processing-status">🔄 Processing...</div>';
                                }}
                                
                                docItem.innerHTML = `
                                    <div class="document-info">
                                        <div class="document-icon file-type-${{doc.file_type}}">
                                            ${{getFileIcon(doc.file_type)}}
                                        </div>
                                        <div class="document-details">
                                            <div class="document-name">${{doc.original_filename}}</div>
                                            <div class="document-meta">
                                                <span>${{formatFileSize(doc.file_size)}}</span>
                                                <span>${{doc.file_type.toUpperCase()}}</span>
                                                <span>${{formatDate(doc.upload_date)}}</span>
                                            </div>
                                            ${{processingInfo}}
                                        </div>
                                    </div>
                                    <div class="document-actions">
                                        <button class="delete-btn" onclick="deleteDocument(${{doc.id}}, '${{doc.original_filename}}')">
                                            🗑️ Remove
                                        </button>
                                    </div>
                                `;
                                documentsList.appendChild(docItem);
                            }});
                        }} else {{
                            documentsList.innerHTML = `
                                <div class="no-documents">
                                    <div style="font-size: 48px; margin-bottom: 16px;">📁</div>
                                    <div style="font-size: 16px; font-weight: 600; margin-bottom: 8px;">No documents uploaded yet</div>
                                    <div style="font-size: 14px;">Upload your first document to get started</div>
                                </div>
                            `;
                        }}
                    }} else {{
                        documentsList.innerHTML = `<div class="loading-documents" style="color: #ef4444;">Error loading documents: ${{result.error}}</div>`;
                    }}
                    
                }} catch (error) {{
                    console.error("Error loading documents:", error);
                    documentsList.innerHTML = '<div class="loading-documents" style="color: #ef4444;">Network error loading documents</div>';
                }}
            }}
            
            // Delete document function
            async function deleteDocument(docId, filename) {{
                if (!confirm(`Are you sure you want to delete "${{filename}}"? This action cannot be undone.`)) {{
                    return;
                }}
                
                try {{
                    const response = await fetch(`/api/documents/${{docId}}`, {{
                        method: 'DELETE',
                        credentials: 'same-origin'
                    }});
                    
                    const result = await response.json();
                    
                    if (response.ok) {{
                        const uploadStatus = document.getElementById('uploadStatus');
                        uploadStatus.innerHTML = '<div class="upload-status success">✅ Document deleted successfully</div>';
                        
                        loadUserDocuments();
                        
                        setTimeout(() => {{
                            uploadStatus.innerHTML = '';
                        }}, 3000);
                        
                    }} else {{
                        alert(`Error deleting document: ${{result.error}}`);
                    }}
                    
                }} catch (error) {{
                    console.error("Delete error:", error);
                    alert("Network error. Please try again.");
                }}
            }}
            
            // Helper functions
            function formatFileSize(bytes) {{
                if (bytes === 0) return '0 Bytes';
                const k = 1024;
                const sizes = ['Bytes', 'KB', 'MB', 'GB'];
                const i = Math.floor(Math.log(bytes) / Math.log(k));
                return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
            }}
            
            function getFileIcon(fileType) {{
                const icons = {{
                    'pdf': '📄',
                    'doc': '📝',
                    'docx': '📝',
                    'txt': '📄',
                    'ppt': '📊',
                    'pptx': '📊',
                    'xls': '📈',
                    'xlsx': '📈'
                }};
                return icons[fileType.toLowerCase()] || '📄';
            }}
            
            function formatDate(dateString) {{
                const date = new Date(dateString);
                return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {{hour: '2-digit', minute:'2-digit'}});
            }}
            
            // Navigation functionality
            document.addEventListener('DOMContentLoaded', function() {{
                console.log('🔧 Setting up navigation...');
                
                const navLinks = document.querySelectorAll('.nav-link[href^="#"]');
                console.log('📋 Found navigation links:', navLinks.length);
                
                function scrollToElement(targetId) {{
                    console.log('🎯 Scrolling to:', targetId);
                    const targetSection = document.querySelector(targetId);
                    console.log('📍 Target section found:', !!targetSection);
                    
                    if (targetSection) {{
                        const headerHeight = 80;
                        const targetPosition = targetSection.offsetTop - headerHeight - 20;
                        console.log('📏 Scroll position:', targetPosition);
                        
                        window.scrollTo({{
                            top: Math.max(0, targetPosition),
                            behavior: 'smooth'
                        }});
                        return true;
                    }} else {{
                        console.error('❌ Section not found:', targetId);
                        return false;
                    }}
                }}
                
                // Add click handlers to navigation links
                navLinks.forEach((link, index) => {{
                    const href = link.getAttribute('href');
                    console.log(`🔗 Setting up link ${{index + 1}}: ${{href}}`);
                    
                    link.addEventListener('click', function(e) {{
                        console.log('🖱️ Navigation link clicked:', href);
                        e.preventDefault();
                        
                        const targetId = this.getAttribute('href');
                        
                        if (scrollToElement(targetId)) {{
                            // Update active states
                            navLinks.forEach(l => l.classList.remove('active'));
                            this.classList.add('active');
                            console.log('✅ Navigation successful');
                        }} else {{
                            console.error('❌ Navigation failed for:', targetId);
                        }}
                    }});
                }});
                
                // Handle action buttons (Upload Documents, Start Querying, etc.)
                const actionButtons = document.querySelectorAll('.btn-primary[href^="#"], .btn-secondary[href^="#"]');
                console.log('🎯 Found action buttons:', actionButtons.length);
                
                actionButtons.forEach((button, index) => {{
                    const href = button.getAttribute('href');
                    console.log(`🔘 Setting up button ${{index + 1}}: ${{href}}`);
                    
                    button.addEventListener('click', function(e) {{
                        console.log('🖱️ Action button clicked:', href);
                        e.preventDefault();
                        
                        const targetId = this.getAttribute('href');
                        
                        if (scrollToElement(targetId)) {{
                            // Update active nav link
                            navLinks.forEach(l => l.classList.remove('active'));
                            const correspondingNavLink = document.querySelector(`.nav-link[href="${{targetId}}"]`);
                            if (correspondingNavLink) {{
                                correspondingNavLink.classList.add('active');
                                console.log('✅ Updated active nav link');
                            }}
                        }}
                    }});
                }});
                
                // Test if sections exist
                const sectionsToTest = ['#upload', '#query', '#how-it-works', '#use-cases', '#contact'];
                sectionsToTest.forEach(sectionId => {{
                    const section = document.querySelector(sectionId);
                    console.log(`📋 Section ${{sectionId}}: ${{section ? '✅ Found' : '❌ Missing'}}`);
                }});
                
                console.log('✅ Navigation setup complete');
            }});
        </script>
        
        <footer class="footer">
            <div class="footer-content">
                <div class="footer-grid">
                    <div class="footer-section">
                        <h3>AI-Based Smart File Assistant</h3>
                        <p>Revolutionizing document management with intelligent contextual querying and efficient information extraction from multiple documents.</p>
                        <p>Upload, analyze, and query your documents with the power of AI.</p>
                    </div>
                    <div class="footer-section">
                        <h3>Features</h3>
                        <div class="footer-links">
                            <a href="#upload" class="footer-link">Document Upload</a>
                            <a href="#query" class="footer-link">Smart Querying</a>
                            <a href="#how-it-works" class="footer-link">How It Works</a>
                            <a href="#contact" class="footer-link">Contact</a>
                        </div>
                    </div>
                    <div class="footer-section">
                        <h3>Account</h3>
                        <div class="footer-links">
                            <a href="/dashboard" class="footer-link">Dashboard</a>
                            <a href="/profile" class="footer-link">Profile Settings</a>
                            <a href="/documents" class="footer-link">My Documents</a>
                            <a href="/history" class="footer-link">Query History</a>
                        </div>
                    </div>
                    <div class="footer-section">
                        <h3>Support</h3>
                        <div class="footer-links">
                            <a href="/help" class="footer-link">Help Center</a>
                            <a href="/contact" class="footer-link">Contact Us</a>
                            <a href="#" class="footer-link">Documentation</a>
                            <a href="#" class="footer-link">API Reference</a>
                        </div>
                    </div>
                </div>
                <div class="footer-bottom">
                    <p>&copy; 2026 AI-Based Smart File Assistant. All rights reserved.</p>
                    <div class="social-links">
                        <a href="#" class="social-link">📧</a>
                        <a href="#" class="social-link">🐙</a>
                        <a href="#" class="social-link">💼</a>
                    </div>
                </div>
            </div>
        </footer>
    </body>
    </html>
    '''