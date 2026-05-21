# FridgeBuddy 🥕

> *Your cozy, stress-free fridge assistant — keeping your food (and your wallet) alive.*

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-red?style=flat-square&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

FridgeBuddy is a lightweight, beautifully-designed food expiry tracker built for college students who are tired of discovering science experiments at the back of their fridge. No databases, no logins, no complexity — just a JSON file and a cute carrot mascot cheering you on. 🥕

---

## ✨ Features

| Feature | Description |
|---|---|
| 📋 **Add Food Items** | Track any food with a name, category, and expiry date |
| 🍎 **Smart Emoji Detection** | Automatically assigns an emoji based on the food name |
| 🚨 **Expiring Soon Alert Zone** | High-visibility panel for items expiring within 2 days |
| 🧊 **Sorted Food List** | All items auto-sorted by closest expiry date |
| 🗑️ **One-Click Delete** | Remove items instantly when you eat (or mourn) them |
| 🥕 **Mascot Messages** | Dynamic, personality-rich messages from your carrot buddy |
| 📊 **Stats Dashboard** | Track total items, expiring soon, and food waste prevented |
| 🎨 **Cozy Aesthetic** | Sage green, cream white, soft peach — no harsh corporate blues |

---

## 🗂️ File Structure

```
fridgebuddy/
│
├── app.py                 # Main Streamlit UI, layout, and state management
├── storage.py             # JSON read/write: load, save, add, delete
├── food_utils.py          # Date math, status labels, sorting, emoji detection
├── mascot_messages.py     # Contextual mascot personality and message logic
├── requirements.txt       # Python dependencies
├── README.md              # You're reading it!
│
└── data/
    └── foods.json         # Auto-created on first run — no setup needed!
```

---

## 🚀 Run Locally

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/fridgebuddy.git
cd fridgebuddy
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch FridgeBuddy

```bash
streamlit run app.py
```

Your browser will open automatically at `http://localhost:8501`. 🎉

> **Note:** The `data/` folder and `foods.json` are created automatically on first run — no manual setup required!

---

## ☁️ Deploy to Streamlit Community Cloud

1. Push your repo to GitHub.
2. Visit [share.streamlit.io](https://share.streamlit.io) and sign in.
3. Click **New app** → select your repo → set `app.py` as the main file.
4. Click **Deploy**. That's it!

> FridgeBuddy uses `os.path.abspath(__file__)` for all file paths, making it fully compatible with Linux-based cloud deployments.

---

## 🎨 Design Philosophy

FridgeBuddy was designed to feel like a *"cute little fridge assistant"*, not a corporate inventory system. Every design decision reinforces this:

- **Palette**: Sage green (#8fbc8f), Cream white (#fdf9f3), Soft peach (#ffb4a2), Pastel yellow (#ffd97d)
- **Typography**: Nunito — rounded, friendly, and modern
- **Cards**: Custom HTML mini-cards with soft backgrounds and rounded corners
- **Mascot**: A contextual carrot character with rotating personality-driven messages

---

## 🧠 How It Works

```
User adds food  →  storage.py saves to data/foods.json
                →  food_utils.py calculates days_left()
                →  app.py renders sorted cards with urgency colours
                →  mascot_messages.py picks a contextual message
                →  User eats food → delete_food() removes it instantly
```

---

## 📸 Screenshots

> *(Add your own screenshots after running the app — a GIF of the mascot messages is especially charming for a GitHub portfolio!)*

---

## 🛠️ Built With

- [Streamlit](https://streamlit.io/) — UI framework
- [Python `datetime`](https://docs.python.org/3/library/datetime.html) — Date calculations
- [Python `json` + `os`](https://docs.python.org/3/library/json.html) — Local storage
- [Google Fonts — Nunito](https://fonts.google.com/specimen/Nunito) — Typography

---

## 🙌 Contributing

PRs welcome! Ideas for future features:
- [ ] Push notifications for expiring items
- [ ] Barcode scanner integration
- [ ] Recipe suggestions based on expiring ingredients
- [ ] Weekly "fridge health" summary emails

---

## 📄 License

MIT — go wild, use it, fork it, impress your professors with it. 🎓

---

*Made with 💚 for college students who forget about their food 😅*
