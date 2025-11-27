# ==========================================
# TRANSLATION DATABASE (22 Scheduled Languages)
# ==========================================

LANGUAGES = {
    'English': 'en', 'Hindi': 'hi', 'Assamese': 'as', 'Bengali': 'bn', 
    'Bodo': 'brx', 'Dogri': 'doi', 'Gujarati': 'gu', 'Kannada': 'kn', 
    'Kashmiri': 'ks', 'Konkani': 'kok', 'Maithili': 'mai', 'Malayalam': 'ml', 
    'Manipuri': 'mni', 'Marathi': 'mr', 'Nepali': 'ne', 'Odia': 'or', 
    'Punjabi': 'pa', 'Sanskrit': 'sa', 'Santali': 'sat', 'Sindhi': 'sd', 
    'Tamil': 'ta', 'Telugu': 'te', 'Urdu': 'ur'
}

TRANS_DB = {
    'en': {
        'title': "FarmFin Assist",
        'subtitle': "Your Companion for Agri-Credit & Financial Growth",
        'nav_home': "🏠 Home",
        'nav_profile': "👤 Farmer Profile",
        'nav_health': "💰 Financial Health",
        'nav_schemes': "📜 Loans & Subsidies",
        'nav_calc': "🧮 Profit Calculator",
        'nav_learn': "🎓 Learning Zone",
        'nav_report': "📄 Download Report",
        'welcome': "Welcome, Farmer!",
        'intro': "Empowering farmers with financial literacy and credit readiness.",
        'enter_details': "Please enter your details",
        'name': "Full Name",
        'land_size': "Land Size (Acres)",
        'crop_type': "Primary Crop",
        'district': "District",
        'save_btn': "Save Profile",
        'reset_btn': "🔴 Reset Data",
        'income_annual': "Annual Income (₹)",
        'expenses_annual': "Annual Expenses (₹)",
        'loan_emi': "Monthly EMI (₹)",
        'calc_health': "Analyze Health",
        'dscr_score': "DSCR Score",
        'credit_score': "Credit Score",
        'download_pdf': "Download PDF Report",
        'risk_safe': "SAFE / ELIGIBLE",
        'risk_high': "HIGH RISK",
        'metric_interest': "Interest Rate",
        'metric_season': "Next Crop Season"
    },
    'hi': {
        'title': "फार्म-फिन असिस्ट",
        'subtitle': "कृषि-क्रेडिट और वित्तीय विकास के लिए आपका साथी",
        'nav_home': "🏠 होम",
        'nav_profile': "👤 किसान प्रोफाइल",
        'nav_health': "💰 वित्तीय स्वास्थ्य",
        'nav_schemes': "📜 ऋण और सब्सिडी",
        'nav_calc': "🧮 लाभ कैलकुलेटर",
        'nav_learn': "🎓 शिक्षण क्षेत्र",
        'nav_report': "📄 रिपोर्ट डाउनलोड करें",
        'welcome': "स्वागत है, किसान भाई!",
        'intro': "किसानों को वित्तीय साक्षरता और ऋण तैयारी के साथ सशक्त बनाना।",
        'enter_details': "कृपया अपना विवरण दर्ज करें",
        'name': "पूरा नाम",
        'land_size': "भूमि का आकार (एकड़)",
        'crop_type': "मुख्य फसल",
        'district': "ज़िला",
        'save_btn': "प्रोफाइल सहेजें",
        'reset_btn': "🔴 डेटा रीसेट करें",
        'income_annual': "वार्षिक आय (₹)",
        'expenses_annual': "वार्षिक व्यय (₹)",
        'loan_emi': "मासिक ईएमआई (₹)",
        'calc_health': "स्वास्थ्य विश्लेषण",
        'dscr_score': "डीएससीआर स्कोर",
        'credit_score': "क्रेडिट स्कोर",
        'download_pdf': "पीडीएफ डाउनलोड करें",
        'risk_safe': "सुरक्षित / योग्य",
        'risk_high': "उच्च जोखिम",
        'metric_interest': "ब्याज दर",
        'metric_season': "अगली फसल का मौसम"
    }
}

def get_text(lang_code, key):
    return TRANS_DB.get(lang_code, {}).get(key, TRANS_DB['en'].get(key, key))