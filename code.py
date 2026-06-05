from click import style
import streamlit as st 
from datetime import date, datetime
import json
import os
import random
import re

# ════════════════════════════════════════════════
# PAGE CONFIG & CLEAN THEME
# ════════════════════════════════════════════════
st.set_page_config(
    page_title="FridgeBuddy 1.0",
    page_icon="🥕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Global CSS for a clean enterprise-grade aesthetic
# (Merged later in file to avoid nested string literals)

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



st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>

    /* Core Typography */
    html, body, [class*="css"], .stApp, .main-title, .main-subtitle {
        font-family: 'Merriweather', serif !important;
    }

    /* Page Background */
    body, .stApp, .block-container {
        background-color: #a53860 !important;
    }

    /* Elegant Title Design */
    .main-title {
        font-size: 2.75rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 0.25rem;
    }
    .main-subtitle {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 2rem;
    }

    /* Card styling */
    /*
    .panel-card {
        background-color: #a53860 !important;
        border: 1px solid #000000 !important;
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }
    */

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
    normalized = normalize_name(name)
    for keyword, emoji in EMOJI_MAP.items():
        if keyword in normalized:
            return emoji

    for token in normalized.split():
        token = singularize(token)
        for keyword, emoji in EMOJI_MAP.items():
            if keyword == token:
                return emoji

    return CATEGORY_EMOJIS.get(category, "🍽️")


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
    st.caption("Shelf Life Tracking")
    st.space = st.empty()
    st.markdown("---")
    
    add_name = st.text_input(" Specific Item Name", placeholder="e.g., Greek Yogurt, Spinach")
    add_cat = st.selectbox("Category Group", list(CATEGORY_EMOJIS.keys()))
    add_expiry = st.date_input("Expiration Date", value=date.today())
    
    if add_name.strip():
        st.caption(f"Auto-assigned Icon: {detect_emoji(add_name, add_cat)}")
        
    if st.button("➕ Log Item to Fridge", use_container_width=True, type="primary"):
        raw_names = add_name.strip()
        if not raw_names:
            st.error("Please specify a valid item name.")
        else:
            names = [n.strip() for n in re.split(r"[,\n;]+", raw_names) if n.strip()]
            if not names:
                st.error("Please specify at least one valid item name.")
            else:
                if len(names) == 1:
                    add_food(names[0], add_cat, add_expiry)
                    st.success(f"Added {names[0]}!")
                else:
                    add_foods(names, add_cat, add_expiry)
                    st.success(f"Added {len(names)} items: {', '.join(names)}")
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
    filtered_foods = [f for f in filtered_foods if f["category"].casefold() == selected_category.casefold()]
if search.strip():
    filtered_foods = [f for f in filtered_foods if search.casefold() in f["name"].casefold()]

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
