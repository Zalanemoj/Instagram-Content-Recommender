import streamlit as st
import pandas as pd
import pickle
import os
import google.generativeai as genai

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Instagram AI Strategist", page_icon="🚀", layout="wide")

st.title("🚀 Instagram Engagement Predictor & AI Strategist")
st.markdown("""
This tool uses your **XGBoost Model** to predict engagement numbers, 
and **Google Gemini** to interpret them into a strategy.
""")

# --- 2. LOAD XGBOOST MODEL ---
@st.cache_resource
def load_model():
    # Paths to check (covers local, sagemaker, and nested folders)
    paths = ['Models/XGB-Model.pkl', 'models/XGB-Model.pkl', 'XGB-Model.pkl', 'XGB-Best-Model.pkl']
    
    for path in paths:
        if os.path.exists(path):
            try:
                with open(path, 'rb') as f:
                    model = pickle.load(f)
                return model, path
            except:
                continue
    return None, None

xgb_model, model_path = load_model()

# Status Indicator
if xgb_model:
    st.success(f"✅ XGBoost Model Loaded from: `{model_path}`")
else:
    st.error("❌ Model not found! Please ensure 'XGB-Model.pkl' is in your folder.")
    st.stop()

# --- 3. SIDEBAR: INPUTS ---
st.sidebar.header("🔑 1. AI Setup")
api_key = st.sidebar.text_input("Gemini API Key", type="password", help="Required for the Strategy Report")

st.sidebar.divider()
st.sidebar.header("📝 2. Post Details")

# Categorical Inputs
media_type = st.sidebar.selectbox("Media Type", ['Reel', 'Carousel', 'Photo', 'Video'])
traffic_source = st.sidebar.selectbox("Traffic Source", ['Reels Feed', 'Explore', 'Home Feed', 'Hashtags', 'Profile', 'External'])
content_category = st.sidebar.selectbox("Category", ['Fashion', 'Lifestyle', 'Fitness', 'Food', 'Travel', 'Technology', 'Beauty', 'Comedy', 'Music', 'Photography'])

# Numerical Inputs
st.sidebar.caption("Estimated Metrics (for prediction context)")
col1, col2 = st.sidebar.columns(2)
with col1:
    likes = st.number_input("Likes", value=1000)
    comments = st.number_input("Comments", value=50)
    shares = st.number_input("Shares", value=20)
    saves = st.number_input("Saves", value=30)
with col2:
    reach = st.number_input("Reach", value=5000)
    impressions = st.number_input("Impressions", value=6000)
    followers_gained = st.number_input("New Followers", value=5)

caption_length = st.sidebar.slider("Caption Length", 0, 2200, 150)
hashtags_count = st.sidebar.slider("Hashtags Count", 0, 30, 10)

# --- 4. PREDICTION FUNCTION (One-Hot Encoding) ---
def get_model_input():
    # 1. Define columns EXACTLY as trained
    expected_cols = [
        'likes', 'comments', 'shares', 'saves', 'reach', 'impressions', 
        'caption_length', 'hashtags_count', 'followers_gained',
        # Media
        'media_type_Carousel', 'media_type_Photo', 'media_type_Reel', 'media_type_Video',
        # Traffic
        'traffic_source_Explore', 'traffic_source_External', 'traffic_source_Hashtags', 
        'traffic_source_Home Feed', 'traffic_source_Profile', 'traffic_source_Reels Feed',
        # Category
        'content_category_Beauty', 'content_category_Comedy', 'content_category_Fashion', 
        'content_category_Fitness', 'content_category_Food', 'content_category_Lifestyle', 
        'content_category_Music', 'content_category_Photography', 'content_category_Technology', 
        'content_category_Travel'
    ]
    
    # 2. Zero-initialize
    data = {col: 0 for col in expected_cols}
    
    # 3. Fill Stats
    data['likes'] = likes
    data['comments'] = comments
    data['shares'] = shares
    data['saves'] = saves
    data['reach'] = reach
    data['impressions'] = impressions
    data['caption_length'] = caption_length
    data['hashtags_count'] = hashtags_count
    data['followers_gained'] = followers_gained
    
    # 4. Fill Categories (Set active choice to 1)
    if f'media_type_{media_type}' in data: data[f'media_type_{media_type}'] = 1
    if f'traffic_source_{traffic_source}' in data: data[f'traffic_source_{traffic_source}'] = 1
    if f'content_category_{content_category}' in data: data[f'content_category_{content_category}'] = 1
    
    return pd.DataFrame([data])

# --- 5. GEMINI FUNCTION ---
def get_ai_advice(pred_score, api_key):
    if not api_key:
        return "⚠️ Please enter your Gemini API Key in the sidebar to unlock the strategy report."
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Dynamic Prompt using REAL data from the inputs
        prompt = f"""
        Act as a senior Instagram Analyst.
        I have run a predictive model on a planned post. Here is the data:
        
        - **Category:** {content_category}
        - **Format:** {media_type}
        - **Source:** {traffic_source}
        - **Predicted Engagement Rate:** {pred_score:.2%}
        
        Based ONLY on this data, provide a strategy report:
        1. **Verdict:** Is {pred_score:.2%} a good score for the {content_category} niche? (Be honest).
        2. **Timing:** What is the specific best time to post {content_category} content to maximize this?
        3. **Action Plan:** Give 2 specific ways to increase engagement for a {media_type} beyond {pred_score:.2%}.
        
        Keep it professional, concise, and actionable.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Gemini Error: {str(e)}"

# --- 6. MAIN EXECUTION ---
# Single Button to ensure everything runs together
if st.button("🚀 Generate Prediction & Strategy Report", type="primary"):
    
    # A. Run XGBoost Prediction
    with st.spinner("Running XGBoost Model..."):
        input_df = get_model_input()
        prediction = xgb_model.predict(input_df)[0]
    
    # B. Run Gemini Analysis
    with st.spinner("Consulting AI Strategist..."):
        strategy_report = get_ai_advice(prediction, api_key)

    # --- 7. DISPLAY RESULTS ---
    col_res1, col_res2 = st.columns([1, 1.5])
    
    with col_res1:
        st.subheader("📊 Model Prediction")
        st.metric(label="Predicted Engagement Rate", value=f"{prediction:.2%}")
        st.progress(min(prediction * 5, 1.0))
        
        if prediction > 0.10:
            st.success("🌟 Viral Potential")
        elif prediction > 0.05:
            st.info("✅ Solid Performance")
        else:
            st.warning("⚠️ Needs Optimization")

    with col_res2:
        st.subheader("🧠 AI Strategy Report")
        st.markdown(strategy_report)

else:
    st.info("👈 Enter your details in the sidebar and click the button to start.")
