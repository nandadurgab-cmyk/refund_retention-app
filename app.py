import streamlit as st
import pandas as pd
import joblib

# Import authentication
from login import show_login
from register import show_register
from auth import update_prediction_count, log_prediction, get_user_info

# Configure page
st.set_page_config(
    page_title="Refund Prediction System",
    page_icon="📦",
    layout="wide"
)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'user' not in st.session_state:
    st.session_state.user = None

# Page routing - Show login/register if not logged in
if not st.session_state.logged_in:
    if st.session_state.page == 'register':
        show_register()
    else:
        show_login()
    st.stop()

# Load trained model
try:
    model = joblib.load("refund_model.pkl")
except:
    st.error("⚠️ Error: Model file 'refund_model.pkl' not found!")
    st.stop()

# Custom CSS for main app - WHITE BACKGROUND, BLACK TEXT
st.markdown("""
    <style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Force white background everywhere */
    .stApp {
        background-color: #ffffff !important;
    }
    
    .main {
        background-color: #ffffff !important;
    }
    
    .block-container {
        background-color: #ffffff !important;
        padding-top: 2rem;
        max-width: 1400px;
    }
    
    /* Force all text to black */
    .stApp, .main, div, p, span, label, .stMarkdown {
        color: #000000 !important;
    }
    
    /* Headers - Black */
    h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
    }
    
    /* Subheader */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #000000 !important;
    }
    
    /* Text inputs */
    .stTextInput input {
        background-color: #f8f9fa !important;
        color: #000000 !important;
        border: 2px solid #dee2e6 !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        font-size: 15px !important;
    }
    
    .stTextInput input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        outline: none !important;
    }
    
    .stTextInput input::placeholder {
        color: #6c757d !important;
    }
    
    /* Number inputs */
    .stNumberInput input {
        background-color: #f8f9fa !important;
        color: #000000 !important;
        border: 2px solid #dee2e6 !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        font-size: 15px !important;
    }
    
    .stNumberInput input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        outline: none !important;
    }
    
    /* Selectbox */
    .stSelectbox {
        color: #000000 !important;
    }
    
    .stSelectbox label {
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    .stSelectbox [data-baseweb="select"] {
        background-color: #f8f9fa !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        background-color: #f8f9fa !important;
        border: 2px solid #dee2e6 !important;
        border-radius: 8px !important;
        color: #000000 !important;
    }
    
    .stSelectbox [data-baseweb="select"]:focus-within > div {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    /* Selectbox dropdown menu */
    [data-baseweb="menu"] {
        background-color: #ffffff !important;
    }
    
    [data-baseweb="menu"] li {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    [data-baseweb="menu"] li:hover {
        background-color: #f8f9fa !important;
    }
    
    /* Labels */
    .stTextInput label,
    .stNumberInput label,
    .stSelectbox label {
        color: #fff !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    
    /* Buttons */
    .stButton button {
        background: #3b82f6 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        background: #2563eb !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #3b82f6 !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #000000 !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stMetricDelta"] {
        color: #000000 !important;
    }
    
    /* Alert boxes */
    .stSuccess {
        background-color: #d4edda !important;
        color: #155724 !important;
        border: 1px solid #c3e6cb !important;
        border-radius: 8px !important;
        padding: 16px !important;
    }
    
    .stSuccess p, .stSuccess div, .stSuccess span {
        color: #155724 !important;
    }
    
    .stError {
        background-color: #f8d7da !important;
        color: #721c24 !important;
        border: 1px solid #f5c6cb !important;
        border-radius: 8px !important;
        padding: 16px !important;
    }
    
    .stError p, .stError div, .stError span {
        color: #721c24 !important;
    }
    
    .stWarning {
        background-color: #fff3cd !important;
        color: #856404 !important;
        border: 1px solid #ffeeba !important;
        border-radius: 8px !important;
        padding: 16px !important;
    }
    
    .stWarning p, .stWarning div, .stWarning span {
        color: #856404 !important;
    }
    
    .stInfo {
        background-color: #d1ecf1 !important;
        color: #0c5460 !important;
        border: 1px solid #bee5eb !important;
        border-radius: 8px !important;
        padding: 16px !important;
    }
    
    .stInfo p, .stInfo div, .stInfo span {
        color: #0c5460 !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #3b82f6 !important;
    }
    
    /* Divider */
    hr {
        border: none;
        border-top: 1px solid #dee2e6 !important;
        margin: 2rem 0 !important;
    }
    
    /* Markdown content */
    .stMarkdown {
        color: #000000 !important;
    }
    
    /* Force markdown text color */
    .stMarkdown p, .stMarkdown li, .stMarkdown span, .stMarkdown strong {
        color: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Get updated user info
user_info = get_user_info(st.session_state.user['username'])
if user_info:
    st.session_state.user = user_info

# Header with logout
col_head1, col_head2 = st.columns([4, 1])

with col_head1:
    st.title("📦 Refund Prediction Dashboard")
    st.markdown("**AI-Powered E-commerce Return Analytics**")

with col_head2:
    st.write("")  # Spacing
    if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.page = 'login'
        st.rerun()

st.markdown("---")

# User info card with inline styles
st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        border-radius: 12px;
        padding: 24px 32px;
        margin-bottom: 32px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    '>
        <h3 style='color: #ffffff !important; font-size: 1.5rem; font-weight: 700; margin: 0 0 8px 0;'>
            Welcome, {st.session_state.user['full_name']}! 👋
        </h3>
        <p style='color: #ffffff !important; margin: 0; font-size: 0.95rem;'>
            <strong style='color: #ffffff !important;'>{st.session_state.user['company']}</strong> • 
            {st.session_state.user['role']} • 
            @{st.session_state.user['username']}
        </p>
    </div>
""", unsafe_allow_html=True)

