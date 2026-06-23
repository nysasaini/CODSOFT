"""
CineGenre AI — Movie Genre Classifier
Netflix-style dynamic UI that re-themes itself based on the predicted genre.

Author: Nysa
Internship: CODSOFT AI Internship
"""

import streamlit as st
import joblib

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="CineGenre AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# GENRE THEMES
# Each genre gets: gradient colors, glow color, emoji, accent, tagline
# =========================================================
THEMES = {
    "horror": {
        "bg1": "#0a0000", "bg2": "#1a0000", "accent": "#ff1a1a",
        "glow": "rgba(255,0,0,0.35)", "emoji": "🔪",
        "tagline": "Something is watching in the dark...",
    },
    "thriller": {
        "bg1": "#05050f", "bg2": "#150024", "accent": "#a142f4",
        "glow": "rgba(161,66,244,0.35)", "emoji": "🕵️",
        "tagline": "Every second counts.",
    },
    "comedy": {
        "bg1": "#1a1400", "bg2": "#2b1f00", "accent": "#ffd60a",
        "glow": "rgba(255,214,10,0.35)", "emoji": "😂",
        "tagline": "Laughter loading...",
    },
    "romance": {
        "bg1": "#1a0010", "bg2": "#2b0020", "accent": "#ff4d8d",
        "glow": "rgba(255,77,141,0.35)", "emoji": "💕",
        "tagline": "Love is in the air.",
    },
    "action": {
        "bg1": "#1a0a00", "bg2": "#2b1300", "accent": "#ff7a00",
        "glow": "rgba(255,122,0,0.35)", "emoji": "💥",
        "tagline": "Buckle up. It's about to go off.",
    },
    "drama": {
        "bg1": "#0a0a12", "bg2": "#161624", "accent": "#5c7cfa",
        "glow": "rgba(92,124,250,0.30)", "emoji": "🎭",
        "tagline": "Real stories. Real emotions.",
    },
    "sci-fi": {
        "bg1": "#000a12", "bg2": "#001a2b", "accent": "#00e0ff",
        "glow": "rgba(0,224,255,0.35)", "emoji": "🚀",
        "tagline": "The future is now.",
    },
    "fantasy": {
        "bg1": "#0a0014", "bg2": "#1c0033", "accent": "#b388ff",
        "glow": "rgba(179,136,255,0.35)", "emoji": "🧙",
        "tagline": "Magic beyond imagination.",
    },
    "crime": {
        "bg1": "#0a0a0a", "bg2": "#1a0505", "accent": "#d92626",
        "glow": "rgba(217,38,38,0.30)", "emoji": "🚔",
        "tagline": "Justice has a price.",
    },
    "mystery": {
        "bg1": "#06060f", "bg2": "#10102a", "accent": "#8e7cff",
        "glow": "rgba(142,124,255,0.30)", "emoji": "🔍",
        "tagline": "Nothing is what it seems.",
    },
    "animation": {
        "bg1": "#001a14", "bg2": "#002b22", "accent": "#00e0a8",
        "glow": "rgba(0,224,168,0.35)", "emoji": "🎨",
        "tagline": "A world brought to life.",
    },
    "documentary": {
        "bg1": "#0a0e0a", "bg2": "#141f14", "accent": "#6fbf73",
        "glow": "rgba(111,191,115,0.30)", "emoji": "🎥",
        "tagline": "Reality, unfiltered.",
    },
    "family": {
        "bg1": "#0a1414", "bg2": "#0f2424", "accent": "#4dd0c4",
        "glow": "rgba(77,208,196,0.30)", "emoji": "👨‍👩‍👧",
        "tagline": "Stories for everyone.",
    },
    "adventure": {
        "bg1": "#0f1400", "bg2": "#1a2400", "accent": "#a3e635",
        "glow": "rgba(163,230,53,0.30)", "emoji": "🗺️",
        "tagline": "The journey begins.",
    },
    "music": {
        "bg1": "#140a1f", "bg2": "#241333", "accent": "#ff61d2",
        "glow": "rgba(255,97,210,0.30)", "emoji": "🎵",
        "tagline": "Feel the rhythm.",
    },
    "war": {
        "bg1": "#0d0d05", "bg2": "#1a1a0a", "accent": "#c9a227",
        "glow": "rgba(201,162,39,0.30)", "emoji": "⚔️",
        "tagline": "No story without sacrifice.",
    },
    "western": {
        "bg1": "#140d05", "bg2": "#241a0a", "accent": "#d98c3d",
        "glow": "rgba(217,140,61,0.30)", "emoji": "🤠",
        "tagline": "Out where the law runs thin.",
    },
    "biography": {
        "bg1": "#0a0a0e", "bg2": "#16161f", "accent": "#9aa5b1",
        "glow": "rgba(154,165,177,0.30)", "emoji": "📖",
        "tagline": "A life worth telling.",
    },
    "sport": {
        "bg1": "#001018", "bg2": "#001f2e", "accent": "#27b8ff",
        "glow": "rgba(39,184,255,0.30)", "emoji": "🏆",
        "tagline": "Victory takes everything.",
    },
}

