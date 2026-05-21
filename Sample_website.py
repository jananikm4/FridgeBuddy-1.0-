import streamlit as st
import json
import os
import random
from datetime import datetime

# ==============================================================================
# 1. TECHNICAL ARCHITECTURE & DATA STORAGE CONFIGURATION
# ==============================================================================

# Relative storage path setup ensures it works on local machines & Streamlit Cloud
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
FILE_PATH = os.path.join(DATA_DIR, "foods.json")

def initialize_storage():
    """Safely creates data directory and blank JSON file on execution."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w") as f:
            json.dump([], f)

def load_foods():
    """Loads current virtual fridge contents from local storage database."""
    initialize_storage()
    try:
        with open(FILE_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_foods(foods):
    """Saves updated dictionary array payload to database."""
    initialize_storage()
    with open(FILE_PATH, "w") as f:
        json.dump(foods, f, indent=4)

def add_food_item(name, expiry_date, category, emoji):
    """Appends an incoming grocery asset item with a unique tracking identification key."""
    foods = load_foods()
    new_id = max([item.get("id", 0) for item in foods], default=0) + 1
    new_item = {
        "id": new_id,
        "name": name,
        "expiry_date": expiry_date.strftime("%Y-%m-%d"),
        "category": category,
        "emoji": emoji
    }
    foods.append(new_item)
    save_foods(foods)

def delete_food_item(item_id):
    """Removes tracked item by primary ID key instantly upon click event callback."""
    foods = load_foods()
    updated_foods = [item for item in foods if item.get("id") != item_id]
    save_foods(updated_foods)

# ==============================================================================
# 2. ALGORITHMIC FRIDGE INTELLIGENCE & UTILITY SCHEMAS
# ==============================================================================

EMOJI_DICTIONARY = {
    "apple": "🍎", "banana": "🍌", "milk": "🥛", "egg": "🥚", "cheese": "🧀",
    "carrot": "🥕", "tomato": "🍅", "potato": "🥔", "onion": "🧅", "chicken": "🍗",
    "meat": "🥩", "fish": "🐟", "rice": "🍚", "bread": "🍞", "yogurt": "🍦",
    "strawberry": "🍓", "berry": "🍓", "orange": "🍊", "lemon": "🍋", "mango": "🥭",
    "grape": "🍇", "watermelon": "🍉", "broccoli": "🥦", "lettuce": "🥬", "salad": "🥗",
    "spinach": "🥬", "cucumber": "🥒", "cake": "🍰", "chocolate": "🍫", "juice": "🧃",
    "soda": "🥤", "beer": "🍺", "pizza": "🍕", "burger": "🍔", "leftover": "🍱"
}

def auto_detect_emoji(food_name, category_emoji):
    """Contextual matching engine assigning individual custom icons based on keyword matching."""
    cleaned_name = food_name.lower().strip()
    for keyword, emoji in EMOJI_DICTIONARY.items():
        if keyword in cleaned_name:
            return emoji
    return category_emoji

def process_and_sort_fridge(foods_list):
    """Performs live date calculation routines and sorts closest expiration values first."""
    today = datetime.today().date()
    processed_list = []
    
    for item in foods_list:
        expiry_date = datetime.strptime(item["expiry_date"], "%Y-%m-%d").date()
        days_left = (expiry_date - today).days
        item_copy = item.copy()
        item_copy["days_left"] = days_left
        processed_list.append(item_copy)
        
    return sorted(processed_list, key=lambda x: x["days_left"])

def get_mascot_feedback(processed_foods):
    """Core algorithmic personality state selector generating chaotic/supportive micro-copy."""
    if not processed_foods:
        return "🧹 Your fridge is completely empty. Did you move out? Time to restock! 🛒"
        
    expired_items = [f for f in processed_foods if f["days_left"] < 0]
    expiring_soon = [f for f in processed_foods if 0 <= f["days_left"] <= 2]
    
    if expired_items:
        unfortunate_soldier = expired_items[0]["name"]
        msg = [
            f"🚨 We lost the {unfortunate_soldier} soldier 💔 it has seen things...",
            f"☣️ The {unfortunate_soldier} is creating a new ecosystem in there. Throw it away!",
            f"🤢 RIP {unfortunate_soldier}. Smells like bad decisions."
        ]
        return random.choice(msg)
        
    if expiring_soon:
        urgent_food = expiring_soon[0]["name"]
        msg = [
            f"😭 Girl PLEASE eat the {urgent_food}! It is literally fighting for survival right now.",
            f"👀 Don't you dare ignore the {urgent_food} today. It's calling your name.",
            f"⏱️ Tick tock, the {urgent_food} clock is running out!"
        ]
        return random.choice(msg)
        
    healthy_msg = [
        "Your fridge is thriving today ✨ no food casualties detected 🫡",
        "Looking good! Clean fridge, clean mind, wealthy bank account 💅",
        "No alarms ringing! Grab a healthy snack, you earned it 🍎"
    ]
    return random.choice(healthy_msg)

# ==============================================================================
# 3. STREAMLIT FRONTEND USER INTERFACE & DESIGN PATTERNS
# ==============================================================================

st.set_page_config(page_title="FridgeBuddy 🥕", page_icon="🥕", layout="centered")

# Custom Injectable Styling Layers via Markdown block configuration
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
    }
    .main-title {
        text-align: center;
        color: #2E5A44;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        color: #7A9E7E;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }
    .food-card {
        background-color: #F7F9F6;
        padding: 15px;
        border-radius: 12px;
        border-left: 5px solid #A3C9A8;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .food-card-expired {
        background-color: #FFF2F2;
        padding: 15px;
        border-radius: 12px;
        border-left: 5px solid #FF8A8A;
        margin-bottom: 10px;
    }
    .food-card-urgent {
        background-color: #FFF9E6;
        padding: 15px;
        border-radius: 12px;
        border-left: 5px solid #FFD07B;
        margin-bottom: 10px;
    }
    .mascot-box {
        background-color: #FDF6EE;
        padding: 20px;
        border-radius: 16px;
        border: 2px dashed #E6A15C;
        text-align: center;
        margin-top: 25px;
    }
    </style>
""", unsafe_allowed_html=True)

