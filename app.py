import streamlit as st
from google import genai
from PIL import Image

# Page Configuration
st.set_page_config(
    page_title="SmartChef AI | Zero Waste & Health Engine",
    page_icon="🥗",
    layout="wide"
)

# Custom Styling Injection (CSS)
st.markdown("""
    <style>
    /* Main Background & Gradient Header */
    .main {
        background-color: #f8f9fa;
    }
    .header-box {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 24px;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .header-box h1 {
        color: white !important;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .header-box p {
        font-size: 1.1rem;
        opacity: 0.95;
    }
    
    /* Styled Metric Cards */
    .metric-card {
        background: white;
        padding: 18px;
        border-radius: 12px;
        text-align: center;
        border-left: 5px solid #11998e;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .metric-card h3 {
        margin: 0;
        color: #2c3e50;
        font-size: 1.5rem;
    }
    .metric-card p {
        margin: 0;
        color: #7f8c8d;
        font-size: 0.9rem;
    }

    /* Container Cards */
    div[data-testid="stVerticalBlock"] > div.element-container {
        border-radius: 10px;
    }
    
    /* Custom Button */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
        color: white;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 12px;
        padding: 12px 24px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(56, 239, 125, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# Securely retrieve API Key from Streamlit Secrets or Sidebar fallback
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if not api_key:
    st.error("🔑 API Key missing! Please configure Streamlit Secrets.")
    st.stop()

# Initialize Gemini Client
client = genai.Client(api_key=api_key)

# Header Section with Stylish Banner
st.markdown("""
    <div class="header-box">
        <h1>🥗 SmartChef AI</h1>
        <p>Transforming Leftovers into Healthy Meals | Supporting SDG 3 & SDG 12</p>
    </div>
""", unsafe_allow_html=True)

# Impact Counter Metrics (Styled Cards)
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown("""<div class="metric-card"><h3>SDG 3 & 12</h3><p>Community Goals</p></div>""", unsafe_allow_html=True)
with m2:
    st.markdown("""<div class="metric-card"><h3>~400g Saved</h3><p>Avg Food Saved / Meal</p></div>""", unsafe_allow_html=True)
with m3:
    st.markdown("""<div class="metric-card"><h3>~1.2 kg CO₂</h3><p>Prevented Footprint</p></div>""", unsafe_allow_html=True)

st.write("")
st.write("")

# User Inputs Layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📸 1. Input Ingredients")
    input_method = st.radio("Choose Input Method:", ["Type Text Ingredients", "Upload Fridge Photo"], horizontal=True)
    
    ingredients_text = ""
    uploaded_image = None
    
    if input_method == "Type Text Ingredients":
        ingredients_text = st.text_area(
            "List your leftovers:",
            placeholder="e.g., half a bowl of cooked rice, wilted spinach, chicken breast...",
            height=120
        )
    else:
        uploaded_file = st.file_uploader("Upload a clear photo of your fridge or pantry shelf:", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            uploaded_image = Image.open(uploaded_file)
            st.image(uploaded_image, caption="Uploaded Fridge View", use_container_width=True)

    st.markdown("### ⏳ Pantry Expiry Radar")
    expiring_items = st.text_input("Items expiring TODAY or TOMORROW:", placeholder="e.g., open yogurt, fresh spinach")

with col2:
    st.markdown("### 🎯 2. Dietary & Health Target")
    
    health_profile = st.selectbox(
        "Select Health Target Mode:",
        [
            "Standard Healthy Household Mode",
            "🩸 Diabetic & Blood-Sugar Friendly (Low GI / High Fiber)",
            "💪 High-Protein & Fitness Focused",
            "🥗 100% Vegetarian / Plant-Based",
            "🥜 Allergen-Safe (Nut-Free / Gluten-Free)"
        ]
    )
    
    family_size = st.slider("Portion Size (Servings):", min_value=1, max_value=6, value=2)
    
    st.info("💡 **Smart Features Active:** Custom prompt formatting, low-GI recipe prioritization, and real-time carbon reduction estimates.")

st.divider()

# Generate Button Logic
if st.button("✨ Cook Smart with AI", type="primary"):
    with st.spinner(" SmartChef AI is scanning items and crafting a custom recipe..."):
        
        system_instruction = f"""
        You are an elite nutritionist and zero-waste chef expert.
        Generate a delicious, healthy, low-waste recipe based on leftover ingredients.
        
        User Rules:
        - Health Profile: {health_profile}
        - Servings Required: {family_size}
        - Expiring Priority Ingredients: {expiring_items}
        
        If Diabetic/Blood-Sugar Friendly mode is selected:
        1. Prioritize low glycemic index (GI) foods.
        2. Combine high-fiber or protein options to prevent glucose spikes.
        3. Cap simple carbohydrates and explain sugar/carb safety.
        
        Structured Output Format Required:
        ---
        ## 🍲 Recipe Title
        **Preparation Time:** [X] Mins | **Difficulty:** [Easy/Medium]
        
        ### 🛒 Ingredients Required (Using Leftovers First)
        - [List items]
        
        ### 🍳 Step-by-Step Instructions
        1. [Step 1]
        2. [Step 2]
        
        ### 🩸 Blood Sugar & Health Breakdown
        - **Carb & Glycemic Impact:** [Explain glycemic safety]
        - **Nutritional Grade:** [e.g., A+]
        - **Key Macro Breakdown:** [Calories, Protein, Carbs, Fiber per serving]
        
        ### 🌿 Zero-Waste Impact Metrics
        - **Food Waste Prevented:** ~[X] grams
        - **Estimated CO₂ Footprint Saved:** ~[X] kg
        ---
        """
        
        try:
            if input_method == "Upload Fridge Photo" and uploaded_image:
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=[uploaded_image, system_instruction + "\nFirst, identify the leftover ingredients in the photo, then build the recipe."]
                )
            else:
                prompt = f"{system_instruction}\nLeftover Ingredients Provided: {ingredients_text}"
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=prompt
                )
            
            st.success("Recipe Created Successfully!")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"Error connecting to AI backend: {str(e)}")
     