# Statistics cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div style='
            background: #f8f9fa;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            border: 2px solid #dee2e6;
            text-align: center;
        '>
            <p style='color: #6c757d !important; font-size: 0.9rem; font-weight: 600; margin: 0 0 8px 0; text-transform: uppercase;'>
                Total Predictions
            </p>
            <p style='color: #3b82f6 !important; font-size: 2.5rem; font-weight: 800; margin: 0;'>
                {st.session_state.user['predictions_count']}
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style='
            background: #f8f9fa;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            border: 2px solid #dee2e6;
            text-align: center;
        '>
            <p style='color: #6c757d !important; font-size: 0.9rem; font-weight: 600; margin: 0 0 8px 0; text-transform: uppercase;'>
                Session Status
            </p>
            <p style='color: #28a745 !important; font-size: 2.5rem; font-weight: 800; margin: 0;'>
                Active
            </p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div style='
            background: #f8f9fa;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            border: 2px solid #dee2e6;
            text-align: center;
        '>
            <p style='color: #6c757d !important; font-size: 0.9rem; font-weight: 600; margin: 0 0 8px 0; text-transform: uppercase;'>
                ML Model
            </p>
            <p style='color: #3b82f6 !important; font-size: 2.5rem; font-weight: 800; margin: 0;'>
                Ready
            </p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Prediction form section
st.subheader("📊 Order Analysis")
st.write("Enter the order details below to predict refund likelihood")

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    product_category = st.selectbox("📦 Product Category", ["Clothing", "Books", "Electronics", "Home", "Toys"])
    product_price = st.number_input("💰 Product Price (₹)", min_value=1.0, value=50.0, step=1.0)
    order_quantity = st.number_input("🔢 Order Quantity", min_value=1, step=1, value=1)
    days_to_return = st.number_input("📅 Days to Return", min_value=0, value=30, step=1)

