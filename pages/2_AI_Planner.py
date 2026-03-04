import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Planner", page_icon="🥗", layout="wide")

st.markdown("""
<style>
    html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }
    #MainMenu, footer, header { visibility: hidden; }

    .page-header {
        background: linear-gradient(135deg, #1a1a2e, #0f3460);
        border-radius: 16px;
        padding: 36px 32px;
        margin-bottom: 28px;
    }
    .page-header h1 { color: #fff; font-size: 2.2rem; font-weight: 800; margin: 0; }
    .page-header p  { color: #a0aec0; margin: 6px 0 0; font-size: 1rem; }

    .profile-card {
        background: #1a1a2e;
        border: 1px solid #0f3460;
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 24px;
    }
    .profile-card h3 {
        color: #e94560; font-size: 0.95rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: 1px; margin-bottom: 16px;
    }

    div[data-testid="metric-container"] {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 16px;
    }
    div[data-testid="metric-container"] label { color: #a0aec0 !important; font-size: 0.85rem; }
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #ffffff !important; font-size: 1.4rem; font-weight: 700;
    }

    .plan-output {
        background: #1a1a2e;
        border: 1px solid #0f3460;
        border-radius: 16px;
        padding: 32px;
        margin-top: 24px;
        color: #e2e8f0;
        line-height: 1.8;
    }
    .plan-output h2 { color: #e94560; border-bottom: 1px solid #0f3460; padding-bottom: 8px; }
    .plan-output h3 { color: #63b3ed; margin-top: 20px; }
    .plan-output ul li { margin: 6px 0; }

    .stButton > button {
        background: linear-gradient(135deg, #e94560, #c73652) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 14px !important;
        transition: opacity 0.2s !important;
    }
    .stButton > button:hover { opacity: 0.85 !important; }

    div[data-baseweb="radio"] label { color: #cbd5e0 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <h1>🥗 AI Personalised Planner</h1>
    <p>Powered by Google Gemini — generates meal plans and workout routines tailored just for you.</p>
</div>
""", unsafe_allow_html=True)

if "user_data" not in st.session_state:
    st.error("⚠️ No data found. Please complete the **Calculator** page first before generating a plan.")
    if st.button("📊 Go to Calculator"):
        st.switch_page("pages/1_calculator.py")
    st.stop()

data = st.session_state["user_data"]

# Load API key
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("⚠️ Gemini API key not found. Please add `GEMINI_API_KEY` to your Streamlit secrets.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Profile summary
st.markdown('<div class="profile-card"><h3>👤 Your Profile Summary</h3>', unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("🎯 Goal",           data["goal"])
c2.metric("🔥 Daily Calories", f"{data['tdee']} kcal")
c3.metric("📏 BMI",            f"{data['bmi']} — {data['bmi_category']}")
c4.metric("🥩 Protein Target", f"{data['protein_g']}g / day")
c5.metric("⚖️ Body Weight",    f"{data['weight']} kg")
st.markdown('</div>', unsafe_allow_html=True)

# Plan selection
st.subheader("🛠️ Choose Your Plan Type")
plan_type = st.radio(
    "What would you like Gemini to generate?",
    ["🍽️ Meal Plan Only", "🏋️ Workout Plan Only", "📋 Full Plan (Meal + Workout)"],
    horizontal=True
)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("✨ Generate My Personalised Plan", use_container_width=True):

    if "Meal" in plan_type and "Workout" in plan_type:
        content_request = """
        1. Full-day meal plan (Breakfast, Lunch, Dinner, Snacks) with approximate calories per meal
        2. Weekly workout routine (day-by-day, with sets and reps)
        3. Daily protein, carbohydrate and fat targets
        4. Recovery and sleep advice
        5. Daily hydration recommendation
        """
    elif "Meal" in plan_type:
        content_request = """
        1. Full-day meal plan (Breakfast, Lunch, Dinner, Snacks) with approximate calories per meal
        2. Daily protein, carbohydrate and fat targets
        3. Practical meal prep tips
        """
    else:
        content_request = """
        1. Weekly workout routine (day-by-day, with exercises, sets and reps)
        2. Warm-up and cool-down guidance
        3. Recovery and sleep advice
        4. Daily hydration recommendation
        """

    prompt = f"""
    You are an expert personal fitness coach and registered nutritionist.
    Create a detailed, structured and practical fitness plan for the following user.

    User Profile:
    - Gender: {data['gender']}
    - Age: {data['age']} years
    - Weight: {data['weight']} kg
    - Height: {data['height']} cm
    - Activity Level: {data['activity']}
    - Primary Goal: {data['goal']}
    - Daily Calorie Target: {data['tdee']} kcal
    - BMI: {data['bmi']} ({data['bmi_category']})
    - Protein Target: {data['protein_g']}g | Fat Target: {data['fat_g']}g | Carb Target: {data['carb_g']}g

    Please include:
    {content_request}

    Format the response with clear markdown headers (##, ###), bullet points, and bold text where appropriate.
    Be specific, practical and motivating. Avoid generic advice — tailor everything to this user's profile.
    """

    with st.spinner("🤖 Generating your personalised plan — this may take a few seconds..."):
        try:
            response = model.generate_content(prompt)
            st.markdown('<div class="plan-output">', unsafe_allow_html=True)
            st.markdown("## 📋 Your Personalised Plan")
            st.markdown(response.text)
            st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            err = str(e)
            if "429" in err:
                st.error("⚠️ **API Rate Limit Reached.** You've exceeded your Gemini free-tier quota. Please wait a few minutes and try again, or enable billing at [aistudio.google.com](https://aistudio.google.com).")
            elif "API_KEY" in err.upper():
                st.error("⚠️ **Invalid API Key.** Please check your `GEMINI_API_KEY` in Streamlit secrets.")
            else:
                st.error(f"⚠️ An unexpected error occurred: {e}")
