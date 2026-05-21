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
    "apple": "🍎", "banana": "🍌", "milk": "🥛", "egg": "🥚",
    "bread": "🍞", "pizza": "🍕", "burger": "🍔", "rice": "🍚",
    "cake": "🎂", "coffee": "☕", "tea": "🍵", "carrot": "🥕",
    "broccoli": "🥦", "cheese": "🧀", "pasta": "🍝", "noodle": "🍜",
    "tomato": "🍅", "potato": "🥔", "onion": "🧅", "garlic": "🧄"
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
    try:
        expiry_date = datetime.strptime(expiry, "%Y-%m-%d").date()
        return (expiry_date - date.today()).days
    except:
        return 0

def status_text(days):
    if days < 0:
        return f"💀 Expired {abs(days)} day(s) ago"
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
    st.session_state.foods = [f for f in st.session_state.foods if f["id"] != food_id]
    save_foods(st.session_state.foods)

# ════════════════════════════════════════════════
# SORTING & DATA SPLITTING
# ════════════════════════════════════════════════
foods = sorted(st.session_state.foods, key=lambda x: days_left(x["expiry"]))
expired = [f for f in foods if days_left(f["expiry"]) < 0]
expiring = [f for f in foods if 0 <= days_left(f["expiry"]) <= 2]

# ════════════════════════════════════════════════
# MASTER THEME AND TEXT CONTRAST OVERRIDES
# ════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 2rem; }