with col2:
    user_age = st.number_input("🎂 Customer Age", min_value=18, max_value=100, value=30, step=1)
    user_gender = st.selectbox("👤 Gender", ["Male", "Female"])
    user_location = "City1"
    payment_method = st.selectbox("💳 Payment Method", ["Credit Card", "Debit Card", "PayPal", "Gift Card"])

with col3:
    shipping_method = st.selectbox("🚚 Shipping Method", ["Standard", "Express", "Next-Day"])
    discount_applied = st.number_input("🏷️ Discount Applied (₹)", min_value=0.0, value=0.0, step=1.0)

st.markdown("<br>", unsafe_allow_html=True)

# Predict button
if st.button("🔮 Predict Refund Likelihood", use_container_width=True, key="predict_btn"):
    with st.spinner("Analyzing order data..."):
        input_data = pd.DataFrame([{
            "Product_Category": product_category,
            "Product_Price": product_price,
            "Order_Quantity": order_quantity,
            "Days_to_Return": days_to_return,
            "User_Age": user_age,
            "User_Gender": user_gender,
            "User_Location": user_location,
            "Payment_Method": payment_method,
            "Shipping_Method": shipping_method,
            "Discount_Applied": discount_applied
        }])
        
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]
        
        # Update stats
        new_count = update_prediction_count(st.session_state.user['username'])
        if new_count:
            st.session_state.user['predictions_count'] = new_count
        
        # Log prediction
        result_text = "Likely Returned" if prediction == 1 else "Not Returned"
        log_prediction(st.session_state.user['username'], product_category, product_price, result_text, probability)
        
        st.markdown("---")
        
        # Results section
        st.subheader("📊 Prediction Results")
        
        if prediction == 1:
            st.error("### 🔁 High Return Risk Detected")
            
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                st.metric("Return Probability", f"{probability:.1%}")
            with col_r2:
                st.metric("Risk Level", "HIGH", delta="⚠️ Warning")
            
            st.warning(f"""
**Risk Analysis:**

- Return probability: **{probability:.2%}**
- Recommendation: Consider quality checks or customer engagement
- Action: Monitor this order closely
            """)
        else:
            st.success("### ✅ Low Return Risk")
            
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                st.metric("Success Probability", f"{(1-probability):.1%}")
            with col_r2:
                st.metric("Risk Level", "LOW", delta="✓ Safe")
            
            st.info(f"""
**Positive Indicators:**

- Return probability: **{probability:.2%}**
- Confidence: **{(1-probability):.2%}**
- Status: Order likely to complete successfully
            """)
        
        st.markdown("---")
        
        # Order summary
        st.subheader("📋 Order Summary")
        
        col_s1, col_s2 = st.columns(2)
        
        with col_s1:
            st.markdown(f"""
**Order Details:**

- **Category:** {product_category}
- **Price:** ₹{product_price:.2f}
- **Quantity:** {order_quantity}
- **Return Window:** {days_to_return} days
- **Shipping:** {shipping_method}
- **Discount:** ₹{discount_applied:.2f}
            """)
        
        with col_s2:
            st.markdown(f"""
**Customer Profile:**

- **Age:** {user_age} years
- **Gender:** {user_gender}
- **Payment Method:** {payment_method}
            """)
        
        st.balloons()

# Footer
st.markdown("---")
st.markdown(f"""
    <div style='
        text-align: center; 
        padding: 20px; 
        background: #f8f9fa; 
        border-radius: 8px; 
        border: 1px solid #dee2e6;
        margin-top: 40px;
    '>
        <p style='color: #000000 !important; font-size: 0.9rem; margin: 0;'>
            © 2024 Refund Prediction System • Powered by Machine Learning
        </p>
        <p style='color: #6c757d !important; font-size: 0.85rem; margin: 8px 0 0 0;'>
            User: <strong style='color: #000000 !important;'>{st.session_state.user['username']}</strong> • 
            Total Predictions: <strong style='color: #000000 !important;'>{st.session_state.user['predictions_count']}</strong>
        </p>
    </div>
""", unsafe_allow_html=True)