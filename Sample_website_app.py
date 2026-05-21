"""
app.py — FridgeBuddy 🥕
Main Streamlit entry-point. Owns layout, state management, and all UI rendering.
Run with:  streamlit run app.py
"""

import streamlit as st
from datetime import date

from sample_website_storage import load_foods, add_food, delete_food
from sample_website_food_utils import calculate_days_left
from sample_website_mascot import get_mascot_message


# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG  (must be first Streamlit call)
# ══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="FridgeBuddy 🥕",
    page_icon="🥕",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS — Cozy, rounded, pastel aesthetic
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
/* ── Google Font import ─────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Nunito+Sans:wght@400;600&display=swap');

/* ── Root palette ────────────────────────────────────────────── */
:root {
    --sage:      #8fbc8f;
    --sage-lt:   #c8e6c8;
    --sage-bg:   #f0f7f0;
    --cream:     #fdf9f3;
    --peach:     #ffb4a2;
    --peach-lt:  #ffe8e3;
    --yellow:    #ffd97d;
    --yellow-lt: #fff8e1;
    --red-soft:  #ff8a80;
    --red-lt:    #ffeaea;
    --text-dark: #3d3d3d;
    --text-mid:  #6b6b6b;
    --radius:    14px;
    --shadow:    0 4px 16px rgba(0,0,0,0.07);
}

/* ── Global base ─────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Nunito', 'Quicksand', sans-serif !important;
    background-color: var(--cream) !important;
    color: var(--text-dark) !important;
}

/* ── Hide default Streamlit chrome ───────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem !important; }

/* ── Sidebar ─────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: var(--sage-bg) !important;
    border-right: 2px solid var(--sage-lt) !important;
}
[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, var(--sage), #6aaa6a) !important;
    color: white !important;
    font-weight: 800 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: var(--radius) !important;
    padding: 0.65rem 1.2rem !important;
    width: 100% !important;
    box-shadow: 0 4px 12px rgba(143,188,143,0.4) !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 18px rgba(143,188,143,0.55) !important;
}

/* ── Generic action buttons (delete) ─────────────────────────── */
.stButton > button {
    border-radius: 8px !important;
    border: 1.5px solid #e0e0e0 !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    transition: transform 0.1s !important;
}
.stButton > button:hover {
    transform: scale(1.04) !important;
}

/* ── Metric cards ────────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: white !important;
    border-radius: var(--radius) !important;
    padding: 1rem 1.25rem !important;
    box-shadow: var(--shadow) !important;
    border: 1.5px solid #ececec !important;
}
[data-testid="stMetricLabel"] { font-weight: 700 !important; color: var(--text-mid) !important; }
[data-testid="stMetricValue"] { font-weight: 900 !important; color: var(--text-dark) !important; }

/* ── Input widgets ───────────────────────────────────────────── */
input, select, textarea {
    border-radius: 10px !important;
    font-family: 'Nunito', sans-serif !important;
}

