import streamlit as st
from auth import login_user

def show_login():
    """Display login page with modern design"""
    
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
            padding-top: 3rem;
            padding-bottom: 3rem;
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
            color: #0f172a !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            margin-bottom: 8px !important;
        }
        
        /* Checkbox */
        .stCheckbox {
            color: #1e293b !important;
        }
        
        .stCheckbox label {
            color: #1e293b !important;
            font-size: 14px !important;
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
        
        .stButton button:active {
            transform: translateY(0px) !important;
        }
        
        /* Form container */
        [data-testid="stForm"] {
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
        }
        
        /* Alert messages */
        .stAlert {
            border-radius: 12px !important;
            border: none !important;
            padding: 16px !important;
        }
        
        /* Success message */
        [data-baseweb="notification"] {
            background-color: #f0fdf4 !important;
            border-left: 4px solid #22c55e !important;
        }
        
        /* Error message */
        .stAlert[data-baseweb="notification"][kind="error"] {
            background-color: #fef2f2 !important;
            border-left: 4px solid #ef4444 !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header section
    st.markdown("""
        <div style='text-align: center; margin-bottom: 3rem;'>
            <h1 style='color: #ffffff; font-size: 3rem; font-weight: 800; margin-bottom: 0.5rem; text-shadow: 0 2px 10px rgba(0,0,0,0.3);'>
                📦 Refund Prediction System
            </h1>
            <p style='color: #cbd5e1; font-size: 1.25rem; font-weight: 400;'>
                AI-Powered Refund Likelihood Analysis
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Create centered columns
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Login card
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
                        <span style='font-size: 40px;'>🔐</span>
                    </div>
                    <h2 style='color: #1e293b; font-size: 1.875rem; font-weight: 700; margin: 0 0 8px 0;'>
                        Welcome Back
                    </h2>
                    <p style='color: #64748b; font-size: 1rem; margin: 0;'>
                        Sign in to access your dashboard
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        # Login form
        with st.form("login_form", clear_on_submit=False):
            st.text_input(
                "Username",
                placeholder="Enter your username",
                key="login_username",
                label_visibility="visible"
            )
            
            st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="login_password",
                label_visibility="visible"
            )
            
            st.checkbox("Remember me for 30 days", key="remember")
            
            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            
            submit = st.form_submit_button("Sign In", use_container_width=True)
            
            if submit:
                username = st.session_state.login_username
                password = st.session_state.login_password
                
                if not username or not password:
                    st.error("⚠️ Please fill in all fields")
                else:
                    with st.spinner("Authenticating..."):
                        success, result = login_user(username, password)
                        
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.user = result
                            st.session_state.page = "app"
                            st.success("✅ Login successful! Redirecting...")
                            st.balloons()
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
        
        # Register button
        st.markdown("""
            <p style='text-align: center; color: #64748b; font-size: 14px; margin-bottom: 12px;'>
                Don't have an account?
            </p>
        """, unsafe_allow_html=True)
        
        if st.button("Create New Account", use_container_width=True, key="goto_register"):
            st.session_state.page = "register"
            st.rerun()
    
    # Footer
    st.markdown("""
        <div style='text-align: center; margin-top: 4rem;'>
            <p style='color: #cbd5e1; font-size: 0.875rem;'>
                © 2024 Refund Prediction System. All rights reserved.
            </p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_login()