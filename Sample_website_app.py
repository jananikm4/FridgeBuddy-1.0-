import streamlit as st
from datetime import date, datetime
import json
import os
import random

# ═══════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════
st.set_page_config(
    page_title="FridgeBuddy 🥕",
    page_icon="🥕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════
# STORAGE
# ═══════════════════════════════
DATA_FILE = "fridge_data.json"

def load_foods():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_foods(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

if "foods" not in st.session_state:
    st.session_state.foods = load_foods()

# ═══════════════════════════════
# THEMES
# ═══════════════════════════════
THEMES = {
    "Peachy Chaos": {
        "bg": "#FFF8F3",
        "card": "#FFFFFF",
        "accent": "#FF8A5B",
        "accent2": "#FFD6C8",
        "text": "#3A312E",
        "subtext": "#7A6E69"
    },
    "Strawberry Milk": {
        "bg": "#FFF1F4",
        "card": "#FFFFFF",
        "accent": "#FF6B8A",
        "accent2": "#FFD1DC",
        "text": "#4A2B34",
        "subtext": "#8B6B76"
    },
    "Matcha Cafe": {
        "bg": "#F6FAF2",
        "card": "#FFFFFF",
        "accent": "#7BA66A",
        "accent2": "#DDECCF",
        "text": "#2F3B2C",
        "subtext": "#6E7C69"
    }
}

# ═══════════════════════════════
# MASCOTS
# ═══════════════════════════════
MASCOTS = {
    "Carrot 🥕": {
        "emoji": "🥕",
        "good": [
            "we are SO back",
            "the fridge ecosystem is thriving",
            "no food casualties today bestie"
        ],
        "bad": [
            "girl please eat the spinach",
            "your yogurt is developing lore",
            "the strawberries are begging for mercy"
        ]
    },

    "Frog 🐸": {
        "emoji": "🐸",
        "good": [
            "you’re doing amazing sweetie",
            "tiny fridge victories matter",
            "your vegetables feel appreciated"
        ],
        "bad": [
            "oopsie the milk is scared",
            "maybe we save the lettuce today?",
            "the cheese is entering its final form"
        ]
    },

    "Cat 🐈": {
        "emoji": "🐈",
        "good": [
            "acceptable.",
            "surprisingly competent.",
            "you avoided disaster."
        ],
        "bad": [
            "pathetic.",
            "your fridge smells like consequences.",
            "i’ve seen raccoons meal prep better."
        ]
    }
}

# ═══════════════════════════════
# SETTINGS
# ═══════════════════════════════
with st.sidebar:

    st.title("⚙️ fridge settings")

    selected_theme = st.selectbox(
        "theme",
        list(THEMES.keys())
    )

    selected_mascot = st.selectbox(
        "mascot",
        list(MASCOTS.keys())
    )

theme = THEMES[selected_theme]
mascot = MASCOTS[selected_mascot]

# ═══════════════════════════════
# CSS
# ═══════════════════════════════
st.markdown(f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

html, body, [class*="css"] {{
    font-family: 'Nunito', sans-serif;
}}

.stApp {{
    background: {theme["bg"]};
}}

#MainMenu {{
    visibility: hidden;
}}

footer {{
    visibility: hidden;
}}

.block-container {{
    padding-top: 2rem;
    max-width: 1000px;
}}

.title {{
    font-size: 4rem;
    font-weight: 900;
    color: {theme["text"]};
    margin-bottom: 0;
}}

.subtitle {{
    color: {theme["subtext"]};
    font-size: 1.1rem;
    margin-top: -10px;
    margin-bottom: 2rem;
}}

.stat-pill {{
    background: {theme["card"]};
    border-radius: 25px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    border: 3px solid {theme["accent2"]};
}}

.stat-number {{
    font-size: 2rem;
    font-weight: 900;
    color: {theme["accent"]};
}}

.stat-label {{
    color: {theme["subtext"]};
    font-weight: 700;
}}

.food-card {{
    background: {theme["card"]};
    border-radius: 28px;
    padding: 1.2rem;
    margin-bottom: 1rem;
    box-shadow: 0 6px 16px rgba(0,0,0,0.05);
    border: 3px solid transparent;
    transition: 0.2s ease;
}}

.food-card:hover {{
    border: 3px solid {theme["accent2"]};
    transform: translateY(-2px);
}}

.food-name {{
    font-size: 1.3rem;
    font-weight: 800;
    color: {theme["text"]};
}}

.food-status {{
    color: {theme["subtext"]};
    font-weight: 700;
}}

.mascot-box {{
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 280px;
    background: white;
    border-radius: 28px;
    padding: 1.2rem;
    box-shadow: 0 8px 30px rgba(0,0,0,0.1);
    z-index: 999;
    animation: floaty 3s ease-in-out infinite;
}}

@keyframes floaty {{
    0% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-5px); }}
    100% {{ transform: translateY(0px); }}
}}

.mascot-face {{
    font-size: 3rem;
}}

.mascot-text {{
    color: {theme["text"]};
    font-weight: 700;
    margin-top: 0.5rem;
}}

.stButton > button {{
    background: {theme["accent"]} !important;
    color: white !important;
    border: none !important;
    border-radius: 18px !important;
    font-weight: 800 !important;
    height: 3rem !important;
}}

