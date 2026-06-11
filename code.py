from click import style
import streamlit as st 
from datetime import date, datetime
import json
import os
import random
import re
import pandas as pd

# ════════════════════════════════════════════════
# PAGE CONFIG & DYNAMIC PALETTE THEME
# ════════════════════════════════════════════════
st.set_page_config(
    page_title="FridgeBuddy 1.0",
    page_icon="🥕",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
    [data-testid="stAppViewContainer"] { background-color: #ecf39e; }
    html, body, [class*="css"], .stApp, .main-title, .main-subtitle {
        font-family: 'Merriweather', serif !important;
        color: #f4f5f7 !important;
    }
    .main-title { font-size: 2.75rem; font-weight: 700; color: #FFFFFF; margin-bottom: 0.25rem; }
    .main-subtitle { font-size: 1.05rem; color: #64748B; margin-bottom: 2rem; }
    .action-panel { border-radius: 12px; padding: 1.5rem; height: 100%; }
    .recipe-bg { background: linear-gradient(135deg, #FFF7ED 0%, #FFEDD5 100%); border: 1px solid #FED7AA; }
    .mascot-bg { background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%); border: 1px solid #BBF7D0; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════
# STORAGE & DATA LAYER
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
def is_edible(name):
    """STRICT validation: Returns True ONLY if a food keyword is found in the input."""
    clean_name = name.lower().strip()
    # Check if any word in our Pandas DB exists inside the user's input
    matches = FOOD_DB[FOOD_DB['item'].apply(lambda x: x in clean_name)]
    return not matches.empty

def detect_emoji(name, category):
    clean_name = name.lower().strip()
    for item, emoji in EMOJI_MAP.items():
        if item in clean_name: return emoji
    return CATEGORY_EMOJIS.get(category, "🍽️")


def is_edible(name):
    clean_name = name.lower().strip()
    return any(item in clean_name for item in EMOJI_MAP.keys())

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
# MAIN UI LAYOUT PLATFORM
# ════════════════════════════════════════════════
st.markdown("<div class='main-title'>FridgeBuddy</div>", unsafe_allow_html=True)
st.markdown("<div class='main-subtitle'>Intelligent tracking ecosystem for household food preservation.</div>", unsafe_allow_html=True)

foods = sorted(st.session_state.foods, key=lambda x: days_left(x["expiry"]))
expired = [f for f in foods if days_left(f["expiry"]) < 0]
expiring = [f for f in foods if 0 <= days_left(f["expiry"]) <= 2]

# High Contrast Statistics Layer
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("Total Inventory", len(foods))
col_m2.metric("Urgent (<48h)", len(expiring))
col_m3.metric("Expired Status", len(expired))
col_m4.metric("Saved Counter", max(0, len(foods) - len(expired)))

st.markdown("---")
st.subheader("🧊 Live Inventory Matrix")

if not foods:
    st.info("Your virtual fridge is empty! Use the sidebar panel to add tracking objects.")
else:
    for idx, food in enumerate(foods):
        d = days_left(food["expiry"])
        
        # Color coding rows using the palette spectrum
        if d < 0:
            border_color = "#de350b" # Crimson Red border for expired
            bg_color = "rgba(222, 53, 11, 0.2)"
        elif d <= 2:
            border_color = "#ffb3c6" # Soft Rose Pink border for urgent
            bg_color = "rgba(255, 179, 198, 0.2)"
        else:
            border_color = "#2684ff" # Sky Blue border for normal
            bg_color = "rgba(38, 132, 255, 0.1)"

        st.markdown(f"""
        <div style="border-left: 6px solid {border_color}; background-color: {bg_color}; 
                    padding: 15px; border-radius: 10px; margin-bottom: 12px;">
            <table style="width:100%; border:none; border-collapse:collapse; background:transparent;">
                <tr style="background:transparent;">
                    <td style="width:8%; font-size:2.2rem; text-align:center; border:none; padding:0;">{food['emoji']}</td>
                    <td style="width:32%; border:none; padding:0 10px;">
                        <span style="font-size:1.15rem; font-weight:700; color:#f4f5f7;">{food['name']}</span><br>
                        <small style="color:#ffb3c6;">{food['category']}</small>
                    </td>
                    <td style="width:40%; border:none; padding:0 15px;">
                        <span style="font-size:0.9rem; font-weight:bold; color:{border_color};">
                            {f"⚠️ EXPIRED ({abs(d)}d ago)" if d < 0 else f"⏱️ EXPIRES IN {d} DAYS" if d <= 2 else f"🗓️ {d} days remaining"}
                        </span>
                    </td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
        
        # Inline functional action grid underneath the row layout
        act_col1, act_col2 = st.columns([7, 1])
        with act_col2:
            if st.button("Consume ✅", key=f"btn_{food['id']}", use_container_width=True):
                st.session_state.foods = [f for f in st.session_state.foods if f["id"] != food["id"]]
                save_foods(st.session_state.foods)
                st.rerun()

# ════════════════════════════════════════════════
# ANALYTICS & INSIGHT MODULES
# ════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
c_l, c_r = st.columns(2)

with c_l:
    st.markdown("""
    <div class='action-panel recipe-bg'>
        <h4 style='color: #0052cc; margin-top:0;'>👨‍🍳 Smart Recipe Suggestion</h4>
        <p style="font-size: 0.95rem; color: #0052cc; font-weight: 600; margin: 0;">
            Omelette curation strategy unlocked. Complete ingredient availability verified.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c_r:
    msg = "Inventory stabilization complete. No waste trajectories predicted." if not expiring else "Action required: Consume imminent perishables to prevent structural decay."
    st.markdown(f"""
    <div class='action-panel mascot-bg'>
        <h4 style='color: #0052cc; margin-top:0;'>📊 Diagnostics & Insights</h4>
        <p style="font-size: 0.95rem; color: #0052cc; font-weight: 600; margin: 0;">
            {msg}
        </p>
    </div>
    """, unsafe_allow_html=True)
