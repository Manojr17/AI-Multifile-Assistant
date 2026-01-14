// Form switching functionality
function switchToSignup(event) {
    event.preventDefault();
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    
    loginForm.classList.remove('active');
    signupForm.classList.add('active');
}

function switchToLogin(event) {
    event.preventDefault();
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    
    signupForm.classList.remove('active');
    loginForm.classList.add('active');
}

// Profile picture preview
function previewImage(event) {
    const file = event.target.files[0];
    const preview = document.getElementById('profilePreview');
    
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.innerHTML = `<img src="${e.target.result}" alt="Profile Preview">`;
        };
        reader.readAsDataURL(file);
    }
}

// Form validation
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function validatePassword(password) {
    // Require: 8+ chars, 1 uppercase, 1 lowercase, 1 number, 1 special char, no spaces
    const rules = evaluatePasswordRules(password);
    return Object.values(rules).every(rule => rule === true);
}

function evaluatePasswordRules(password) {
    return {
        length: password.length >= 8,
        uppercase: /[A-Z]/.test(password),
        lowercase: /[a-z]/.test(password),
        number: /\d/.test(password),
        special: /[@$!%*?&]/.test(password),
        nospace: !/\s/.test(password)
    };
}

function updateChecklist(password) {
    const rules = evaluatePasswordRules(password);
    const items = document.querySelectorAll('#passwordChecklist .item');
    items.forEach(item => {
        const rule = item.getAttribute('data-rule');
        if (rules[rule]) {
            item.classList.add('valid');
            item.classList.remove('invalid');
        } else {
            item.classList.add('invalid');
            item.classList.remove('valid');
        }
    });
}

function updateStrengthMeter(password) {
    const rules = evaluatePasswordRules(password);
    const passed = Object.values(rules).filter(Boolean).length;
    const bar = document.getElementById('strengthBar');
    if (!bar) return;
    const percent = Math.min(100, Math.round((passed / Object.keys(rules).length) * 100));
    bar.style.width = percent + '%';
    if (percent <= 33) {
        bar.style.background = '#dc3545';
    } else if (percent <= 66) {
        bar.style.background = '#f0ad4e';
    } else {
        bar.style.background = '#28a745';
    }
}

function showMessage(message, type, formId) {
    // Remove existing messages
    const existingMessage = document.querySelector(`#${formId} .message`);
    if (existingMessage) {
        existingMessage.remove();
    }
    
    // Create new message
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    
    // Insert at the beginning of the form
    const form = document.getElementById(formId);
    form.insertBefore(messageDiv, form.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (messageDiv.parentNode) {
            messageDiv.remove();
        }
    }, 5000);
}

function showPopup(message, type = 'success') {
    // Create popup overlay
    const overlay = document.createElement('div');
    overlay.className = 'popup-overlay';
    
    // Create popup content
    const popup = document.createElement('div');
    popup.className = `popup-content ${type}`;
    
    // Add icon based on type
    const icon = type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️';
    
    popup.innerHTML = `
        <div class="popup-icon">${icon}</div>
        <div class="popup-message">${message}</div>
        <button class="popup-close" onclick="closePopup()">OK</button>
    `;
    
    overlay.appendChild(popup);
    document.body.appendChild(overlay);
    
    // Add animation
    setTimeout(() => {
        overlay.classList.add('show');
    }, 10);
    
    // Auto-close after 4 seconds
    setTimeout(() => {
        closePopup();
    }, 4000);
}

function closePopup() {
    const overlay = document.querySelector('.popup-overlay');
    if (overlay) {
        overlay.classList.remove('show');
        setTimeout(() => {
            if (overlay.parentNode) {
                overlay.remove();
            }
        }, 300);
    }
}

function setButtonLoading(button, isLoading) {
    if (isLoading) {
        button.disabled = true;
        button.classList.add('loading');
    } else {
        button.disabled = false;
        button.classList.remove('loading');
    }
}

// Login form handler - POST to backend and follow redirect
document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value;
    const submitButton = this.querySelector('button[type="submit"]');

    // Validation
    if (!email || !password) {
        showPopup('Please fill in all fields', 'error');
        return;
    }

    if (!validateEmail(email)) {
        showPopup('Please enter a valid email address', 'error');
        return;
    }

    setButtonLoading(submitButton, true);

    try {
        const res = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'same-origin',
            body: JSON.stringify({ email, password })
        });

        const data = await res.json().catch(() => ({}));

        if (res.ok && data.redirect) {
            showPopup('🎉 Login successful! Welcome back!', 'success');
            // Follow server-provided redirect after popup shows
            setTimeout(() => {
                window.location.href = data.redirect;
            }, 1500);
            return;
        }

        // If server responded with an error message
        const errMsg = data.error || 'Login failed. Please check your credentials.';
        showPopup(errMsg, 'error');

    } catch (error) {
        showPopup('Network error. Please try again.', 'error');
    } finally {
        setButtonLoading(submitButton, false);
    }
});

