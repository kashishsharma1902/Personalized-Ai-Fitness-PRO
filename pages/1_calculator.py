import streamlit as st

st.set_page_config(page_title="Metrics Calculator", page_icon="📊", layout="wide")

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

    .form-card {
        background: #1a1a2e;
        border: 1px solid #0f3460;
        border-radius: 16px;
        padding: 32px;
        margin-bottom: 20px;
    }
    .form-card h3 { color: #e94560; font-size: 1rem; font-weight: 700;
                    text-transform: uppercase; letter-spacing: 1px; margin-bottom: 18px; }

    .result-card {
        background: linear-gradient(135deg, #0f3460, #1a1a2e);
        border: 1px solid #e94560;
        border-radius: 16px;
        padding: 28px;
        margin-top: 24px;
    }
    .result-card h3 { color: #fff; font-size: 1.1rem; font-weight: 700; margin-bottom: 16px; }

    div[data-testid="metric-container"] {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 16px;
    }
    div[data-testid="metric-container"] label { color: #a0aec0 !important; font-size: 0.85rem; }
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #ffffff !important; font-size: 1.5rem; font-weight: 700;
    }

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

    .success-banner {
        background: linear-gradient(135deg, #1a2e1a, #0f3d1a);
        border: 1px solid #38a169;
        border-radius: 12px;
        padding: 16px 20px;
        color: #68d391;
        font-weight: 600;
        margin-top: 16px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <h1>📊 Personal Metrics Calculator</h1>
    <p>Enter your details below to calculate your BMR, TDEE, BMI and daily macro targets.</p>
</div>
""", unsafe_allow_html=True)

with st.form("metrics_form"):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="form-card"><h3>🧍 Body Stats</h3>', unsafe_allow_html=True)
        weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
        height = st.number_input("Height (cm)", min_value=120, max_value=230, value=170)
        age    = st.number_input("Age (years)", min_value=15, max_value=80,  value=25)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="form-card"><h3>🎯 Goals & Lifestyle</h3>', unsafe_allow_html=True)
        gender   = st.selectbox("Gender", ["Male", "Female"])
        activity = st.selectbox("Activity Level", [
            "Sedentary (little or no exercise)",
            "Light (1–3 days/week)",
            "Moderate (3–5 days/week)",
            "Very Active (6–7 days/week)"
        ])
        goal = st.selectbox("Primary Goal", ["Lose Weight", "Maintain Weight", "Build Muscle"])
        st.markdown('</div>', unsafe_allow_html=True)

    submitted = st.form_submit_button("⚡ Calculate My Metrics", use_container_width=True)

if submitted:
    # BMR — Mifflin-St Jeor
    if gender == "Male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    multipliers = {
        "Sedentary (little or no exercise)": 1.2,
        "Light (1–3 days/week)":             1.375,
        "Moderate (3–5 days/week)":          1.55,
        "Very Active (6–7 days/week)":       1.725
    }
    tdee = bmr * multipliers[activity]

    if goal == "Lose Weight":
        target_cal = tdee - 400
        goal_note  = "🔻 400 kcal deficit applied"
    elif goal == "Build Muscle":
        target_cal = tdee + 300
        goal_note  = "🔺 300 kcal surplus applied"
    else:
        target_cal = tdee
        goal_note  = "⚖️ Maintenance calories"

    # BMI
    bmi = weight / ((height / 100) ** 2)
    bmi_category = (
        "Underweight" if bmi < 18.5 else
        "Normal Weight" if bmi < 25 else
        "Overweight" if bmi < 30 else
        "Obese"
    )

    # Macros
    protein_g = round(weight * 2.0)
    fat_g     = round(target_cal * 0.25 / 9)
    carb_g    = round((target_cal - protein_g * 4 - fat_g * 9) / 4)

    activity_clean = activity.split("(")[0].strip()

    st.session_state["user_data"] = {
        "weight": weight, "height": height, "age": age,
        "gender": gender, "activity": activity_clean, "goal": goal,
        "bmr": round(bmr), "tdee": round(target_cal),
        "bmi": round(bmi, 1), "bmi_category": bmi_category,
        "protein_g": protein_g, "fat_g": fat_g, "carb_g": carb_g,
    }

    st.markdown('<div class="success-banner">✅ Data saved successfully! Head to the AI Planner in the sidebar to generate your personalised plan.</div>', unsafe_allow_html=True)

    # Results
    st.markdown('<div class="result-card"><h3>📈 Your Results</h3>', unsafe_allow_html=True)
    r1, r2, r3, r4 = st.columns(4)
    r1.metric("🔥 Daily Calories",  f"{round(target_cal)} kcal", goal_note)
    r2.metric("⚡ BMR",             f"{round(bmr)} kcal")
    r3.metric("📏 BMI",             f"{round(bmi, 1)}")
    r4.metric("🏷️ BMI Category",    bmi_category)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="result-card"><h3>🍽️ Daily Macro Targets</h3>', unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    m1.metric("🥩 Protein", f"{protein_g}g",  "4 kcal/g")
    m2.metric("🫙 Fats",    f"{fat_g}g",      "9 kcal/g")
    m3.metric("🌾 Carbs",   f"{carb_g}g",     "4 kcal/g")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🥗 Go to AI Planner →", use_container_width=True):
        st.switch_page("pages/2_AI_Planner.py")