.stButton > button:hover {{
    transform: scale(1.02);
}}

.stTextInput input,
.stDateInput input,
.stSelectbox div[data-baseweb="select"] {{
    border-radius: 18px !important;
    border: 2px solid {theme["accent2"]} !important;
    background: white !important;
}}

</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════
# HELPERS
# ═══════════════════════════════
CATEGORYS = [
    "Fruits 🍓",
    "Vegetables 🥦",
    "Dairy 🥛",
    "Snacks 🍪",
    "Drinks 🧃",
    "Frozen ❄️"
]

EMOJIS = {
    "milk": "🥛",
    "apple": "🍎",
    "banana": "🍌",
    "pizza": "🍕",
    "bread": "🍞",
    "egg": "🥚",
    "rice": "🍚",
    "cheese": "🧀",
    "carrot": "🥕",
    "tomato": "🍅"
}

def detect_emoji(name):

    lower = name.lower()

    for key, emoji in EMOJIS.items():
        if key in lower:
            return emoji

    return "🍽️"

def days_left(expiry):

    expiry_date = datetime.strptime(
        expiry,
        "%Y-%m-%d"
    ).date()

    return (expiry_date - date.today()).days

def add_food(name, category, expiry):

    food = {
        "id": str(datetime.now().timestamp()),
        "name": name,
        "category": category,
        "emoji": detect_emoji(name),
        "expiry": expiry.strftime("%Y-%m-%d")
    }

    st.session_state.foods.append(food)
    save_foods(st.session_state.foods)

def delete_food(food_id):

    st.session_state.foods = [
        f for f in st.session_state.foods
        if f["id"] != food_id
    ]

    save_foods(st.session_state.foods)

# ═══════════════════════════════
# HEADER
# ═══════════════════════════════
st.markdown(f"""
<div class="title">
🥕 FridgeBuddy
</div>

<div class="subtitle">
your fridge but emotionally unstable
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════
# ADD FOOD
# ═══════════════════════════════
st.markdown("### ➕ add food")

c1, c2, c3 = st.columns(3)

with c1:
    add_name = st.text_input(
        "food name",
        placeholder="greek yogurt..."
    )

with c2:
    add_cat = st.selectbox(
        "category",
        CATEGORYS
    )

with c3:
    add_expiry = st.date_input(
        "expiry date",
        value=date.today()
    )

if st.button("add to fridge", use_container_width=True):

    if add_name.strip():

        add_food(
            add_name.strip(),
            add_cat,
            add_expiry
        )

        st.rerun()

# ═══════════════════════════════
# PROCESS DATA
# ═══════════════════════════════
foods = sorted(
    st.session_state.foods,
    key=lambda x: days_left(x["expiry"])
)

expired = [
    f for f in foods
    if days_left(f["expiry"]) < 0
]

expiring = [
    f for f in foods
    if days_left(f["expiry"]) <= 2
]

# ═══════════════════════════════
# STATS
# ═══════════════════════════════
s1, s2, s3 = st.columns(3)

stats = [
    ("🍓 alive", len(foods)),
    ("⚠️ danger", len(expiring)),
    ("💀 casualties", len(expired))
]

for col, stat in zip([s1, s2, s3], stats):

    with col:

        st.markdown(f"""
        <div class="stat-pill">
            <div class="stat-number">
                {stat[1]}
            </div>

            <div class="stat-label">
                {stat[0]}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════
# FRIDGE
# ═══════════════════════════════
st.markdown("## 🧊 fridge contents")

if not foods:

    st.markdown("""
    <div class="food-card" style="text-align:center;">
        <h2>your fridge is empty</h2>
        <p>this is between you and the carrot now</p>
    </div>
    """, unsafe_allow_html=True)

else:

    for idx, food in enumerate(foods):

        d = days_left(food["expiry"])

        if d < 0:
            status = f"💀 expired {abs(d)} day(s) ago"

        elif d == 0:
            status = "🔥 expires TODAY"

        elif d == 1:
            status = "⚠️ expires tomorrow"

        else:
            status = f"✨ {d} days left"

        left, right = st.columns([8,1])

        with left:

            st.markdown(f"""
            <div class="food-card">

                <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
                ">

                    <div>

                        <div class="food-name">
                            {food["emoji"]} {food["name"]}
                        </div>

                        <div class="food-status">
                            {food["category"]}
                        </div>

                    </div>

                    <div class="food-status">
                        {status}
                    </div>

                </div>

            </div>
            """, unsafe_allow_html=True)

        with right:

            if st.button(
                "eat",
                key=f"delete_{idx}"
            ):
                delete_food(food["id"])
                st.rerun()

# ═══════════════════════════════
# MASCOT MESSAGE
# ═══════════════════════════════
if len(expired) > 0 or len(expiring) > 2:

    mascot_message = random.choice(
        mascot["bad"]
    )

else:

    mascot_message = random.choice(
        mascot["good"]
    )

st.markdown(f"""
<div class="mascot-box">

    <div class="mascot-face">
        {mascot["emoji"]}
    </div>

    <div class="mascot-text">
        {mascot_message}
    </div>

</div>
""", unsafe_allow_html=True)
