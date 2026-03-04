import streamlit as st

st.set_page_config(
    page_title="AI Fitness Pro",
    layout="wide",
    page_icon="💪",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Global font */
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
    }

    /* Hide default Streamlit header */
    #MainMenu, footer, header {visibility: hidden;}

    /* Hero section */
    .hero {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-radius: 20px;
        padding: 60px 40px;
        text-align: center;
        margin-bottom: 30px;
    }
    .hero h1 {
        font-size: 3.2rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 10px;
        letter-spacing: -1px;
    }
    .hero p {
        font-size: 1.2rem;
        color: #a0aec0;
        margin-bottom: 30px;
    }
    .hero span { color: #e94560; }

    /* Feature cards */
    .feature-card {
        background: #1a1a2e;
        border: 1px solid #0f3460;
        border-radius: 16px;
        padding: 28px 24px;
        text-align: center;
        height: 100%;
        transition: transform 0.2s;
    }
    .feature-card:hover { transform: translateY(-4px); }
    .feature-card .icon { font-size: 2.4rem; margin-bottom: 12px; }
    .feature-card h3 { color: #ffffff; font-size: 1.1rem; margin-bottom: 8px; }
    .feature-card p  { color: #a0aec0; font-size: 0.9rem; line-height: 1.5; }

    /* Info box */
    .info-box {
        background: linear-gradient(135deg, #0f3460, #1a1a2e);
        border-left: 4px solid #e94560;
        border-radius: 12px;
        padding: 24px;
        margin-top: 10px;
    }
    .info-box h4 { color: #e94560; margin-bottom: 14px; font-size: 1rem; }
    .info-box p  { color: #cbd5e0; font-size: 0.92rem; margin: 6px 0; }
    .info-box strong { color: #ffffff; }
</style>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
    <div class="icon">💪</div>
    <h1>AI Fitness <span>Pro</span></h1>
    <p>Your AI-Powered Health & Nutrition Companion — Personalized. Smart. Effective.</p>
</div>
""", unsafe_allow_html=True)

# Feature cards
c1, c2, c3, c4 = st.columns(4)
features = [
    ("📊", "Metrics Calculator", "Calculate your BMR, TDEE & BMI based on your personal stats."),
    ("🥗", "AI Meal Plans",      "Get a full-day meal plan tailored to your calorie and macro goals."),
    ("🏋️", "Workout Routines",  "Receive weekly workout plans with sets, reps & recovery advice."),
    ("💧", "Health Guidance",    "Personalised hydration, sleep & recovery recommendations."),
]
for col, (icon, title, desc) in zip([c1, c2, c3, c4], features):
    with col:
        st.markdown(f"""
        <div class="feature-card">
            <div class="icon">{icon}</div>
            <h3>{title}</h3>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Info + CTA
left, right = st.columns([1.2, 1])
with left:
    st.markdown("""
    <div class="info-box">
        <h4>📖 Key Terms Explained</h4>
        <p><strong>BMR</strong> — Basal Metabolic Rate: calories your body burns at complete rest.</p>
        <p><strong>TDEE</strong> — Total Daily Energy Expenditure: BMR adjusted for your activity level.</p>
        <p><strong>BMI</strong> — Body Mass Index: a measure of body composition using height & weight.</p>
        <p><strong>Macros</strong> — Macronutrients: Protein, Carbohydrates & Fats your body needs daily.</p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("👈 Use the **sidebar** to navigate between pages. Start with the **Calculator** to enter your details, then head to the **AI Planner** to generate your plan.")
    if st.button("🚀 Go to Calculator", use_container_width=True):
        st.switch_page("pages/1_calculator.py")

st.divider()
st.image(
    "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&q=80&w=1400",
    caption="Consistency is the key to lasting results.",
    use_container_width=True
)