.stApp { background: linear-gradient(135deg, #fff7ec, #ffe5bf, #ffd18f); }
h1, h2, h3 { color: #070A3C !important; }

/* Main app content text color fix */
.stApp p, .stApp span, .stApp label, .stApp div:not([data-testid="stSidebar"]) { color: #222222; }

/* ── FOOLPROOF SIDEBAR TEXT FIX ── */
section[data-testid="stSidebar"] { 
    background: linear-gradient(180deg, #070A3C, #062375) !important; 
}
section[data-testid="stSidebar"] * { 
    color: #ffffff !important; 
}

/* Fix input placeholder options to never be white-on-white */
div[data-baseweb="select"] * {
    color: #222222 !important;
}

/* Clean UI Input Fields */
.stTextInput input, .stDateInput input { 
    background: white !important; 
    color: #222 !important; 
    border-radius: 16px !important; 
    border: 2px solid rgba(240,102,42,0.2) !important; 
}
.stSelectbox > div > div { 
    background: white !important; 
    border-radius: 16px !important; 
    border: 2px solid rgba(240,102,42,0.2) !important; 
}

/* Interactive Hover Buttons */
.stButton > button { 
    background: linear-gradient(135deg, #F0662A, #F6941D) !important; 
    color: white !important; 
    border: none !important; 
    border-radius: 18px !important; 
    font-weight: 800 !important; 
    box-shadow: 0 4px 10px rgba(240,102,42,0.25) !important;
    transition: 0.2s cubic-bezier(0.4, 0, 0.2, 1); 
}
.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(240,102,42,0.4) !important; }

/* Dashboard Cards */
[data-testid="stMetric"] { background: rgba(255,255,255,0.85); border-radius: 24px; padding: 1.2rem; backdrop-filter: blur(10px); box-shadow: 0 8px 24px rgba(0,0,0,0.03); }

/* Premium HTML Food Cards */
.html-food-card {
    border-radius: 20px;
    padding: 1.2rem;
    margin-bottom: 0.5rem;
    box-shadow: 0 6px 14px rgba(0,0,0,0.04);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.stProgress > div > div > div > div { background: linear-gradient(90deg, #F6941D, #F0662A) !important; }
.recipe-box { background: linear-gradient(135deg, #F0662A, #F6941D); padding: 1.5rem; border-radius: 24px; box-shadow: 0 8px 20px rgba(240,102,42,0.2); }
.recipe-box * { color: white !important; }

.mascot-box { background: linear-gradient(135deg, #070A3C, #062375); padding: 1.5rem; border-radius: 24px; box-shadow: 0 8px 20px rgba(7,10,60,0.2); }
.mascot-box * { color: white !important; }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════
with st.sidebar:
    st.title("🥕 FridgeBuddy")
    st.caption("your chaotic fridge assistant")
    st.divider()
    
    add_name = st.text_input("Food Name", placeholder="e.g. Tomato, Milk, Yogurt...", key="sidebar_add_name")
    add_cat = st.selectbox("Category", list(CATEGORY_EMOJIS.keys()), key="sidebar_add_cat")
    add_expiry = st.date_input("Expiry Date", value=date.today(), key="sidebar_add_expiry")
    
    if add_name.strip():
        st.info(f"Detected emoji: {detect_emoji(add_name, add_cat)}")
        
    if st.button("🥗 Add to Fridge", use_container_width=True):
        if not add_name.strip():
            st.error("Enter a food name 😭")
        else:
            add_food(add_name.strip(), add_cat, add_expiry)
            st.success(f"Added {add_name.strip()}!")
            st.rerun()

# ════════════════════════════════════════════════
# MAIN HEADER TITLE
# ════════════════════════════════════════════════
st.markdown("""
<div style='text-align:center;'>
    <h1 style='font-size:4.5rem;font-weight:900;'> 🥕 FridgeBuddy </h1>
    <p style='font-size:1.2rem; font-weight:600; opacity:0.85; color: #333333;'> keeping your food alive one panic notification at a time </p>
</div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ════════════════════════════════════════════════
# METRICS ROW
# ════════════════════════════════════════════════
c1, c2, c3, c4 = st.columns(4)
c1.metric("📦 Total", len(foods))
c2.metric("🔥 Expiring Soon", len(expiring))
c3.metric("💀 Expired", len(expired))
c4.metric("♻️ Saved", max(0, len(foods) - len(expired)))
st.markdown("<br>", unsafe_allow_html=True)

# ════════════════════════════════════════════════
# FILTER INVENTORY CONTROL
# ════════════════════════════════════════════════
f1, f2 = st.columns(2)
with f1:
    selected_category = st.selectbox("Filter Category", ["All"] + list(CATEGORY_EMOJIS.keys()))
with f2:
    search = st.text_input("🔍 Search", placeholder="Search items in your fridge...")

filtered_foods = foods
if selected_category != "All":
    filtered_foods = [f for f in filtered_foods if f["category"] == selected_category]
if search.strip():
    filtered_foods = [f for f in filtered_foods if search.lower() in f["name"].lower()]

# ════════════════════════════════════════════════
# BULK REMOVAL
# ════════════════════════════════════════════════
if expired:
    if st.button("🧹 Clear All Expired Items", use_container_width=True):
        st.session_state.foods = [f for f in st.session_state.foods if days_left(f["expiry"]) >= 0]
        save_foods(st.session_state.foods)
        st.success("Expired items removed!")
        st.rerun()

# ════════════════════════════════════════════════
# COMPONENT: MAIN FOOD TRACKER VIEW
# ════════════════════════════════════════════════
st.subheader("🧊 Your Fridge")

if len(filtered_foods) == 0:
    st.markdown("""
    <div style='text-align:center; padding:4rem; background: rgba(255,255,255,0.6); border-radius: 24px; border: 2px dashed rgba(0,0,0,0.1);'>
        <div style='font-size:5rem;'>🫙</div>
        <h2 style='margin-top:1rem; color: #070A3C;'>Your matching fridge contents are empty</h2>
        <p style='color:#666;'>Clear your search filters or add a new food item from the sidebar container!</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for food in filtered_foods:
        d = days_left(food["expiry"])
        bg = {"expired": "#ffe5e5", "critical": "#fff0df", "warning": "#fff7df", "good": "#ffffff"}[urgency(d)]
        
        # Premium nested card logic block
        st.markdown(f"""
        <div class="html-food-card" style="background: {bg}; border: 1px solid rgba(0,0,0,0.05);">
            <div>
                <span style="font-size:1.8rem; margin-right:0.5rem;">{food["emoji"]}</span>
                <strong style="font-size:1.3rem; color:#070A3C;">{food["name"]}</strong>
                <br><span style="font-size:0.85rem; color:#666;">{food["category"]}</span>
            </div>
            <div style="text-align: right;">
                <span style="font-size:1.1rem; font-weight:800; color:#070A3C;">{status_text(d)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Layout matching spacing for progress bars and consume action triggers
        col_bar, col_btn = st.columns([5, 1])
        with col_bar:
            progress = min(max((d + 1) / 14, 0.0), 1.0)
            st.progress(progress)
        with col_btn:
            if st.button("🗑️ Consumed", key=food["id"], use_container_width=True):
                delete_food(food["id"])
                st.rerun()
        st.markdown("<div style='margin-bottom:1.5rem;'></div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════
# PANELS: RECIPES & MASCOT SYSTEM
# ════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
c_left, c_right = st.columns(2)

with c_left:
    recipe_messages = [
        "🍳 Omelette arc unlocked.",
        "🥪 Sandwich engineering opportunity detected.",
        "🍚 Fried rice would go hard right now.",
        "🥤 Smoothie time.",
        "🍜 Noodle era activated."
    ]
    st.markdown(f"""
    <div class='recipe-box'>
        <h3> 👨‍🍳 Recipe Suggestion </h3>
        <p style="font-size:1.1rem; font-weight:600;"> {random.choice(recipe_messages)} </p>
    </div>
    """, unsafe_allow_html=True)

with c_right:
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
    message = random.choice(chaos_messages) if len(expiring) > 2 or len(expired) > 0 else random.choice(good_messages)
    st.markdown(f"""
    <div class='mascot-box'>
        <h3> 🥕 Carrot Says... </h3>
        <p style="font-size:1.1rem; font-weight:600;"> {message} </p>
    </div>
    """, unsafe_allow_html=True)
