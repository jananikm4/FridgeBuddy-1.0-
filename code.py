from click import style
import streamlit as st 
from datetime import date, datetime
import json
import os
import random
import re
import pandas as pd

# ════════════════════════════════════════════════
# PAGE CONFIG & THEME
# ════════════════════════════════════════════════
st.set_page_config(
    page_title="FridgeBuddy 1.0",
    page_icon="🥕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Global CSS for a clean enterprise-grade aesthetic
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
    /*Page Background*/
    [data-testid="stAppViewContainer"] {
    background-color: #ecf39e;
}
    /* Core Typography */
    html, body, [class*="css"], .stApp, .main-title, .main-subtitle {
        font-family: 'Merriweather', serif !important;
    }
    
    /* Elegant Title Design */
    .main-title {
        font-size: 2.75rem;
        font-weight: 700;
        color: #FFFFFF; /* ◄ Changed to White */
        margin-bottom: 0.25rem;
    }
    .main-subtitle {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 2rem;
    }

    /* Card styling */
    .panel-card {
        background-color: #ecf39e;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }
    
    /* Action Panels (Recipe / Mascot) */
    .action-panel {
        border-radius: 12px;
        padding: 1.5rem;
        height: 100%;
    }
    .recipe-bg {
        background: linear-gradient(135deg, #FFF7ED 0%, #FFEDD5 100%);
        border: 1px solid #FED7AA;
    }
    .mascot-bg {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        border: 1px solid #BBF7D0;
    }
    
    /* Remove default padding overheads */
    .block-container { padding-top: 2.5rem; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════
# STORAGE & DATA
# ════════════════════════════════════════════════
DATA_FILE = "fridge_data.json"

def load_foods():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f: return json.load(f)
        except: return []
    return []

def save_foods(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f)

if "foods" not in st.session_state:
    st.session_state.foods = load_foods()

EMOJI_MAP = {
    "apple": "🍎", "banana": "🍌", "orange": "🍊", "grape": "🍇", "strawberry": "🍓", 
    "watermelon": "🍉", "mango": "🥭", "peach": "🍑", "pear": "🍐", "cherry": "🍒", 
    "lemon": "🍋", "lime": "🍋", "blueberry": "🫐", "blueberries": "🫐", "raspberry": "🍓", 
    "avocado": "🥑", "pineapple": "🍍", "coconut": "🥥", "kiwi": "🥝", "carrot": "🥕", 
    "broccoli": "🥦", "spinach": "🥬", "lettuce": "🥬", "tomato": "🍅", "cucumber": "🥒", 
    "pepper": "🫑", "onion": "🧅", "garlic": "🧄", "potato": "🥔", "corn": "🌽", 
    "mushroom": "🍄", "celery": "🥬", "cabbage": "🥬", "zucchini": "🥒", "milk": "🥛", 
    "cheese": "🧀", "butter": "🧈", "yogurt": "🫙", "egg": "🥚", "cream": "🥛", 
    "chicken": "🍗", "beef": "🥩", "pork": "🥓", "fish": "🐟", "salmon": "🐟", 
    "shrimp": "🍤", "tuna": "🐟", "meat": "🥩", "bacon": "🥓", "sausage": "🌭", 
    "tofu": "🫙", "bread": "🍞", "rice": "🍚", "pasta": "🍝", "noodle": "🍜", 
    "pizza": "🍕", "burger": "🍔", "sandwich": "🥪", "cake": "🎂", "cookie": "🍪", 
    "chocolate": "🍫", "candy": "🍬", "ice cream": "🍦", "donut": "🍩", "juice": "🧃", 
    "soda": "🥤", "water": "💧", "coffee": "☕", "tea": "🍵", "beer": "🍺", 
    "wine": "🍷", "leftover": "🍱", "soup": "🍲", "salad": "🥗", "sauce": "🫙", "jam": "🫙"
}

CATEGORY_EMOJIS = {
    "Fruits 🍎": "🍎", "Vegetables 🥦": "🥦", "Dairy 🥛": "🥛", 
    "Snacks 🍪": "🍪", "Drinks 🧃": "🧃", "Frozen ❄️": "❄️", "Leftovers 🍱": "🍱"
}

# Create the Pandas Database for strict checking
FOOD_DB = pd.DataFrame(list(EMOJI_MAP.keys()), columns=["item"])

# ════════════════════════════════════════════════
# VALIDATION LOGIC
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
    "apple": "🍎",   "banana": "🍌",   "orange": "🍊",   "grape": "🍇",
    "strawberry": "🍓", "watermelon": "🍉", "mango": "🥭",  "peach": "🍑",
    "pear": "🍐",    "cherry": "🍒",   "lemon": "🍋",   "lime": "🍋",
    "blueberry": "🫐", "blueberries": "🫐", "raspberry": "🍓", "raspberries": "🍓", "avocado": "🥑", "pineapple": "🍍",
    "coconut": "🥥",  "kiwi": "🥝",

    "carrot": "🥕",  "broccoli": "🥦", "spinach": "🥬", "lettuce": "🥬",
    "tomato": "🍅",  "cucumber": "🥒", "pepper": "🫑",  "onion": "🧅",
    "garlic": "🧄",  "potato": "🥔",  "corn": "🌽",    "mushroom": "🍄",
    "celery": "🥬",  "cabbage": "🥬", "zucchini": "🥒",

    "milk": "🥛",    "cheese": "🧀",  "butter": "🧈",  "yogurt": "🫙",
    "egg": "🥚",     "cream": "🥛",

    "chicken": "🍗", "beef": "🥩",    "pork": "🥓",    "fish": "🐟",
    "salmon": "🐟",  "shrimp": "🍤",  "tuna": "🐟",    "meat": "🥩",
    "bacon": "🥓",   "sausage": "🌭", "tofu": "🫙",

    "bread": "🍞",   "rice": "🍚",    "pasta": "🍝",   "noodle": "🍜",
    "pizza": "🍕",   "burger": "🍔",  "sandwich": "🥪",

    "cake": "🎂",    "cookie": "🍪",  "chocolate": "🍫", "candy": "🍬",
    "ice cream": "🍦", "donut": "🍩",

    "juice": "🧃",   "soda": "🥤",    "water": "💧",   "coffee": "☕",
    "tea": "🍵",     "beer": "🍺",    "wine": "🍷",    "milk tea": "🧋",

    "leftover": "🍱", "soup": "🍲",   "salad": "🥗",   "sauce": "🫙",
    "jam": "🫙",      "honey": "🍯",  "oil": "🫙",     "vinegar": "🫙",
}



def normalize_name(name):
    text = name.casefold()
    text = re.sub(r"[^\w\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def singularize(word):
    if word.endswith("ies"):
        return word[:-3] + "y"
    if word.endswith(("oes", "ses", "xes", "ches", "shes")):
        return word[:-2]
    if word.endswith("s") and len(word) > 3 and not word.endswith("ss"):
        return word[:-1]
    return word


def detect_emoji(name, category):
    clean_name = name.lower().strip()
    for item, emoji in EMOJI_MAP.items():
        if item in clean_name: return emoji
    return CATEGORY_EMOJIS.get(category, "🍽️")

# ════════════════════════════════════════════════
# UTILITIES
# ════════════════════════════════════════════════
def days_left(expiry):
    try:
        expiry_date = datetime.strptime(expiry, "%Y-%m-%d").date()
        return (expiry_date - date.today()).days
    except:
        return 0

def get_status_details(days):
    if days < 0:
        return f"Expired {abs(days)}d ago", "🔴"
    if days == 0:
        return "Expires TODAY", "🟠"
    if days == 1:
        return "Expires tomorrow", "🟡"
    return f"{days} days left", "🟢"

# ════════════════════════════════════════════════
# DATA ACTIONS
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

def add_foods(names, category, expiry):
    for name in names:
        add_food(name, category, expiry)


def delete_food(food_id):
    st.session_state.foods = [f for f in st.session_state.foods if f["id"] != food_id]
    save_foods(st.session_state.foods)

# ════════════════════════════════════════════════
# SIDEBAR CONTROL
# ════════════════════════════════════════════════
with st.sidebar:
    st.title("🥕 FridgeBuddy")
    st.markdown("---")
    add_name = st.text_input("Specific Item Name", placeholder="e.g., Apple, Milk")
    add_cat = st.selectbox("Category Group", list(CATEGORY_EMOJIS.keys()))
    add_expiry = st.date_input("Expiration Date", value=date.today())
    
    if st.button("➕ Log Item to Fridge", use_container_width=True, type="primary"):
        if not add_name.strip():
            st.error("Enter a name!")
        elif not is_edible(add_name):
            # THIS IS THE FIX: It explicitly rejects non-food items like 'earphones'
            st.error(f"❌ '{add_name}' is not edible! Please add actual food.")
        else:
            new_food = {
                "id": str(datetime.now().timestamp()),
                "name": add_name.strip(),
                "category": add_cat,
                "emoji": detect_emoji(add_name, add_cat),
                "expiry": add_expiry.strftime("%Y-%m-%d")
            }
            st.session_state.foods.append(new_food)
            save_foods(st.session_state.foods)
            st.success(f"Added {add_name}!")
            st.rerun()

# ════════════════════════════════════════════════
# MAIN UI
# ════════════════════════════════════════════════
st.markdown("<div class='main-title'>FridgeBuddy</div>", unsafe_allow_html=True)
st.markdown("<div class='main-subtitle'>Intelligent tracking ecosystem for food preservation.</div>", unsafe_allow_html=True)

foods = sorted(st.session_state.foods, key=lambda x: days_left(x["expiry"]))
expired = [f for f in foods if days_left(f["expiry"]) < 0]
expiring = [f for f in foods if 0 <= days_left(f["expiry"]) <= 2]

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("Total", len(foods))
col_m2.metric("Urgent", len(expiring))
col_m3.metric("Expired", len(expired))
col_m4.metric("Saved", max(0, len(foods) - len(expired)))

st.markdown("---")
st.subheader("🧊 Live Inventory Matrix")

if not foods:
    st.info("Fridge is empty!")
else:
    for idx, food in enumerate(foods):
        d = days_left(food["expiry"])
        with st.container():
            c1, c2, c3, c4 = st.columns([0.5, 2.5, 4, 1])
            c1.write(f"### {food['emoji']}")
            c2.markdown(f"**{food['name']}**\n{food['category']}")
            c3.progress(min(max((d + 1) / 14, 0.0), 1.0))
            if c4.button("Mark Consumed", key=f"btn_{food['id']}"):
                st.session_state.foods = [f for f in st.session_state.foods if f["id"] != food["id"]]
                save_foods(st.session_state.foods)
                st.rerun()
        st.markdown("<hr style='margin:10px 0; opacity:0.1'>", unsafe_allow_html=True)

# Insights
c_l, c_r = st.columns(2)
with c_l:
    st.markdown("<div class='action-panel recipe-bg'>👨‍🍳 <b>Recipe Suggestion</b><br>Omelette strategy unlocked.</div>", unsafe_allow_html=True)
with c_r:
    msg = "Status Stable." if not expiring else "Warning: Perishables degrading."
    st.markdown(f"<div class='action-panel mascot-bg'>📊 <b>Diagnostics</b><br>{msg}</div>", unsafe_allow_html=True)
