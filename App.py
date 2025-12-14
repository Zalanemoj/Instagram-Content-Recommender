import streamlit as st
import pandas as pd
import pickle
import os
import google.generativeai as genai

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Instagram Strategy Dashboard", page_icon="📈", layout="wide")

st.title("📈 Instagram Engagement & Strategy Dashboard")
st.markdown("Predict engagement rates and get AI-powered improvement strategies.")

# --- 2. LOAD RESOURCES ---
@st.cache_resource
def load_resources():
    # Path to your model based on your structure
    model_path = 'Models/XGB-Model.pkl' 
    
    # Fallback paths just in case
    if not os.path.exists(model_path):
        model_path = 'models/XGB-Model.pkl' # Try lowercase
    
    try:
        if os.path.exists(model_path):
            with open(model_path, 'rb') as file:
                model = pickle.load(file)
            return model
        else:
            return None
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

xgb_model = load_resources()

if xgb_model is None:
    st.error("❌ Model not found! Please check that 'XGB-Model.pkl' is inside the 'Models' folder.")
    st.stop()

# --- 3. SIDEBAR: INPUTS ---
st.sidebar.header("🔑 AI Strategy Setup")
api_key = st.sidebar.text_input("Gemini API Key (Optional)", type="password", help="For AI advice")

st.sidebar.divider()
st.sidebar.header("📝 Post Details")

# Categorical Inputs
media_type = st.sidebar.selectbox("Media Type", ['Reel', 'Carousel', 'Photo', 'Video'])
traffic_source = st.sidebar.selectbox("Traffic Source", ['Reels Feed', 'Explore', 'Home Feed', 'Hashtags', 'Profile', 'External'])
content_category = st.sidebar.selectbox("Category", ['Fashion', 'Lifestyle', 'Fitness', 'Food', 'Travel', 'Technology', 'Beauty', 'Comedy', 'Music', 'Photography'])

# Numerical Inputs
col1, col2 = st.sidebar.columns(2)
with col1:
    likes = st.number_input("Est. Likes", value=1000)
    comments = st.number_input("Est. Comments", value=50)
    shares = st.number_input("Est. Shares", value=20)
    saves = st.number_input("Est. Saves", value=30)
with col2:
    reach = st.number_input("Est. Reach", value=5000)
    impressions = st.number_input("Est. Impressions", value=6000)
    followers_gained = st.number_input("New Followers", value=5)

caption_length = st.sidebar.slider("Caption Length (chars)", 0, 2200, 150)
hashtags_count = st.sidebar.slider("Hashtags Count", 0, 30, 10)

# --- 4. PREDICTION LOGIC (One-Hot Encoding) ---
def make_prediction():
    # 1. Define exact columns from your X_train
    expected_cols = [
        'likes', 'comments', 'shares', 'saves', 'reach', 'impressions', 
        'caption_length', 'hashtags_count', 'followers_gained',
        
        # Media Types
        'media_type_Carousel', 'media_type_Photo', 'media_type_Reel', 'media_type_Video',
        
        # Traffic Sources
        'traffic_source_Explore', 'traffic_source_External', 'traffic_source_Hashtags', 
        'traffic_source_Home Feed', 'traffic_source_Profile', 'traffic_source_Reels Feed',
        
        # Content Categories
        'content_category_Beauty', 'content_category_Comedy', 'content_category_Fashion', 
        'content_category_Fitness', 'content_category_Food', 'content_category_Lifestyle', 
        'content_category_Music', 'content_category_Photography', 'content_category_Technology', 
        'content_category_Travel'
    ]
    
    # 2. Initialize with 0
    data = {col: 0 for col in expected_cols}
    
    # 3. Fill Numerical Data
    data['likes'] = likes
    data['comments'] = comments
    data['shares'] = shares
    data['saves'] = saves
    data['reach'] = reach
    data['impressions'] = impressions
    data['caption_length'] = caption_length
    data['hashtags_count'] = hashtags_count
    data['followers_gained'] = followers_gained
    
    # 4. Fill Categorical Data (Set specific column to 1)
    if f'media_type_{media_type}' in data: data[f'media_type_{media_type}'] = 1
    if f'traffic_source_{traffic_source}' in data: data[f'traffic_source_{traffic_source}'] = 1
    if f'content_category_{content_category}' in data: data[f'content_category_{content_category}'] = 1
    
    return pd.DataFrame([data])

# --- 5. MAIN DASHBOARD ---
# Layout
left_col, right_col = st.columns([1, 1.5])

with left_col:
    st.subheader("📊 Performance Prediction")
    
    if st.button("🚀 Analyze Post", type="primary"):
        # Predict
        input_df = make_prediction()
        try:
            prediction = xgb_model.predict(input_df)[0]
            
            # Show Result
            st.metric(label="Predicted Engagement Rate", value=f"{prediction:.2%}")
            st.progress(min(prediction * 5, 1.0)) # Visual bar
            
            # Save for AI
            st.session_state['pred_value'] = prediction
            st.session_state['run_ai'] = True
            
        except Exception as e:
            st.error(f"Prediction Error: {e}")

with right_col:
    st.subheader("🤖 AI Strategist")
    
    if 'run_ai' in st.session_state and st.session_state['run_ai']:
        pred_val = st.session_state['pred_value']
        
        if api_key:
            try:
                genai.configure(api_key=api_key)
                gemini = genai.GenerativeModel('gemini-2.5-flash')
                
                prompt = f"""
                Act as a social media expert. I have a planned Instagram post:
                - Category: {content_category}
                - Format: {media_type}
                - Predicted Engagement: {pred_val:.2%}
                
                Provide 3 brief, bullet-point strategic tips to increase this specific engagement score. 
                Focus on: Best time to post for {content_category}, caption hooks, and hashtag strategy.
                """
                
                with st.spinner("Generating strategy..."):
                    response = gemini.generate_content(prompt)
                    st.success("Strategy Report:")
                    st.markdown(response.text)
            except Exception as e:
                st.error(f"Gemini API Error: {e}")
        else:
            st.info("💡 Enter a Gemini API Key in the sidebar to get specific advice on how to improve this score.")
    else:
        st.write("👈 Click **Analyze Post** to see predictions and insights.")