// Signup form handler - submit to backend using multipart/form-data
document.getElementById('signupForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const firstName = document.getElementById('firstName').value.trim();
    const lastName = document.getElementById('lastName').value.trim();
    const email = document.getElementById('signupEmail').value.trim();
    const password = document.getElementById('signupPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const profilePicture = document.getElementById('profilePicture').files[0];
    const submitButton = this.querySelector('button[type="submit"]');

    // Validation
    if (!firstName || !lastName || !email || !password || !confirmPassword) {
        showPopup('Please fill in all required fields', 'error');
        return;
    }

    if (!validateEmail(email)) {
        showPopup('Please enter a valid email address', 'error');
        return;
    }

    if (!validatePassword(password)) {
        showPopup('Password must meet all requirements shown below', 'error');
        return;
    }

    if (password !== confirmPassword) {
        showPopup('Passwords do not match', 'error');
        return;
    }

    setButtonLoading(submitButton, true);

    try {
        const res = await fetch('/api/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'same-origin',
            body: JSON.stringify({
                first_name: firstName,
                last_name: lastName,
                email: email,
                password: password
            })
        });

        const data = await res.json().catch(() => ({}));

        if (res.ok) {
            const message = data.redirect ? 
                '🎉 Account created successfully! Redirecting to dashboard...' : 
                '🎉 Account created successfully! You can now log in.';
            showPopup(message, 'success');
            
            if (data.redirect) {
                // Redirect to dashboard after successful signup
                setTimeout(() => {
                    window.location.href = data.redirect;
                }, 1500);
            } else {
                // Reset and switch to login form (fallback)
                this.reset();
                document.getElementById('profilePreview').innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                    </svg>
                `;
                // Switch to login form after popup
                setTimeout(() => {
                    document.getElementById('signupForm').classList.remove('active');
                    document.getElementById('loginForm').classList.add('active');
                }, 2000);
            }
            return;
        }

        // Handle specific error cases
        if (res.status === 400 && data.error && data.error.includes('already exists')) {
            showPopup('⚠️ User already exists! Please try logging in instead.', 'error');
            // Switch to login form for existing users
            setTimeout(() => {
                document.getElementById('signupForm').classList.remove('active');
                document.getElementById('loginForm').classList.add('active');
                // Pre-fill email in login form
                document.getElementById('loginEmail').value = email;
            }, 2000);
            return;
        }

        const errMsg = data.error || 'Signup failed. Please try again.';
        showPopup(errMsg, 'error');

    } catch (error) {
        showPopup('Network error. Please try again.', 'error');
    } finally {
        setButtonLoading(submitButton, false);
    }
});

// Real-time password validation feedback
document.getElementById('signupPassword').addEventListener('input', function() {
    const password = this.value;
    const rules = evaluatePasswordRules(password);
    const isValid = Object.values(rules).every(rule => rule === true);
    
    updateChecklist(password);
    updateStrengthMeter(password);

    if (password.length > 0) {
        if (isValid) {
            this.style.borderColor = '#28a745';
        } else {
            this.style.borderColor = '#dc3545';
        }
    } else {
        this.style.borderColor = '#e1e5e9';
        updateStrengthMeter('');
    }
});

// Real-time confirm password validation
document.getElementById('confirmPassword').addEventListener('input', function() {
    const password = document.getElementById('signupPassword').value;
    const confirmPassword = this.value;
    
    if (confirmPassword.length > 0) {
        if (password === confirmPassword) {
            this.style.borderColor = '#28a745';
        } else {
            this.style.borderColor = '#dc3545';
        }
    } else {
        this.style.borderColor = '#e1e5e9';
    }
});

// Email validation feedback
function addEmailValidation(inputId) {
    document.getElementById(inputId).addEventListener('blur', function() {
        const email = this.value.trim();
        if (email.length > 0) {
            if (validateEmail(email)) {
                this.style.borderColor = '#28a745';
            } else {
                this.style.borderColor = '#dc3545';
            }
        } else {
            this.style.borderColor = '#e1e5e9';
        }
    });
}

addEmailValidation('loginEmail');
addEmailValidation('signupEmail');

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Check URL parameter to determine which form to show
    const urlParams = new URLSearchParams(window.location.search);
    const mode = urlParams.get('mode');
    
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    
    // Remove active class from both forms first
    loginForm.classList.remove('active');
    signupForm.classList.remove('active');
    
    // Show the appropriate form based on mode parameter
    if (mode === 'signup') {
        signupForm.classList.add('active');
    } else {
        // Default to login form
        loginForm.classList.add('active');
    }
    
    // Add smooth transitions
    const forms = document.querySelectorAll('.form');
    forms.forEach(form => {
        form.style.transition = 'all 0.3s ease';
    });
});