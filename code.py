import streamlit as st
from datetime import date, datetime
import json
import os
import random

# ════════════════════════════════════════════════
# PAGE CONFIG & CLEAN THEME
# ════════════════════════════════════════════════
st.set_page_config(
    page_title="FridgeBuddy",
    page_icon="🥕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Global CSS for a clean enterprise-grade aesthetic
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Core Typography */
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', sans-serif;
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
        background-color: #FFFFFF;
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
# STORAGE LAYER
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
# METADATA MAPS
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

def delete_food(food_id):
    st.session_state.foods = [f for f in st.session_state.foods if f["id"] != food_id]
    save_foods(st.session_state.foods)

# ════════════════════════════════════════════════
# SIDEBAR CONTROL
# ════════════════════════════════════════════════
with st.sidebar:
    st.title("🥕 FridgeBuddy")
    st.caption("Smart Shelf Tracking")
    st.space = st.empty()
    st.markdown("---")
    
    add_name = st.text_input("Item Name", placeholder="e.g., Greek Yogurt, Spinach")
    add_cat = st.selectbox("Category Group", list(CATEGORY_EMOJIS.keys()))
    add_expiry = st.date_input("Expiration Date", value=date.today())
    
    if add_name.strip():
        st.caption(f"Auto-assigned Icon: {detect_emoji(add_name, add_cat)}")
        
    if st.button("➕ Log Item to Fridge", use_container_width=True, type="primary"):
        if not add_name.strip():
            st.error("Please specify a valid item name.")
        else:
            add_food(add_name.strip(), add_cat, add_expiry)
            st.success(f"Added {add_name.strip()}!")
            st.rerun()

# ════════════════════════════════════════════════
# APP CONTAINER & STATISTICS
# ════════════════════════════════════════════════
st.markdown("<div class='main-title'>FridgeBuddy</div>", unsafe_allow_html=True)
st.markdown("<div class='main-subtitle'>Intelligent tracking ecosystem for household food preservation.</div>", unsafe_allow_html=True)

# Data Processing
foods = sorted(st.session_state.foods, key=lambda x: days_left(x["expiry"]))
expired = [f for f in foods if days_left(f["expiry"]) < 0]
expiring = [f for f in foods if 0 <= days_left(f["expiry"]) <= 2]

# Premium Native Metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric(label="Total Inventory", value=len(foods))
m2.metric(label="Critical (<48h)", value=len(expiring), delta=f"{len(expiring)} urgent" if expiring else None, delta_color="inverse")
m3.metric(label="Expired Status", value=len(expired), delta=f"{len(expired)} items" if expired else None, delta_color="off")
m4.metric(label="Saved Counter", value=max(0, len(foods) - len(expired)))

st.markdown("<br>", unsafe_allow_html=True)

# ════════════════════════════════════════════════
# FILTERS & SEARCH CONTROLS
# ════════════════════════════════════════════════
ctrl_col1, ctrl_col2 = st.columns([1, 2])
with ctrl_col1:
    selected_category = st.selectbox("Category Filter", ["All Categories"] + list(CATEGORY_EMOJIS.keys()), label_visibility="collapsed")
with ctrl_col2:
    search = st.text_input("Search Engine", placeholder="🔍 Search current kitchen inventory...", label_visibility="collapsed")

filtered_foods = foods
if selected_category != "All Categories":
    filtered_foods = [f for f in filtered_foods if f["category"] == selected_category]
if search.strip():
    filtered_foods = [f for f in filtered_foods if search.lower() in f["name"].lower()]

# Bulk Clean-Up Button
if expired:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🧹 Purge All Expired Items from Database", use_container_width=True):
        st.session_state.foods = [f for f in st.session_state.foods if days_left(f["expiry"]) >= 0]
        save_foods(st.session_state.foods)
        st.toast("Database optimized: Expired elements wiped.")
        st.rerun()

st.markdown("---")

# ════════════════════════════════════════════════
# INVENTORY DISPLAY PLATFORM
# ════════════════════════════════════════════════
st.subheader("🧊 Live Inventory Matrix")

if not filtered_foods:
    st.info("No tracking assets match your current structural filters. Add objects or clear filters to begin.")
else:
    for idx, food in enumerate(filtered_foods):
        d = days_left(food["expiry"])
        label, indicator = get_status_details(d)
        
        # Using built-in containers with subtle custom markup for precise alignment
        with st.container():
            col_icon, col_details, col_progress, col_action = st.columns([0.5, 2.5, 4, 1])
            
            with col_icon:
                st.markdown(f"<div style='font-size: 2rem; padding-top: 5px; text-align: center;'>{food['emoji']}</div>", unsafe_allow_html=True)
                
            with col_details:
                st.markdown(f"**{food['name']}** &nbsp;•&nbsp; <small style='color:#64748B;'>{food['category']}</small>", unsafe_allow_html=True)
                st.markdown(f"<small>{indicator} {label}</small>", unsafe_allow_html=True)
                
            with col_progress:
                progress_val = min(max((d + 1) / 14, 0.0), 1.0)
                st.markdown("<div style='padding-top: 15px;'></div>", unsafe_allow_html=True)
                st.progress(progress_val)
                
            with col_action:
                st.markdown("<div style='padding-top: 5px;'></div>", unsafe_allow_html=True)
                if st.button("Mark Consumed", key=f"del_{food['id']}_{idx}", use_container_width=True, type="secondary"):
                    delete_food(food["id"])
                    st.rerun()
                    
            st.markdown("<div style='border-bottom: 1px solid #F1F5F9; margin: 0.75rem 0;'></div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════
# ANALYTICS & INSIGHT MODULES
# ════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
c_left, c_right = st.columns(2)

with c_left:
    recipe_messages = [
        "Omelette curation strategy unlocked.",
        "Sandwich asset deployment opportunities detected.",
        "Wok-fried rice optimization highly recommended.",
        "Fruit smoothie extraction sequence ready.",
        "Noodle base assembly parameters activated."
    ]
    st.markdown(f"""
    <div class='action-panel recipe-bg'>
        <h4 style='color: #9A3412; margin-top:0;'>👨‍🍳 Smart Recipe Suggestion</h4>
        <p style="font-size: 0.95rem; color: #C2410C; font-weight: 500; margin: 0;"> 
            {random.choice(recipe_messages)} 
        </p>
    </div>
    """, unsafe_allow_html=True)

with c_right:
    good_messages = [
        "Inventory stabilization complete. No waste trajectories predicted.",
        "Zero food casualties imminent. High shelf efficiency.",
        "Storage patterns demonstrate maximum emotional and structural stability."
    ]
    chaos_messages = [
        "Dairy structures are demonstrating aggressive degradation curves.",
        "Action required: Consume imminent perishables to prevent structural decay.",
        "Leafy green properties are losing biological integrity."
    ]
    message = random.choice(chaos_messages) if len(expiring) > 2 or len(expired) > 0 else random.choice(good_messages)
    
    st.markdown(f"""
    <div class='action-panel mascot-bg'>
        <h4 style='color: #166534; margin-top:0;'>📊 Diagnostics & Insights</h4>
        <p style="font-size: 0.95rem; color: #15803D; font-weight: 500; margin: 0;"> 
            {message} 
        </p>
    </div>
    """, unsafe_allow_html=True)