DEFAULT_THEME = {
    "bg1": "#0a0a0a", "bg2": "#141414", "accent": "#E50914",
    "glow": "rgba(229,9,20,0.35)", "emoji": "🎬",
    "tagline": "AI-Powered Genre Prediction System",
}


def get_theme(genre):
    if not genre:
        return DEFAULT_THEME
    key = genre.strip().lower()
    return THEMES.get(key, DEFAULT_THEME)


# =========================================================
# SESSION STATE
# =========================================================
if "predicted_genre" not in st.session_state:
    st.session_state.predicted_genre = None
if "show_balloons" not in st.session_state:
    st.session_state.show_balloons = False

theme = get_theme(st.session_state.predicted_genre)

# =========================================================
# DYNAMIC CSS (re-rendered every run based on current theme)
# =========================================================
st.markdown(
    f"""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    /* ---------- DYNAMIC ANIMATED BACKGROUND ---------- */
    .stApp {{
        background: radial-gradient(circle at 20% 20%, {theme['glow']} 0%, transparent 45%),
                    radial-gradient(circle at 80% 80%, {theme['glow']} 0%, transparent 50%),
                    linear-gradient(160deg, {theme['bg1']} 0%, {theme['bg2']} 100%);
        background-attachment: fixed;
        transition: background 1.2s ease-in-out;
    }}

    /* ---------- HERO HEADER ---------- */
    .hero {{
        text-align: center;
        padding: 30px 10px 10px 10px;
        animation: fadeIn 1s ease-in-out;
    }}

    .hero .logo {{
        font-size: 46px;
        font-weight: 800;
        letter-spacing: 1px;
        color: {theme['accent']};
        text-shadow: 0 0 25px {theme['glow']};
    }}

    .hero .tagline {{
        font-size: 17px;
        color: #b3b3b3;
        margin-top: 6px;
        letter-spacing: 0.5px;
    }}

    /* ---------- GENRE CHIP ROW ---------- */
    .chip-row {{
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 10px;
        margin: 22px 0 8px 0;
    }}

    .chip {{
        padding: 7px 16px;
        border-radius: 999px;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        color: #d9d9d9;
        font-size: 13px;
        backdrop-filter: blur(6px);
    }}

    /* ---------- INPUT CARD ---------- */
    .input-card {{
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 18px;
        padding: 28px 30px;
        margin: 10px auto 0 auto;
        max-width: 900px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        backdrop-filter: blur(12px);
        animation: fadeIn 1s ease-in-out;
    }}

    .input-card h4 {{
        color: #f2f2f2;
        margin-bottom: 14px;
        font-weight: 700;
    }}

    .stTextArea textarea {{
        background: rgba(0,0,0,0.35) !important;
        color: #fff !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
    }}

    /* ---------- PREDICT BUTTON ---------- */
    div.stButton > button {{
        background: linear-gradient(135deg, {theme['accent']}, {theme['bg2']});
        color: white;
        font-weight: 700;
        font-size: 16px;
        padding: 12px 30px;
        border-radius: 12px;
        border: none;
        box-shadow: 0 6px 20px {theme['glow']};
        transition: all 0.25s ease-in-out;
    }}

    div.stButton > button:hover {{
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 10px 28px {theme['glow']};
    }}

    /* ---------- RESULT CARD ---------- */
    .result-card {{
        width: min(560px, 90%);
        margin: 36px auto 10px auto;
        padding: 36px 24px;
        border-radius: 24px;
        text-align: center;
        background: linear-gradient(160deg, rgba(255,255,255,0.08), rgba(255,255,255,0.02));
        border: 1px solid {theme['accent']}55;
        box-shadow: 0 18px 50px {theme['glow']};
        backdrop-filter: blur(14px);
        animation: popIn 0.5s ease-out;
    }}

    .result-card .emoji {{
        font-size: 64px;
        margin-bottom: 6px;
        filter: drop-shadow(0 0 18px {theme['glow']});
    }}

    .result-card .label {{
        font-size: 14px;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #aaaaaa;
        margin-bottom: 6px;
    }}

    .result-card .genre-name {{
        font-size: 44px;
        font-weight: 800;
        color: {theme['accent']};
        text-shadow: 0 0 30px {theme['glow']};
        margin: 4px 0 10px 0;
    }}

    .result-card .sub {{
        color: #cfcfcf;
        font-size: 14px;
    }}

    /* ---------- ANIMATIONS ---------- */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(-8px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    @keyframes popIn {{
        0% {{ opacity: 0; transform: scale(0.9); }}
        100% {{ opacity: 1; transform: scale(1); }}
    }}

    /* ---------- FOOTER ---------- */
    .footer {{
        text-align: center;
        color: #777;
        font-size: 13px;
        margin-top: 50px;
        padding-bottom: 20px;
    }}

    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #0a0a0a, #141414);
        border-right: 1px solid rgba(255,255,255,0.06);
    }}

    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# LOAD MODEL
# =========================================================
try:
    model = joblib.load("saved_model/model.pkl")
    tfidf = joblib.load("saved_model/tfidf.pkl")
    model_loaded = True
except Exception as e:
    model_loaded = False
    load_error = str(e)

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown(f"## {DEFAULT_THEME['emoji']} CineGenre AI")
    st.markdown("##### Movie Genre Classification System")
    st.markdown("---")
    st.markdown(
        """
        **Built using:**
        - Python
        - NLP (TF-IDF)
        - Scikit-learn

        **Models compared:**
        - Naive Bayes
        - Logistic Regression
        - Linear SVM

        **Final model:** best performer on test accuracy

        ---
        **Author:** Nysa
        **Internship:** CODSOFT AI Internship
        """
    )
    st.markdown("---")
    if st.session_state.predicted_genre:
        st.markdown(f"**Current theme:** {theme['emoji']} {st.session_state.predicted_genre.title()}")
        if st.button("↺ Reset theme"):
            st.session_state.predicted_genre = None
            st.rerun()

# =========================================================
# HERO HEADER
# =========================================================
st.markdown(
    f"""
    <div class="hero">
        <div class="logo">{theme['emoji']} CineGenre AI</div>
        <div class="tagline">{theme['tagline']}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Genre chip row (Netflix-style browse strip)
chips_html = "".join(
    f"<div class='chip'>{t['emoji']} {g.title()}</div>"
    for g, t in list(THEMES.items())[:12]
)
st.markdown(f"<div class='chip-row'>{chips_html}</div>", unsafe_allow_html=True)

# =========================================================
# INPUT CARD
# =========================================================
st.markdown("<div class='input-card'>", unsafe_allow_html=True)
st.markdown("#### 📝 Enter a Movie Plot")

plot = st.text_area(
    label="",
    height=220,
    placeholder="Example: A detective investigates a mysterious murder in New York City...",
    label_visibility="collapsed",
)

col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    predict = st.button("🎯 Predict Genre")

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# PREDICTION
# =========================================================
if predict:
    if not model_loaded:
        st.error(f"⚠️ Could not load model files: {load_error}")
    elif plot.strip() == "":
        st.warning("⚠️ Please enter a movie plot before predicting.")
    else:
        movie_vector = tfidf.transform([plot])
        prediction = model.predict(movie_vector)[0]

        st.session_state.predicted_genre = prediction
        st.session_state.show_balloons = True
        st.rerun()

# Render the result card from session state so it survives the rerun
# (and stays visible until the next prediction or reset).
if st.session_state.predicted_genre:
    st.markdown(
        f"""
        <div class="result-card">
            <div class="emoji">{theme['emoji']}</div>
            <div class="label">Predicted Genre</div>
            <div class="genre-name">{st.session_state.predicted_genre.title()}</div>
            <div class="sub">{theme['tagline']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.session_state.get("show_balloons"):
        st.balloons()
        st.session_state.show_balloons = False

# =========================================================
# FOOTER
# =========================================================
st.markdown(
    "<div class='footer'>Built during CODSOFT Internship · Powered by Streamlit & Scikit-learn</div>",
    unsafe_allow_html=True,
)