/* ── Divider ─────────────────────────────────────────────────── */
hr { border-color: var(--sage-lt) !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HELPER: Render a food card as styled HTML
# ══════════════════════════════════════════════════════════════════════════════

def _card_style(urgency: str) -> tuple[str, str]:
    """Return (bg_color, border_color) based on urgency level."""
    return {
        "expired":  ("#ffeaea", "#ff8a80"),
        "critical": ("#fff8e1", "#ffd97d"),
        "warning":  ("#f0f7f0", "#8fbc8f"),
        "ok":       ("#fdf9f3", "#e0e0e0"),
    }.get(urgency, ("#fdf9f3", "#e0e0e0"))


def render_food_card_html(item: dict, days: int | None) -> str:
    """Generate the HTML string for one food mini-card (no interactive widgets inside)."""
    urgency = get_urgency_level(days)
    status  = get_status_label(days)
    bg, border = _card_style(urgency)

    return f"""
    <div style="
        background: {bg};
        border: 2px solid {border};
        border-radius: 14px;
        padding: 0.75rem 1.1rem;
        margin-bottom: 0.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 0.4rem;
    ">
        <div>
            <span style="font-size:1.5rem;">{item.get('emoji','🍽️')}</span>
            <strong style="font-size:1.05rem; margin-left:0.4rem;">{item['name']}</strong>
            <span style="
                font-size:0.78rem;
                background:#eee;
                border-radius:20px;
                padding:2px 10px;
                margin-left:0.5rem;
                color:#666;
            ">{item.get('category','').split(' ')[0]}</span>
        </div>
        <div style="font-size:0.9rem; font-weight:600; color:#555;">
            {status}
        </div>
    </div>
    """


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — Add Food Form
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 🥕 FridgeBuddy")
    st.markdown("*Your cozy fridge companion*")
    st.divider()

    st.markdown("### ➕ Add to Fridge")

    food_name = st.text_input(
        "Food Name",
        placeholder="e.g. Greek yogurt, Apples…",
        key="food_name_input",
    )

    category = st.selectbox(
        "Category",
        options=[
            "Fruits 🍎",
            "Vegetables 🥦",
            "Dairy 🥛",
            "Snacks 🍪",
            "Drinks 🧃",
            "Frozen ❄️",
            "Leftovers 🍱",
        ],
        key="category_input",
    )

    expiry_date = st.date_input(
        "Expiry Date",
        value=date.today(),
        min_value=date(2000, 1, 1),
        key="expiry_input",
    )

    # Preview detected emoji live
    if food_name.strip():
        detected = detect_emoji(food_name, category)
        st.markdown(
            f"<div style='font-size:0.85rem; color:#888; margin-top:-0.5rem;'>"
            f"Detected emoji: {detected}</div>",
            unsafe_allow_html=True,
        )

    add_clicked = st.button("🥗 Add to Fridge", use_container_width=True)

    if add_clicked:
        if not food_name.strip():
            st.error("Please enter a food name! 🙈")
        else:
            emoji = detect_emoji(food_name.strip(), category)
            add_food(food_name.strip(), category, emoji, expiry_date)
            st.success(f"Added {emoji} {food_name.strip()} to your fridge!")
            st.rerun()

    st.divider()
    st.markdown(
        "<div style='font-size:0.8rem; color:#999; text-align:center;'>"
        "Made with 💚 for college students<br>who forget about their food 😅"
        "</div>",
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# MAIN DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════

# ── Load & process data ────────────────────────────────────────────────────────
foods        = load_foods()
sorted_foods = sort_by_expiry(foods)
stats        = compute_stats(foods)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 1.5rem 0 0.5rem 0;">
    <h1 style="font-size:3rem; font-weight:900; margin:0; letter-spacing:-1px;">
        FridgeBuddy 🥕
    </h1>
    <p style="font-size:1.1rem; color:#888; margin-top:0.2rem; font-weight:600;">
        your friendly fridge assistant — keeping your food (and your wallet) alive ✨
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Metrics row ────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("📦 Total Items",        stats["total"])
c2.metric("🔥 Expiring Soon",      len(stats["expiring_soon"]))
c3.metric("💀 Already Expired",    len(stats["expired"]))
c4.metric("♻️ Waste Prevented",    f"{stats['waste_prevented']} items")

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 🚨 EXPIRING SOON ZONE
# ══════════════════════════════════════════════════════════════════════════════

critical_items = [
    f for f in sorted_foods
    if get_urgency_level(days_left(f.get("expiry_date", ""))) == "critical"
]

if critical_items:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #fff8e1, #ffe8e3);
        border: 2.5px solid #ffd97d;
        border-radius: 18px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 18px rgba(255,180,0,0.15);
    ">
        <h3 style="margin:0 0 0.6rem 0; color:#b8860b; font-size:1.2rem;">
            🚨 Eat These NOW — Expiring Within 2 Days!
        </h3>
    """, unsafe_allow_html=True)

    for item in critical_items:
        days = days_left(item.get("expiry_date", ""))
        status = get_status_label(days)
        st.markdown(
            f"<div style='display:flex; align-items:center; gap:0.6rem; "
            f"margin-bottom:0.3rem; font-size:1rem; font-weight:700;'>"
            f"<span style='font-size:1.4rem;'>{item.get('emoji','🍽️')}</span>"
            f"<span>{item['name']}</span>"
            f"<span style='color:#b8860b; font-weight:600;'>— {status}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 🧊 MAIN FOOD LIST
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("### 🧊 Your Fridge")

if not sorted_foods:
    st.markdown("""
    <div style="
        text-align:center;
        padding: 3rem 2rem;
        background: #f9f9f9;
        border-radius: 18px;
        border: 2px dashed #ccc;
        color: #aaa;
        font-size: 1.1rem;
    ">
        <div style="font-size:3rem;">🫙</div>
        <strong>Your fridge is empty!</strong><br>
        Add your first item using the sidebar →
    </div>
    """, unsafe_allow_html=True)
else:
    for item in sorted_foods:
        days = days_left(item.get("expiry_date", ""))

        # Render the styled card
        st.markdown(render_food_card_html(item, days), unsafe_allow_html=True)

        # Delete button sits right below the card in a narrow column
        _, btn_col = st.columns([6, 1])
        with btn_col:
            if st.button("🗑️ Eat/Delete", key=f"del_{item['id']}"):
                delete_food(item["id"])
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# 🥕 MASCOT SECTION
# ══════════════════════════════════════════════════════════════════════════════

st.divider()
st.markdown("### 🥕 Carrot Says…")

mascot_data  = get_mascot_message(stats)
mood_emoji   = get_mood_emoji(mascot_data["mood"])

# Mood-based background colors
mood_colors = {
    "happy":   ("#f0f7f0", "#8fbc8f"),
    "worried": ("#fff8e1", "#ffd97d"),
    "sad":     ("#ffeaea", "#ff8a80"),
    "chaos":   ("#ffe8e3", "#ffb4a2"),
}
bg_color, border_color = mood_colors.get(mascot_data["mood"], ("#f9f9f9", "#ccc"))

st.markdown(f"""
<div style="
    background: {bg_color};
    border: 2px solid {border_color};
    border-radius: 18px;
    padding: 1.5rem 2rem;
    display: flex;
    align-items: flex-start;
    gap: 1.2rem;
    box-shadow: 0 4px 16px rgba(0,0,0,0.06);
">
    <div style="font-size: 3.5rem; line-height: 1;">{mood_emoji}</div>
    <div>
        <p style="font-size:1.05rem; font-weight:700; margin:0 0 0.6rem 0; color:#3d3d3d;">
            {mascot_data['message']}
        </p>
        <p style="font-size:0.88rem; color:#777; margin:0; font-style:italic;">
            {mascot_data['tip']}
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