# Main Dashboard Typography Headers
st.markdown("<h1 class='main-title'>FridgeBuddy 🥕</h1>", unsafe_allowed_html=True)
st.markdown("<p class='sub-title'>Your cute little fridge assistant to stop wasting groceries</p>", unsafe_allowed_html=True)

# SIDEBAR OPERATIONS PANEL
st.sidebar.markdown("### 📥 Restock Your Fridge")

CATEGORIES = {
    "Fruits 🍎": "🍎",
    "Vegetables 🥦": "🥦",
    "Dairy 🥛": "🥛",
    "Snacks 🍪": "🍪",
    "Drinks 🧃": "🧃",
    "Frozen ❄️": "❄️",
    "Leftovers 🍱": "🍱"
}

with st.sidebar.form(key="add_food_form", clear_on_submit=True):
    food_name = st.text_input("What did you buy?", placeholder="e.g., Greek Yogurt, Strawberries")
    category_selection = st.selectbox("Category", list(CATEGORIES.keys()))
    expiry_date = st.date_input("Expiry Date", datetime.today().date())
    
    submit_button = st.form_submit_button(label="Add to Fridge ✨")

if submit_button:
    if food_name.strip() == "":
        st.sidebar.warning("Please type a food name first!")
    else:
        default_cat_emoji = CATEGORIES[category_selection]
        chosen_emoji = auto_detect_emoji(food_name, default_cat_emoji)
        
        add_food_item(food_name.strip(), expiry_date, category_selection, chosen_emoji)
        st.sidebar.success(f"Added {food_name} successfully!")
        st.rerun()

