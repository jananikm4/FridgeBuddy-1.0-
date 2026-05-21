"""
mascot_messages.py — FridgeBuddy 🥕
Generates personality-rich mascot messages based on fridge state.
Keeps the comedy and warmth concentrated in one place for easy tweaking.
"""

import random


# ── Mascot identity ────────────────────────────────────────────────────────────
MASCOT_EMOJI = "🥕"   # Carrot buddy — our little icon
MASCOT_NAME  = "Carrot"


# ── Message pools ──────────────────────────────────────────────────────────────

HEALTHY_MESSAGES = [
    "Your fridge is absolutely thriving ✨ no food casualties detected 🫡",
    "All items are safe and sound! I'm so proud of you 🥹",
    "Chef's kiss 🤌 — your fridge is living its best life right now.",
    "Zero drama in the fridge today. Seriously impressive fridge management. 💅",
    "Everything is fresh and fine. You deserve a gold star ⭐ — take two.",
]

EXPIRING_TEMPLATES = [
    "Girl PLEASE eat the {name} {emoji} — it's fighting for its life out there 😭",
    "The {name} {emoji} is sending you a distress signal. It deserves better!! 🚨",
    "POV: your {name} {emoji} at 2am wondering why you haven't eaten it yet 🫠",
    "BREAKING: {name} {emoji} is on its last legs. This is not a drill. 😤",
    "{name} {emoji} said 'I thought we were friends' 😔 eat it before it's too late!",
]

EXPIRED_TEMPLATES = [
    "We lost the {name} {emoji} soldier 💔 it has seen things... may it rest in peace 🕯️",
    "Moment of silence for the {name} {emoji} 😔 it deserved better. We all did.",
    "The {name} {emoji} has left the chat 👋 please delete it and move forward.",
    "RIP {name} {emoji} — gone but not forgotten. Mostly just... gone. 🪦",
]

CHAOS_MESSAGES = [
    "Your fridge is living in complete chaos rn 😭 but we love you anyway 💚",
    "Multiple items at risk! This is a Code Green emergency 🚨 (green like the mold haha... sorry 😬)",
    "The fridge is screaming internally. Please. PLEASE eat something. 🥺",
]


# ── Public API ─────────────────────────────────────────────────────────────────

def get_mascot_message(stats: dict) -> dict:
    """
    Return a dict with keys: message (str), mood (str), tip (str).

    mood values: 'happy' | 'worried' | 'sad' | 'chaos'
    """
    expiring = stats.get("expiring_soon", [])
    expired  = stats.get("expired", [])
    total    = stats.get("total", 0)

    # ── Empty fridge ──
    if total == 0:
        return {
            "message": f"Hey! Add your first item so I can keep watch 👀 I'm very responsible, I promise.",
            "mood": "happy",
            "tip": "💡 Tip: Start by adding whatever's in your fridge right now — dairy & produce expire fastest!",
        }

    # ── Multiple crises ──
    if len(expiring) >= 3 and len(expired) >= 1:
        return {
            "message": random.choice(CHAOS_MESSAGES),
            "mood": "chaos",
            "tip": "💡 Tip: Batch-cook expiring items into one meal to save everything at once!",
        }

    # ── Expired items present ──
    if expired:
        item = expired[0]
        msg = random.choice(EXPIRED_TEMPLATES).format(
            name=item["name"], emoji=item.get("emoji", "🍽️")
        )
        return {
            "message": msg,
            "mood": "sad",
            "tip": "💡 Tip: Hit the 🗑️ button to remove expired items and keep your tracker accurate.",
        }

    # ── Items expiring soon ──
    if expiring:
        item = expiring[0]
        msg = random.choice(EXPIRING_TEMPLATES).format(
            name=item["name"], emoji=item.get("emoji", "🍽️")
        )
        return {
            "message": msg,
            "mood": "worried",
            "tip": "💡 Tip: Items expiring within 2 days make great stir-fry, smoothies, or omelettes!",
        }

    # ── All good ──
    return {
        "message": random.choice(HEALTHY_MESSAGES),
        "mood": "happy",
        "tip": "💡 Tip: Keep adding items as you shop so FridgeBuddy can watch over your whole fridge!",
    }


def get_mood_emoji(mood: str) -> str:
    """Map mood string → expressive emoji for the mascot face."""
    return {
        "happy":   "😄",
        "worried": "😰",
        "sad":     "😢",
        "chaos":   "🤯",
    }.get(mood, "🥕")
