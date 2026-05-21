import streamlit as st
from datetime import date, datetime
import json
import os
import random

# ════════════════════════════════════════════════
# PAGE CONFIG
# ════════════════════════════════════════════════
st.set_page_config(
    page_title="FridgeBuddy 🥕",
    page_icon="🥕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ════════════════════════════════════════════════
# COLORS
# ════════════════════════════════════════════════
HAWKBIT = "#FED46D"
MIMOLETTE = "#F6941D"
ORANGE = "#F0662A"
POHUTUKAWA = "#6A1A29"
BLUE = "#062375"
MIDNIGHT = "#070A3C"

# ════════════════════════════════════════════════
# STORAGE
# ════════════════════════════════════════════════
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

# ════════════════════════════════════════════════
# FOOD DATA
# ════════════════════════════════════════════════
CATEGORY_EMOJIS = {
    "Fruits 🍎": "🍎",
    "Vegetables 🥦": "🥦",
    "Dairy 🥛": "🥛",
    "Snacks 🍪": "🍪",
    "Drinks 🧃": "🧃",
    "Frozen ❄️": "❄️",
    "Leftovers 🍱": "🍱",
}

EMOJI_MAP = {
    "apple": "🍎",
    "banana": "🍌",
    "milk": "🥛",
    "egg": "🥚",
    "bread": "🍞",
    "pizza": "🍕",
    "burger": "🍔",
    "rice": "🍚",
    "cake": "🎂",
    "coffee": "☕",
    "tea": "🍵",
    "carrot": "🥕",
    "broccoli": "🥦",
    "cheese": "🧀",
    "pasta": "🍝",
    "noodle": "🍜",
}

def detect_emoji(name, category):
    lower = name.lower()

    for keyword, emoji in EMOJI_MAP.items():
        if keyword in lower:
            return emoji

    return CATEGORY_EMOJIS.get(category, "🍽️")

# ════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════
def days_left(expiry):
    expiry_date = datetime.strptime(expiry, "%Y-%m-%d").date()
    return (expiry_date - date.today()).days

def status_text(days):
    if days < 0:
        return f"💀 Expired {-days} day(s) ago"

    if days == 0:
        return "🔥 Expires TODAY"

    if days == 1:
        return "⚡ Expires tomorrow"

    if days <= 3:
        return f"😬 {days} days left"

    return f"✅ {days} days left"

def urgency(days):
    if days < 0:
        return "expired"

    if days <= 2:
        return "critical"

    if days <= 5:
        return "warning"

    return "good"

# ════════════════════════════════════════════════
# FOOD ACTIONS
# ════════════════════════════════════════════════
def add_food(name, category, expiry):
    food = {
        "id": str(datetime.now().timestamp()),
        "name": name,
        "category": category,
        "emoji": detect_emoji(name, category),
        "expiry": expiry.strftime("%Y-%m-%d")
    }

    st.session_state.foods.append(food)
    save_foods(st.session_state.foods)

def delete_food(food_id):
    st.session_state.foods = [
        food for food in st.session_state.foods
        if food["id"] != food_id
    ]

    save_foods(st.session_state.foods)

# ════════════════════════════════════════════════
# SORT
# ════════════════════════════════════════════════
foods = sorted(
    st.session_state.foods,
    key=lambda x: days_left(x["expiry"])
)

expired = [f for f in foods if days_left(f["expiry"]) < 0]
expiring = [f for f in foods if days_left(f["expiry"]) <= 2]

# ════════════════════════════════════════════════
# CSS
# ════════════════════════════════════════════════
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

#MainMenu, footer {
    visibility: hidden;
}

.stApp {
    background:
        linear-gradient(
            135deg,
            #fff7ec,
            #ffe5bf,
            #ffd18f
        );
}

.block-container {
    padding-top: 2rem;
}

h1, h2, h3 {
    color: #070A3C !important;
}