# LIVE RE-EVALUATION DATA FLOW PIPELINE
raw_foods = load_foods()
processed_foods = process_and_sort_fridge(raw_foods)

expired_list = [f for f in processed_foods if f["days_left"] < 0]
urgent_list = [f for f in processed_foods if 0 <= f["days_left"] <= 2]

# 🚨 VIEW CONTEXT ZONE A: EXPIRING SOON & EXPIRED HIGHLIGHTS
if expired_list or urgent_list:
    st.markdown("### 🚨 Urgent Attention Required")
    
    for item in expired_list:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"""
            <div class="food-card-expired">
                <span style="font-size:1.2rem;">{item['emoji']} <b>{item['name']}</b></span><br>
                <span style="color:#C70000; font-size:0.9rem;">⚠️ EXPIRED ({abs(item['days_left'])} days ago) • {item['category']}</span>
            </div>
            """, unsafe_allowed_html=True)
        with col2:
            st.write("")  # spacing balance container padding element
            if st.button("🗑️ Toss", key=f"exp_{item['id']}"):
                delete_food_item(item['id'])
                st.rerun()
                
    for item in urgent_list:
        col1, col2 = st.columns([4, 1])
        with col1:
            days_str = "TODAY" if item['days_left'] == 0 else "TOMORROW" if item['days_left'] == 1 else "in 2 days"
            st.markdown(f"""
            <div class="food-card-urgent">
                <span style="font-size:1.2rem;">{item['emoji']} <b>{item['name']}</b></span><br>
                <span style="color:#B87400; font-size:0.9rem;">⏱️ Expires {days_str} • {item['category']}</span>
            </div>
            """, unsafe_allowed_html=True)
        with col2:
            st.write("")
            if st.button("🍽️ Eat", key=f"urg_{item['id']}"):
                delete_food_item(item['id'])
                st.rerun()
                
    st.markdown("---")

# 🗄️ VIEW CONTEXT ZONE B: MAIN FRIDGE INVENTORY CONTENT VIEW
st.markdown("### 🥦 Your Fridge Contents")
if not processed_foods:
    st.info("Your virtual fridge is empty. Add items using the left sidebar menu panel to start tracking shelf life!")
else:
    for item in processed_foods:
        # Avoid cluttering layout with duplicates already displayed in the highlight grid view above
        if item['days_left'] <= 2:
            continue
            
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"""
            <div class="food-card">
                <span style="font-size:1.2rem;">{item['emoji']} <b>{item['name']}</b></span><br>
                <span style="color:#555; font-size:0.9rem;">🗓️ {item['days_left']} days remaining • {item['category']}</span>
            </div>
            """, unsafe_allowed_html=True)
        with col2:
            st.write("")
            if st.button("✅ Done", key=f"all_{item['id']}"):
                delete_food_item(item['id'])
                st.rerun()

# 🤖 VIEW CONTEXT ZONE C: MASCOT & ANALYTICAL METRIC DASHBOARDS
st.markdown("### 📊 Fridge Vital Stats")

total_items = len(processed_foods)
danger_count = len(urgent_list) + len(expired_list)
waste_prevented = total_items * 3 

stat1, stat2, stat3 = st.columns(3)
stat1.metric("Total Items", total_items)
stat2.metric("Expiring/Expired", danger_count, delta=f"{danger_count} items", delta_color="inverse")
stat3.metric("Waste Avoided", f"~{waste_prevented} lbs")

feedback_message = get_mascot_feedback(processed_foods)
st.markdown(f"""
<div class="mascot-box">
    <div style="font-size: 2.5rem; margin-bottom: 5px;">🥕</div>
    <div style="font-style: italic; color: #5C4033; font-weight: 600; font-size: 1.05rem;">
        "{feedback_message}"
    </div>
</div>
""", unsafe_allowed_html=True)
