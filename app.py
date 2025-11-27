import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import datetime
import os
from translations import LANGUAGES, get_text

# ==========================================
# 1. CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="FarmFin Assist | NABARD 2025",
    page_icon="🌾",
    layout="wide"
)

# Custom CSS
# This forces the "primary" button (which we use for RESET) to be RED.
st.markdown("""
    <style>
    .main { background-color: #f0f8f5; }
    
    /* Green buttons for normal actions */
    div.stButton > button:first-child {
        background-color: #2e7d32;
        color: white;
        border-radius: 8px;
        border: none;
    }
    
    /* RED buttons for RESET (We use type='primary' in Streamlit for these) */
    div.stButton > button[kind="primary"] {
        background-color: #d32f2f !important;
        color: white !important;
        border: 1px solid #b71c1c !important;
    }
    
    div.stButton > button:hover {
        opacity: 0.9;
    }
    
    .metric-card {
        background-color: white; padding: 20px; border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1); text-align: center;
    }
    h1, h2, h3 { color: #1b5e20; font-family: 'Sans-serif'; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. SESSION STATE
# ==========================================
# Default values function
def get_defaults():
    return {
        'name': '', 'land': 0.0, 'crop': 'Wheat', 
        'district': '', 'income': 0, 'expenses': 0, 'emi': 0
    }

if 'farmer_data' not in st.session_state:
    st.session_state.farmer_data = get_defaults()

if 'lang_code' not in st.session_state:
    st.session_state.lang_code = 'en'

def t(key):
    return get_text(st.session_state.lang_code, key)

# Helper to calculate Season
def get_current_season():
    month = datetime.datetime.now().month
    # Rabi: Oct(10) to Mar(3)
    if month >= 10 or month <= 3:
        return "Rabi (Wheat/Mustard)"
    # Zaid: Apr(4) to May(5)
    elif 4 <= month <= 5:
        return "Zaid (Vegetables)"
    # Kharif: Jun(6) to Sep(9)
    else:
        return "Kharif (Rice/Maize)"

# ==========================================
# 3. SIDEBAR & NAVIGATION
# ==========================================
def sidebar_menu():
    st.sidebar.title("🌍 Language / भाषा")
    
    lang_names = list(LANGUAGES.keys())
    default_index = lang_names.index('English')
    
    selected_lang_name = st.sidebar.selectbox(
        "Choose Interface Language",
        lang_names,
        index=default_index
    )
    st.session_state.lang_code = LANGUAGES[selected_lang_name]
    
    st.sidebar.markdown("---")
    st.sidebar.title(t('title'))
    
    menu_options = {
        "Home": t('nav_home'),
        "Profile": t('nav_profile'),
        "Health": t('nav_health'),
        "Schemes": t('nav_schemes'),
        "Calculator": t('nav_calc'),
        "Report": t('nav_report')
    }
    
    selection = st.sidebar.radio("Go to:", list(menu_options.keys()), format_func=lambda x: menu_options[x])
    return selection

# ==========================================
# 4. LOGIC
# ==========================================
def calculate_metrics(income, expenses, monthly_emi):
    yearly_emi = monthly_emi * 12
    net_income = income - expenses
    
    dscr = 0
    if yearly_emi > 0:
        dscr = round(net_income / yearly_emi, 2)
    elif net_income > 0:
        dscr = 10.0 
    else:
        dscr = 0.0
        
    score = 600
    if dscr > 1.5: score += 100
    elif dscr < 1.0: score -= 100
    if st.session_state.farmer_data['land'] > 2: score += 50
    
    return dscr, min(900, max(300, score))

# ==========================================
# 5. PAGES
# ==========================================
def page_home():
    # Robust Image Loader (Checks for both file name variations)
    img_files = ["farm_header.jpg", "farm_header.jpg.jpg", "farm_header.jpeg"]
    loaded = False
    for img in img_files:
        if os.path.exists(img):
            st.image(img, use_container_width=True)
            loaded = True
            break
    if not loaded:
        st.warning("⚠️ Header image not found. Please ensure 'farm_header.jpg' is in the folder.")

    st.title(t('title'))
    st.subheader(t('subtitle'))
    st.info(t('intro'))
    
    # Updated Metrics as requested
    col1, col2, col3 = st.columns(3)
    col1.metric("Supported Languages", "22")
    col2.metric(t('metric_interest'), "~7% (KCC)")
    col3.metric(t('metric_season'), get_current_season())

def page_profile():
    st.header(t('nav_profile'))
    with st.form("profile"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input(t('name'), st.session_state.farmer_data['name'])
            land = st.number_input(t('land_size'), min_value=0.0, value=float(st.session_state.farmer_data['land']))
        with c2:
            district = st.text_input(t('district'), st.session_state.farmer_data['district'])
            crop = st.selectbox(t('crop_type'), ["Wheat", "Rice", "Cotton", "Sugarcane", "Maize"])
            
        if st.form_submit_button(t('save_btn')):
            st.session_state.farmer_data.update({'name': name, 'land': land, 'district': district, 'crop': crop})
            st.success("✅ Saved!")

    # Red Reset Button
    st.markdown("---")
    if st.button(t('reset_btn'), type="primary", key="reset_profile"):
        st.session_state.farmer_data = get_defaults()
        st.rerun()

def page_health():
    st.header(t('nav_health'))
    c1, c2 = st.columns(2)
    with c1:
        inc = st.number_input(t('income_annual'), value=st.session_state.farmer_data['income'])
        exp = st.number_input(t('expenses_annual'), value=st.session_state.farmer_data['expenses'])
    with c2:
        emi = st.number_input(t('loan_emi'), value=st.session_state.farmer_data['emi'])
        
    if st.button(t('calc_health')):
        st.session_state.farmer_data.update({'income': inc, 'expenses': exp, 'emi': emi})
        dscr, score = calculate_metrics(inc, exp, emi)
        
        st.divider()
        m1, m2 = st.columns(2)
        m1.metric(t('dscr_score'), dscr, delta="> 1.25 Good")
        m2.metric(t('credit_score'), score)
        
        if dscr < 1.0: st.error(t('risk_high'))
        else: st.success(t('risk_safe'))
            
        fig, ax = plt.subplots()
        ax.bar(['Income', 'Expenses'], [inc, exp], color=['#4CAF50', '#d32f2f'])
        st.pyplot(fig)

    # Red Reset Button
    st.markdown("---")
    if st.button(t('reset_btn'), type="primary", key="reset_health"):
        st.session_state.farmer_data['income'] = 0
        st.session_state.farmer_data['expenses'] = 0
        st.session_state.farmer_data['emi'] = 0
        st.rerun()

def page_schemes():
    st.header(t('nav_schemes'))
    st.markdown("""
    ### 🏦 Government Schemes
    1. **Kisan Credit Card (KCC)**: Get loans at ~7% interest for crops.
    2. **PM Fasal Bima Yojana**: Crop insurance for failure due to weather.
    3. **Palan Yojana**: Subsidies for Dairy/Poultry farming.
    """)

def page_calculator():
    st.header(t('nav_calc'))
    c1, c2 = st.columns(2)
    area = c1.number_input("Area (Acres)", 1.0, key="c_area")
    yield_val = c2.number_input("Yield (Quintals/Acre)", 20.0, key="c_yield")
    price = c1.number_input("Market Price (₹/Quintal)", 2000.0, key="c_price")
    cost = c2.number_input("Cost (₹/Acre)", 15000.0, key="c_cost")
    
    if st.button("Calculate Profit"):
        profit = (area * yield_val * price) - (area * cost)
        st.metric("Estimated Profit", f"₹ {profit:,.2f}")
        if profit > 0: st.success("Profitable")
        else: st.error("Loss Making")
        
    # Red Reset Button
    st.markdown("---")
    if st.button(t('reset_btn'), type="primary", key="reset_calc"):
        st.rerun()

def page_report():
    st.header(t('nav_report'))
    if st.button("Generate PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=16)
        pdf.cell(200, 10, txt="FarmFin Assist Report", ln=1, align='C')
        pdf.line(10, 20, 200, 20)
        pdf.set_font("Arial", size=12)
        pdf.ln(20)
        pdf.cell(200, 10, txt=f"Name: {st.session_state.farmer_data['name']}", ln=1)
        pdf.cell(200, 10, txt=f"District: {st.session_state.farmer_data['district']}", ln=1)
        
        pdf.output("report.pdf")
        with open("report.pdf", "rb") as f:
            st.download_button(t('download_pdf'), f, file_name="Farmer_Report.pdf")

# ==========================================
# 6. ROUTER
# ==========================================
selection = sidebar_menu()

if selection == "Home": page_home()
elif selection == "Profile": page_profile()
elif selection == "Health": page_health()
elif selection == "Schemes": page_schemes()
elif selection == "Calculator": page_calculator()
elif selection == "Report": page_report()