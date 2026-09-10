import streamlit as st
from google import genai
from PIL import Image

# Page Configuration
st.set_page_config(
    page_title="SmartChef AI | Leftover Recipe Engine",
    page_icon="🥗",
    layout="wide"
)

# Sidebar: Secure API Key Entry
st.sidebar.title("🔐 Configuration")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if not api_key:
    st.info("👈 Please enter your Google Gemini API key in the sidebar to start!")
    st.stop()

# Initialize Gemini Client
client = genai.Client(api_key=api_key)

# Header Section
st.title("🥗 SmartChef AI: Leftover Recipe Engine")
st.caption("Addressing SDG 3 (Good Health) & SDG 12 (Responsible Consumption)")

# Impact Counter Metric
col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric("Community Target", "SDG 3 & 12")
col_m2.metric("Avg Food Saved / Meal", "~400 grams")
col_m3.metric("Est. CO₂ Saved", "~1.2 kg per recipe")

st.divider()

# User Inputs Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📸 Step 1: Provide Leftover Ingredients")
    input_method = st.radio("Choose Input Method:", ["Type Text Ingredients", "Upload Fridge Photo"])
    
    ingredients_text = ""
    uploaded_image = None
    
    if input_method == "Type Text Ingredients":
        ingredients_text = st.text_area(
            "List your leftovers (e.g., half a bowl of rice, wilted spinach, cooked chicken breast):",
            placeholder="Type items here..."
        )
    else:
        uploaded_file = st.file_uploader("Upload a photo of your fridge or pantry shelf:", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            uploaded_image = Image.open(uploaded_file)
            st.image(uploaded_image, caption="Uploaded Fridge Image", use_column_width=True)

    st.subheader("⏳ Pantry Expiry Radar")
    expiring_items = st.text_input("Which items are expiring TODAY or TOMORROW? (Optional)", 
                                   placeholder="e.g., spinach, open yogurt")

with col2:
    st.subheader("🎯 Step 2: Health & Household Profile")
    
    health_profile = st.selectbox(
        "Select Health Target / Dietary Mode:",
        [
            "Standard Healthy Household Mode",
            "🩸 Diabetic & Blood-Sugar Friendly (Low GI / High Fiber)",
            "💪 High-Protein & Fitness Focused",
            "🥗 100% Vegetarian / Plant-Based",
            "🥜 Allergen-Safe (Nut-Free / Gluten-Free)"
        ]
    )
    
    family_size = st.slider("Portion Size (Servings):", min_value=1, max_value=6, value=2)

st.divider()

# Generate Button Logic
if st.button("🚀 Generate Healthy Recipe & Health Score", type="primary"):
    with st.spinner("SmartChef AI is analyzing ingredients and computing health metrics..."):
        
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
                    model='gemini-2.5-flash',
                    contents=[uploaded_image, system_instruction + "\nFirst, identify the leftover ingredients in the photo, then build the recipe."]
                )
            else:
                prompt = f"{system_instruction}\nLeftover Ingredients Provided: {ingredients_text}"
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
            
            st.success("Recipe Created Successfully!")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"Error connecting to AI backend: {str(e)}")