p, span, div, label {
    color: #333 !important;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #070A3C,
            #062375
        );
}

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: white !important;
}

/* INPUTS */

.stTextInput input,
.stDateInput input {
    background: white !important;
    color: #222 !important;
    border-radius: 16px !important;
    border: 2px solid rgba(240,102,42,0.2) !important;
}

/* SELECTBOX MAIN */

.stSelectbox > div > div {
    background: white !important;
    color: #222 !important;
    border-radius: 16px !important;
    border: 2px solid rgba(240,102,42,0.25) !important;
}

/* SELECTED TEXT */

.stSelectbox div[data-baseweb="select"] span {
    color: #222 !important;
    font-weight: 700 !important;
}

/* DROPDOWN MENU */

div[data-baseweb="popover"] {
    background: #fff7ef !important;
    border-radius: 16px !important;
    border: 2px solid rgba(240,102,42,0.2) !important;
}

/* OPTIONS */

div[role="option"] {
    background: transparent !important;
    color: #222 !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    margin: 4px !important;
}

/* OPTION HOVER */

div[role="option"]:hover {
    background: rgba(240,102,42,0.15) !important;
    color: #070A3C !important;
}

/* SELECTED OPTION */

div[aria-selected="true"] {
    background: rgba(240,102,42,0.18) !important;
    color: #070A3C !important;
}

/* BUTTONS */

.stButton > button {
    background:
        linear-gradient(
            135deg,
            #F0662A,
            #F6941D
        ) !important;

    color: white !important;
    border: none !important;
    border-radius: 18px !important;
    font-weight: 800 !important;
    transition: 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
}

/* METRICS */

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.75);
    border-radius: 24px;
    padding: 1rem;
    backdrop-filter: blur(10px);
}

/* FOOD CARDS */

.food-card {
    background: rgba(255,255,255,0.8);
    border-radius: 24px;
    padding: 1.2rem;
    margin-bottom: 1rem;
    box-shadow: 0 8px 18px rgba(0,0,0,0.05);
}

/* PROGRESS BAR */

.stProgress > div > div > div > div {
    background:
        linear-gradient(
            90deg,
            #F6941D,
            #F0662A
        ) !important;
}

/* RECIPE BOX */

.recipe-box {
    background:
        linear-gradient(
            135deg,
            #F0662A,
            #F6941D
        );

    padding: 1.5rem;
    border-radius: 24px;
}

.recipe-box * {
    color: white !important;
}

/* MASCOT */

.mascot-box {
    background:
        linear-gradient(
            135deg,
            #070A3C,
            #062375
        );

    padding: 1.5rem;
    border-radius: 24px;
}

