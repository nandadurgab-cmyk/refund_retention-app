import streamlit as st
import re
from auth import register_user

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    if not re.search(r"[a-z]", password):
        return False, "Must contain lowercase letters"
    if not re.search(r"[A-Z]", password):
        return False, "Must contain uppercase letters"
    if not re.search(r"\d", password):
        return False, "Must contain numbers"
    return True, "Strong password"

def show_register():
    """Display registration page with modern design"""
    
    # Hide Streamlit default elements
    st.markdown("""
        <style>
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Page background - Deep Blue */
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        }
        
        /* Main container */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }
        
        /* All text inputs */
        .stTextInput input {
            background-color: #ffffff !important;
            color: #1e293b !important;
            border: 2px solid #cbd5e1 !important;
            border-radius: 12px !important;
            padding: 14px 16px !important;
            font-size: 15px !important;
            transition: all 0.3s ease !important;
        }
        
        .stTextInput input:focus {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1) !important;
            outline: none !important;
        }
        
        .stTextInput input::placeholder {
            color: #94a3b8 !important;
        }
        
        /* Labels */
        .stTextInput label {
            color: #1e293b !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            margin-bottom: 8px !important;
        }
        
        /* Buttons */
        .stButton button {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 14px 28px !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            width: 100% !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 14px rgba(59, 130, 246, 0.4) !important;
        }
        
        .stButton button:hover {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5) !important;
        }
        
        /* Form container */
        [data-testid="stForm"] {
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
        }
        
        /* Password strength indicator */
        .password-strength-weak {
            background: #fef2f2;
            color: #991b1b;
            padding: 12px 16px;
            border-radius: 10px;
            border-left: 4px solid #ef4444;
            margin-top: 8px;
            font-size: 14px;
            font-weight: 500;
        }
        
        .password-strength-strong {
            background: #f0fdf4;
            color: #166534;
            padding: 12px 16px;
            border-radius: 10px;
            border-left: 4px solid #22c55e;
            margin-top: 8px;
            font-size: 14px;
            font-weight: 500;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header section
    st.markdown("""
        <div style='text-align: center; margin-bottom: 2.5rem;'>
            <h1 style='color: #ffffff; font-size: 3rem; font-weight: 800; margin-bottom: 0.5rem; text-shadow: 0 2px 10px rgba(0,0,0,0.3);'>
                📦 Refund Prediction System
            </h1>
            <p style='color: #cbd5e1; font-size: 1.25rem; font-weight: 400;'>
                Create your analyst account
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Create centered columns
    col1, col2, col3 = st.columns([0.3, 2.4, 0.3])
    
    with col2:
        # Register card
        st.markdown("""
            <div style='
                background: #ffffff;
                border-radius: 24px;
                padding: 48px 40px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            '>
                <div style='text-align: center; margin-bottom: 32px;'>
                    <div style='
                        background: linear-gradient(135deg, #3b82f6, #2563eb);
                        width: 80px;
                        height: 80px;
                        border-radius: 20px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        margin: 0 auto 20px;
                        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4);
                    '>
                        <span style='font-size: 40px;'>📝</span>
                    </div>
                    <h2 style='color: #1e293b; font-size: 1.875rem; font-weight: 700; margin: 0 0 8px 0;'>
                        Create Account
                    </h2>
                    <p style='color: #64748b; font-size: 1rem; margin: 0;'>
                        Join our prediction platform
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        # Registration form
        with st.form("register_form", clear_on_submit=False):
            col_a, col_b = st.columns(2)
            
            with col_a:
                full_name = st.text_input("Full Name", placeholder="John Doe", key="reg_name")
                username = st.text_input("Username", placeholder="johndoe", key="reg_username")
                email = st.text_input("Email", placeholder="john@company.com", key="reg_email")
            
            with col_b:
                company = st.text_input("Company", placeholder="Your Company Inc.", key="reg_company")
                password = st.text_input("Password", type="password", placeholder="••••••••", key="reg_password")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="••••••••", key="reg_confirm")
            
            # Password strength indicator
            if password:
                is_valid, message = validate_password(password)
                if is_valid:
                    st.markdown(f"<div class='password-strength-strong'>✓ {message}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='password-strength-weak'>✗ {message}</div>", unsafe_allow_html=True)
            
            st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
            
            submit = st.form_submit_button("Create Account", use_container_width=True)
            
            if submit:
                if not all([full_name, username, email, company, password, confirm_password]):
                    st.error("⚠️ Please fill in all fields")
                elif len(username) < 3:
                    st.error("❌ Username must be at least 3 characters")
                elif not validate_email(email):
                    st.error("❌ Please enter a valid email address")
                elif password != confirm_password:
                    st.error("❌ Passwords do not match")
                else:
                    is_valid, message = validate_password(password)
                    if not is_valid:
                        st.error(f"❌ {message}")
                    else:
                        with st.spinner("Creating your account..."):
                            success, result = register_user(username, email, password, full_name, company)
                            
                            if success:
                                st.success(f"✅ {result} Redirecting...")
                                st.balloons()
                                import time
                                time.sleep(2)
                                st.session_state.page = "login"
                                st.rerun()
                            else:
                                st.error(f"❌ {result}")
        
        # Divider
        st.markdown("""
            <div style='
                display: flex;
                align-items: center;
                margin: 32px 0;
            '>
                <div style='flex: 1; height: 1px; background: #e2e8f0;'></div>
                <span style='padding: 0 16px; color: #64748b; font-size: 14px;'>or</span>
                <div style='flex: 1; height: 1px; background: #e2e8f0;'></div>
            </div>
        """, unsafe_allow_html=True)
        
        # Login button
        st.markdown("""
            <p style='text-align: center; color: #64748b; font-size: 14px; margin-bottom: 12px;'>
                Already have an account?
            </p>
        """, unsafe_allow_html=True)
        
        if st.button("Sign In", use_container_width=True, key="goto_login"):
            st.session_state.page = "login"
            st.rerun()
    
    # Footer
    st.markdown("""
        <div style='text-align: center; margin-top: 3rem;'>
            <p style='color: #cbd5e1; font-size: 0.875rem;'>
                © 2025 Refund Prediction System. All rights reserved.
            </p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_register()