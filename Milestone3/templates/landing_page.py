# Landing page template for the AI-Based Smart File Assistant

def get_landing_page_html():
    """Generate the landing page HTML"""
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI-Based Smart File Assistant For Contextual Querying And Efficient Information Extraction From Multiple Documents</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            html { scroll-behavior: smooth; height: 100%; overflow-x: hidden; overflow-y: auto; }
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #ffffff; min-height: 100vh; color: #333; line-height: 1.6; overflow-x: hidden; padding-top: 80px; }
            .header { background: #ffffff; padding: 16px 0; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); position: fixed; top: 0; left: 0; right: 0; z-index: 1000; }
            .header-content { max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; padding: 0 24px; }
            .logo { display: flex; align-items: center; gap: 12px; font-size: 16px; font-weight: 600; color: #2563eb; white-space: nowrap; }
            .logo-icon { width: 40px; height: 40px; background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 18px; font-weight: bold; }
            .nav-menu { display: flex; align-items: center; gap: 32px; }
            .nav-link { color: #64748b; text-decoration: none; font-weight: 500; font-size: 15px; transition: color 0.2s; padding: 8px 0; cursor: pointer; position: relative; }
            .nav-link:hover { color: #2563eb; }
            .nav-link.active { color: #2563eb; }
            .nav-link.active::after { content: ''; position: absolute; bottom: -4px; left: 0; right: 0; height: 2px; background: #2563eb; border-radius: 1px; }
            .auth-buttons { display: flex; align-items: center; gap: 16px; }
            .btn-signin { color: #2563eb; text-decoration: none; font-weight: 500; padding: 8px 16px; border-radius: 6px; transition: all 0.2s; }
            .btn-signin:hover { background: #f1f5f9; }
            .btn-get-started { background: #2563eb; color: white; text-decoration: none; font-weight: 500; padding: 10px 20px; border-radius: 8px; transition: all 0.2s; }
            .btn-get-started:hover { background: #1d4ed8; transform: translateY(-1px); }
            .hero-section { background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 25%, #f1f5f9 50%, #e2e8f0 75%, #f8fafc 100%); padding: 80px 0; position: relative; overflow: hidden; }
            .hero-content { max-width: 1200px; margin: 0 auto; padding: 0 24px; display: grid; grid-template-columns: 1fr 1fr; gap: 60px; align-items: center; }
            .hero-text { z-index: 10; position: relative; }
            .ai-badge { background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; padding: 8px 16px; border-radius: 20px; font-size: 14px; font-weight: 600; display: inline-block; margin-bottom: 24px; }
            .hero-title { font-size: 48px; font-weight: 700; color: #1e293b; line-height: 1.2; margin-bottom: 24px; }
            .hero-description { font-size: 18px; color: #64748b; line-height: 1.6; margin-bottom: 32px; }
            .hero-button { background: #2563eb; color: white; padding: 16px 32px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 16px; transition: all 0.3s ease; display: inline-block; }
            .hero-button:hover { background: #1d4ed8; transform: translateY(-2px); box-shadow: 0 8px 20px rgba(37, 99, 235, 0.4); }
            .hero-image { position: relative; height: 500px; }
            .ai-visual { position: relative; width: 100%; height: 100%; }
            
            /* Modern AI Illustration Styles */
            .modern-illustration { position: relative; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; overflow: hidden; }
            .ai-brain-center { position: relative; z-index: 10; animation: brainFloat 4s ease-in-out infinite; }
            .brain-core { width: 120px; height: 120px; background: rgba(255, 255, 255, 0.95); border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2); backdrop-filter: blur(10px); border: 2px solid rgba(255, 255, 255, 0.3); position: relative; }
            .neural-network { position: relative; width: 80px; height: 80px; }
            .neuron { position: absolute; width: 12px; height: 12px; background: linear-gradient(135deg, #3b82f6, #1d4ed8); border-radius: 50%; box-shadow: 0 0 20px rgba(59, 130, 246, 0.6); animation: neuronPulse 2s ease-in-out infinite; }
            .neuron.n1 { top: 10px; left: 35px; animation-delay: 0s; }
            .neuron.n2 { top: 35px; left: 10px; animation-delay: 0.5s; }
            .neuron.n3 { top: 35px; right: 10px; animation-delay: 1s; }
            .neuron.n4 { bottom: 10px; left: 35px; animation-delay: 1.5s; }
            .connection { position: absolute; background: linear-gradient(90deg, rgba(59, 130, 246, 0.8), rgba(29, 78, 216, 0.4)); height: 2px; border-radius: 1px; animation: connectionFlow 3s ease-in-out infinite; }
            .connection.c1 { top: 40px; left: 22px; width: 36px; transform: rotate(-45deg); animation-delay: 0.2s; }
            .connection.c2 { top: 40px; right: 22px; width: 36px; transform: rotate(45deg); animation-delay: 0.7s; }
            .connection.c3 { bottom: 22px; left: 35px; width: 30px; transform: rotate(90deg); animation-delay: 1.2s; }
            .ai-glow { position: absolute; top: -20px; left: -20px; right: -20px; bottom: -20px; background: radial-gradient(circle, rgba(59, 130, 246, 0.3) 0%, transparent 70%); border-radius: 50%; animation: glowPulse 3s ease-in-out infinite; }
            
            /* Floating Documents */
            .floating-docs { position: absolute; width: 100%; height: 100%; }
            .doc-card { position: absolute; width: 100px; height: 120px; background: rgba(255, 255, 255, 0.9); border-radius: 12px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15); padding: 12px; backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.3); animation: docFloat 6s ease-in-out infinite; }
            .doc1 { top: 20px; left: 20px; animation-delay: 0s; transform: rotate(-8deg); }
            .doc2 { top: 60px; right: 30px; animation-delay: 2s; transform: rotate(12deg); }
            .doc3 { bottom: 40px; left: 40px; animation-delay: 4s; transform: rotate(-5deg); }
            .doc-header { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid rgba(0, 0, 0, 0.1); }
            .doc-type { width: 20px; height: 20px; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: bold; color: white; }
            .doc-type.pdf { background: #dc3545; }
            .doc-type.docx { background: #2563eb; }
            .doc-type.txt { background: #10b981; }
            .doc-type.pdf::after { content: 'PDF'; }
            .doc-type.docx::after { content: 'DOC'; }
            .doc-type.txt::after { content: 'TXT'; }
            .doc-name { font-size: 10px; font-weight: 600; color: #374151; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
            .doc-content { display: flex; flex-direction: column; gap: 6px; }
            .text-line { height: 3px; background: linear-gradient(90deg, #e5e7eb, #d1d5db); border-radius: 2px; animation: textShimmer 2s ease-in-out infinite; }
            .text-line.short { width: 60%; }
            
            /* Animations */
            @keyframes brainFloat { 0%, 100% { transform: translateY(0px) scale(1); } 50% { transform: translateY(-15px) scale(1.05); } }
            @keyframes neuronPulse { 0%, 100% { transform: scale(1); box-shadow: 0 0 20px rgba(59, 130, 246, 0.6); } 50% { transform: scale(1.2); box-shadow: 0 0 30px rgba(59, 130, 246, 1); } }
            @keyframes connectionFlow { 0% { opacity: 0.3; } 50% { opacity: 1; } 100% { opacity: 0.3; } }
            @keyframes glowPulse { 0%, 100% { opacity: 0.5; transform: scale(1); } 50% { opacity: 0.8; transform: scale(1.1); } }
            @keyframes docFloat { 0%, 100% { transform: translateY(0px) rotate(var(--rotation, 0deg)); } 50% { transform: translateY(-20px) rotate(var(--rotation, 0deg)); } }
            @keyframes textShimmer { 0%, 100% { opacity: 0.6; } 50% { opacity: 1; } }
            
            .geometric-bg { position: absolute; top: 0; left: 0; right: 0; bottom: 0; opacity: 0.1; background-image: radial-gradient(circle at 20% 80%, #3b82f6 0%, transparent 50%), radial-gradient(circle at 80% 20%, #1d4ed8 0%, transparent 50%); }
            
            .features-section { padding: 80px 0; background: #ffffff; }
            .features-content { max-width: 1200px; margin: 0 auto; padding: 0 24px; }
            .section-title { font-size: 36px; font-weight: 700; color: #1e293b; text-align: center; margin-bottom: 16px; }
            .section-subtitle { font-size: 18px; color: #64748b; text-align: center; margin-bottom: 60px; max-width: 600px; margin-left: auto; margin-right: auto; }
            .features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 40px; }
            .feature-card { background: #f8fafc; padding: 40px 30px; border-radius: 16px; text-align: center; transition: all 0.3s ease; border: 1px solid #e2e8f0; }
            .feature-card:hover { transform: translateY(-5px); box-shadow: 0 10px 30px rgba(37, 99, 235, 0.1); }
            .feature-icon { width: 60px; height: 60px; background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px; font-size: 24px; color: white; }
            .feature-card h3 { font-size: 20px; font-weight: 600; color: #1e293b; margin-bottom: 12px; }
            .feature-card p { color: #64748b; line-height: 1.6; }
            
            /* How It Works Section */
            .how-it-works-section { padding: 80px 0; background: #f8fafc; }
            .steps-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 40px; margin-top: 60px; }
            .step-card { background: #ffffff; padding: 30px; border-radius: 16px; text-align: center; border: 1px solid #e2e8f0; }
            .step-number { width: 50px; height: 50px; background: #2563eb; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; font-weight: 700; margin: 0 auto 20px; }
            .step-card h3 { font-size: 18px; font-weight: 600; color: #1e293b; margin-bottom: 12px; }
            .step-card p { color: #64748b; line-height: 1.6; }
            
            /* Contact Section */
            .contact-section { padding: 80px 0; background: #f8fafc; }
            .contact-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px; margin-top: 60px; }
            .contact-card { background: #ffffff; padding: 30px; border-radius: 16px; text-align: center; border: 1px solid #e2e8f0; transition: all 0.3s ease; }
            .contact-card:hover { transform: translateY(-5px); box-shadow: 0 10px 30px rgba(37, 99, 235, 0.1); }
            .contact-icon { width: 60px; height: 60px; background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px; font-size: 24px; color: white; }
            .contact-card h3 { font-size: 18px; font-weight: 600; color: #1e293b; margin-bottom: 12px; }
            .contact-card p { color: #64748b; line-height: 1.6; margin-bottom: 8px; }
            .contact-card p:last-child { font-size: 14px; opacity: 0.8; }
            
            @media (max-width: 768px) { 
                .hero-content { grid-template-columns: 1fr; gap: 40px; text-align: center; } 
                .hero-title { font-size: 36px; } 
                .nav-menu { display: none; } 
                .features-grid { grid-template-columns: 1fr; }
                .steps-grid { grid-template-columns: 1fr; }
                .use-cases-grid { grid-template-columns: 1fr; }
                .contact-grid { grid-template-columns: 1fr; }
                .section-title { font-size: 28px; }
            }
        </style>
    </head>
    <body>
        <header class="header">
            <div class="header-content">
                <div class="logo">
                    <div class="logo-icon">🤖</div>
                    <span style="white-space: nowrap;">AI-Based Smart File Assistant</span>
                </div>
                
                <nav class="nav-menu">
                    <a href="#features" class="nav-link">Features</a>
                    <a href="#how-it-works" class="nav-link">How It Works</a>
                    <a href="#contact" class="nav-link">Contact</a>
                </nav>
                
                <div class="auth-buttons">
                    <a href="/auth" class="btn-signin">Sign In</a>
                    <a href="/auth?mode=signup" class="btn-get-started">Get Started</a>
                </div>
            </div>
        </header>

        <section class="hero-section">
            <div class="geometric-bg"></div>
            <div class="hero-content">
                <div class="hero-text">
                    <div class="ai-badge">🚀 AI-Powered Intelligence</div>
                    <h1 class="hero-title">AI-Based Smart File Assistant</h1>
                    <p class="hero-description">
                        Harness the power of AI for contextual querying and efficient 
                        information extraction from multiple documents. Get instant 
                        answers from your files.
                    </p>
                    <a href="/auth?mode=signup" class="hero-button">Explore Now</a>
                </div>
                
                <div class="hero-image">
                    <div class="ai-visual">
                        <div class="modern-illustration">
                            <!-- AI Brain Center -->
                            <div class="ai-brain-center">
                                <div class="brain-core">
                                    <div class="neural-network">
                                        <div class="neuron n1"></div>
                                        <div class="neuron n2"></div>
                                        <div class="neuron n3"></div>
                                        <div class="neuron n4"></div>
                                        <div class="connection c1"></div>
                                        <div class="connection c2"></div>
                                        <div class="connection c3"></div>
                                    </div>
                                </div>
                                <div class="ai-glow"></div>
                            </div>
                            
                            <!-- Floating Documents -->
                            <div class="floating-docs">
                                <div class="doc-card doc1">
                                    <div class="doc-header">
                                        <div class="doc-type pdf"></div>
                                        <div class="doc-name">Report.pdf</div>
                                    </div>
                                    <div class="doc-content">
                                        <div class="text-line"></div>
                                        <div class="text-line short"></div>
                                        <div class="text-line"></div>
                                    </div>
                                </div>
                                
                                <div class="doc-card doc2">
                                    <div class="doc-header">
                                        <div class="doc-type docx"></div>
                                        <div class="doc-name">Contract.docx</div>
                                    </div>
                                    <div class="doc-content">
                                        <div class="text-line"></div>
                                        <div class="text-line"></div>
                                        <div class="text-line short"></div>
                                    </div>
                                </div>
                                
                                <div class="doc-card doc3">
                                    <div class="doc-header">
                                        <div class="doc-type txt"></div>
                                        <div class="doc-name">Notes.txt</div>
                                    </div>
                                    <div class="doc-content">
                                        <div class="text-line short"></div>
                                        <div class="text-line"></div>
                                        <div class="text-line"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        
        <section id="features" class="features-section">
            <div class="features-content">
                <h2 class="section-title">Powerful Features</h2>
                <p class="section-subtitle">
                    Discover the advanced capabilities that make our AI assistant the perfect solution for your document management needs.
                </p>
                <div class="features-grid">
                    <div class="feature-card">
                        <div class="feature-icon">📁</div>
                        <h3>Smart File Upload</h3>
                        <p>Upload multiple document formats including PDF, DOCX, PPT, and TXT. Our system automatically processes and indexes your content for intelligent querying.</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">🔍</div>
                        <h3>Contextual Querying</h3>
                        <p>Ask natural language questions about your documents. Our AI understands context and provides accurate, relevant answers from your uploaded content.</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">📊</div>
                        <h3>Information Extraction</h3>
                        <p>Efficiently extract key information, summaries, and insights from large documents. Save time with automated analysis and data extraction.</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">🔗</div>
                        <h3>Multi-Document Analysis</h3>
                        <p>Analyze relationships and connections across multiple documents. Get comprehensive insights from your entire document collection.</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">⚡</div>
                        <h3>Lightning Fast</h3>
                        <p>Get instant responses to your queries with our optimized AI processing pipeline. No waiting, just immediate insights.</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">🔒</div>
                        <h3>Secure & Private</h3>
                        <p>Your documents are processed securely with enterprise-grade encryption. Your data privacy is our top priority.</p>
                    </div>
                </div>
            </div>
        </section>
        
        <section id="how-it-works" class="how-it-works-section">
            <div class="features-content">
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
        
        <section id="contact" class="contact-section">
            <div class="features-content">
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
        
        <script>
            // Enhanced smooth scrolling with active navigation highlighting
            document.addEventListener('DOMContentLoaded', function() {
                console.log('DOM loaded, initializing smooth scrolling...');
                
                // Smooth scrolling for navigation links
                const navLinks = document.querySelectorAll('.nav-link[href^="#"]');
                console.log('Found navigation links:', navLinks.length);
                
                navLinks.forEach(link => {
                    console.log('Setting up link:', link.getAttribute('href'));
                    link.addEventListener('click', function(e) {
                        console.log('Navigation link clicked:', this.getAttribute('href'));
                        e.preventDefault();
                        
                        const targetId = this.getAttribute('href');
                        const targetSection = document.querySelector(targetId);
                        console.log('Target section found:', !!targetSection);
                        
                        if (targetSection) {
                            const headerHeight = 80; // Fixed header height
                            const targetPosition = targetSection.offsetTop - headerHeight - 20;
                            console.log('Scrolling to position:', targetPosition);
                            
                            window.scrollTo({
                                top: targetPosition,
                                behavior: 'smooth'
                            });
                            
                            // Update active link
                            navLinks.forEach(l => l.classList.remove('active'));
                            this.classList.add('active');
                            console.log('Active link updated');
                        }
                    });
                });
                
                console.log('Smooth scrolling setup complete');
            });
        </script>
    </body>
    </html>
    '''