.mascot-box * {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════
with st.sidebar:

    st.title("🥕 FridgeBuddy")
    st.caption("your chaotic fridge assistant")

    st.divider()

    food_name = st.text_input(
        "Food Name",
        placeholder="Greek yogurt..."
    )

    category = st.selectbox(
        "Category",
        list(CATEGORY_EMOJIS.keys())
    )

    expiry = st.date_input(
        "Expiry Date",
        value=date.today()
    )

    if food_name:
        st.info(
            f"Detected emoji: {detect_emoji(food_name, category)}"
        )

    if st.button("🥗 Add to Fridge", use_container_width=True):

        if food_name.strip() == "":
            st.error("Enter a food name 😭")

        else:
            add_food(food_name, category, expiry)
            st.success(f"Added {food_name}!")
            st.rerun()

# ════════════════════════════════════════════════
# TITLE
# ════════════════════════════════════════════════
st.markdown("""
<div style='text-align:center;'>

<h1 style='font-size:4.5rem;font-weight:900;'>
🥕 FridgeBuddy
</h1>

<p style='font-size:1.2rem;'>
keeping your food alive one panic notification at a time
</p>

</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ════════════════════════════════════════════════
# METRICS
# ════════════════════════════════════════════════
c1, c2, c3, c4 = st.columns(4)

c1.metric("📦 Total", len(foods))
c2.metric("🔥 Expiring Soon", len(expiring))
c3.metric("💀 Expired", len(expired))
c4.metric("♻️ Saved", max(0, len(foods) - len(expired)))

st.markdown("<br>", unsafe_allow_html=True)

# ════════════════════════════════════════════════
# FILTERS
# ════════════════════════════════════════════════
f1, f2 = st.columns(2)

with f1:
    selected_category = st.selectbox(
        "Filter Category",
        ["All"] + list(CATEGORY_EMOJIS.keys())
    )

with f2:
    search = st.text_input(
        "🔍 Search",
        placeholder="Search fridge..."
    )

filtered_foods = foods

if selected_category != "All":
    filtered_foods = [
        food for food in filtered_foods
        if food["category"] == selected_category
    ]

if search:
    filtered_foods = [
        food for food in filtered_foods
        if search.lower() in food["name"].lower()
    ]

# ════════════════════════════════════════════════
# CLEAR EXPIRED
# ════════════════════════════════════════════════
if expired:

    if st.button("🧹 Clear All Expired Items"):

        st.session_state.foods = [
            food for food in st.session_state.foods
            if days_left(food["expiry"]) >= 0
        ]

        save_foods(st.session_state.foods)

        st.success("Expired items removed!")
        st.rerun()

# ════════════════════════════════════════════════
# FOOD LIST
# ════════════════════════════════════════════════
st.subheader("🧊 Your Fridge")

if len(filtered_foods) == 0:

    st.markdown("""
    <div class='food-card' style='text-align:center;padding:4rem;'>

    <div style='font-size:5rem;'>🫙</div>

    <h2>Your fridge is empty</h2>

    <p>Add your first item from the sidebar →</p>

    </div>
    """, unsafe_allow_html=True)

else:

    for food in filtered_foods:

        d = days_left(food["expiry"])

        bg = {
            "expired": "#ffe5e5",
            "critical": "#fff0df",
            "warning": "#fff7df",
            "good": "rgba(255,255,255,0.8)"
        }[urgency(d)]

        st.markdown(f"""
        <div class='food-card' style='background:{bg};'>

        <h3>
        {food["emoji"]} {food["name"]}
        </h3>

        <p style='font-weight:700;'>
        {status_text(d)}
        </p>

        <p>
        {food["category"]}
        </p>

        </div>
        """, unsafe_allow_html=True)

        progress = min(max(d / 14, 0), 1)

        st.progress(progress)

        if st.button(
            "🫡 Consumed",
            key=food["id"],
            use_container_width=True
        ):
            delete_food(food["id"])
            st.rerun()

# ════════════════════════════════════════════════
# RECIPE BOX
# ════════════════════════════════════════════════
recipe_messages = [
    "🍳 Omelette arc unlocked.",
    "🥪 Sandwich engineering opportunity detected.",
    "🍚 Fried rice would go hard right now.",
    "🥤 Smoothie time.",
    "🍜 Noodle era activated."
]

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(f"""
<div class='recipe-box'>

<h3>
👨‍🍳 Recipe Suggestion
</h3>

<p>
{random.choice(recipe_messages)}
</p>

</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════
# MASCOT
# ════════════════════════════════════════════════
good_messages = [
    "Your fridge is thriving ✨",
    "No food casualties detected 🫡",
    "This fridge has emotional stability."
]

chaos_messages = [
    "Your yogurt is entering its villain arc 😭",
    "Please eat something before it develops consciousness.",
    "The spinach is fighting for its life."
]

message = (
    random.choice(chaos_messages)
    if len(expiring) > 2 or len(expired) > 0
    else random.choice(good_messages)
)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(f"""
<div class='mascot-box'>

<h3>
🥕 Carrot Says...
</h3>

<p>
{message}
</p>

</div>
""", unsafe_allow_html=True)
