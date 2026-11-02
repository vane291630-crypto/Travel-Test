"""
TRAVELOO / TRAVELWISE - Travel Destination Advisor Dashboard
Python + Streamlit

Install:
    py -m pip install --upgrade streamlit pandas

Run:
    py -m streamlit run travel_dashboard.py
"""

import html
from datetime import date
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Traveloo | Travel Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------- DESTINATION DATA -----------------------------
DESTINATIONS = [
    {
        "name": "Nha Trang",
        "country": "Vietnam",
        "state": "Khanh Hoa",
        "budget": 24000,
        "days": 5,
        "types": ["Beach", "Adventure", "Family"],
        "seasons": ["Winter", "Summer"],
        "best": "February to August",
        "activities": ["Island hopping", "Snorkelling", "Beach cafés", "Po Nagar towers"],
        "transport": "Fly to Cam Ranh Airport, then transfer",
        "rating": 4.9,
        "reviews": "1,022",
        "emoji": "🏝️",
        "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1000&q=85",
        "description": "Clear turquoise water, island trips and a lively beachfront promenade.",
    },
    {
        "name": "Paris",
        "country": "France",
        "state": "Île-de-France",
        "budget": 85000,
        "days": 5,
        "types": ["Culture", "Romantic", "History"],
        "seasons": ["Spring", "Summer", "Autumn"],
        "best": "April to June and September to October",
        "activities": ["Eiffel Tower", "Louvre Museum", "Seine cruise", "Montmartre"],
        "transport": "Fly to Charles de Gaulle or Orly Airport",
        "rating": 4.9,
        "reviews": "2,410",
        "emoji": "🗼",
        "image": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1000&q=85",
        "description": "Iconic architecture, museums, riverside walks and unforgettable cafés.",
    },
    {
        "name": "Bangkok",
        "country": "Thailand",
        "state": "Central Thailand",
        "budget": 32000,
        "days": 4,
        "types": ["Culture", "Food", "Shopping"],
        "seasons": ["Winter"],
        "best": "November to February",
        "activities": ["Grand Palace", "Wat Arun", "Floating markets", "Street food"],
        "transport": "Fly to Suvarnabhumi or Don Mueang Airport",
        "rating": 4.8,
        "reviews": "1,876",
        "emoji": "🏙️",
        "image": "https://images.unsplash.com/photo-1506189702168-3f5b6a5b4c8d?w=1000&q=85",
        "description": "A vibrant city full of temples, night markets and famous street food.",
    },
    {
        "name": "Rishikesh",
        "country": "India",
        "state": "Uttarakhand",
        "budget": 7000,
        "days": 3,
        "types": ["Adventure", "Nature", "Spiritual"],
        "seasons": ["Winter", "Summer"],
        "best": "September to November and February to May",
        "activities": ["River rafting", "Ganga Aarti", "Yoga", "Waterfall hikes"],
        "transport": "Road or train via Haridwar",
        "rating": 4.8,
        "reviews": "3,240",
        "emoji": "🏞️",
        "image": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?w=1000&q=85",
        "description": "A peaceful riverside town with Himalayan views and outdoor adventure.",
    },
    {
        "name": "Manali",
        "country": "India",
        "state": "Himachal Pradesh",
        "budget": 14000,
        "days": 5,
        "types": ["Adventure", "Nature", "Romantic"],
        "seasons": ["Winter", "Summer"],
        "best": "March to June; December to February for snow",
        "activities": ["Solang Valley", "Old Manali", "Hadimba Temple", "Mountain drives"],
        "transport": "Road or overnight bus",
        "rating": 4.8,
        "reviews": "2,180",
        "emoji": "🏔️",
        "image": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=1000&q=85",
        "description": "A mountain escape with pine forests, cafés and snow-season activities.",
    },
    {
        "name": "Jaipur",
        "country": "India",
        "state": "Rajasthan",
        "budget": 9000,
        "days": 3,
        "types": ["Culture", "History", "Family"],
        "seasons": ["Winter"],
        "best": "October to March",
        "activities": ["Amber Fort", "City Palace", "Hawa Mahal", "Local bazaars"],
        "transport": "Road, train or flight",
        "rating": 4.7,
        "reviews": "1,650",
        "emoji": "🏰",
        "image": "https://images.unsplash.com/photo-1599661046827-dacff0c0f09a?w=1000&q=85",
        "description": "The Pink City blends royal palaces, historic forts and colourful markets.",
    },
    {
        "name": "Goa",
        "country": "India",
        "state": "Goa",
        "budget": 18000,
        "days": 5,
        "types": ["Beach", "Adventure", "Nightlife"],
        "seasons": ["Winter"],
        "best": "November to February",
        "activities": ["Beach hopping", "Water sports", "Fort Aguada", "Café trail"],
        "transport": "Flight, train or road",
        "rating": 4.8,
        "reviews": "4,100",
        "emoji": "🏖️",
        "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=1000&q=85",
        "description": "Sunny beaches, coastal food, water sports and relaxed evenings.",
    },
    {
        "name": "Srinagar",
        "country": "India",
        "state": "Jammu and Kashmir",
        "budget": 22000,
        "days": 5,
        "types": ["Nature", "Romantic", "Family"],
        "seasons": ["Summer", "Winter"],
        "best": "April to October; winter for snow",
        "activities": ["Dal Lake shikara", "Mughal Gardens", "Houseboat stay", "Gulmarg"],
        "transport": "Flight or road",
        "rating": 4.9,
        "reviews": "2,760",
        "emoji": "🌊",
        "image": "https://images.unsplash.com/photo-1566837497312-7be4a6a3c4f8?w=1000&q=85",
        "description": "Beautiful lakes, gardens and mountain scenery in the Kashmir Valley.",
    },
]

TRIP_HISTORY = [
    {"place": "Da Lat", "country": "Vietnam", "dates": "04 Jan – 10 Jan", "status": "Completed", "rating": "4.9", "emoji": "🌿"},
    {"place": "Berlin", "country": "Germany", "dates": "04 Jan – 10 Jan", "status": "Completed", "rating": "5.0", "emoji": "🏛️"},
    {"place": "New York", "country": "USA", "dates": "04 Jan – 10 Jan", "status": "Completed", "rating": "4.8", "emoji": "🌆"},
    {"place": "Da Lat", "country": "Vietnam", "dates": "04 Jan – 10 Jan", "status": "Completed", "rating": "4.9", "emoji": "🌿"},
]

# ----------------------------- THEME -----------------------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "saved" not in st.session_state:
    st.session_state.saved = []
if "nav" not in st.session_state:
    st.session_state.nav = "Home"

DARK = st.session_state.dark_mode
if DARK:
    bg, surface, ink, muted, line = "#111a22", "#1b2934", "#eef5f7", "#a8bac4", "#30424e"
    hero_bg = "linear-gradient(115deg,#102b3d,#145d65,#138b80)"
else:
    bg, surface, ink, muted, line = "#f3f5f7", "#ffffff", "#17212b", "#6b7782", "#e6eaee"
    hero_bg = "linear-gradient(115deg,#dff8f5,#e8f6f7,#e8efff)"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@600;700;800&display=swap');
    :root{{--bg:{bg};--surface:{surface};--ink:{ink};--muted:{muted};--line:{line};--teal:#08b9b2;}}
    html,body,[class*="css"]{{font-family:'DM Sans',sans-serif;}}
    .stApp{{background:var(--bg);color:var(--ink);}}
    .block-container{{max-width:1500px;padding-top:1.15rem;padding-bottom:2.5rem;}}
    [data-testid="stSidebar"]{{background:var(--surface);border-right:1px solid var(--line);}}
    [data-testid="stSidebar"] *{{color:var(--ink);}}
    h1,h2,h3,h4{{color:var(--ink);font-family:'Manrope',sans-serif;}}
    .brand{{font:800 23px 'Manrope',sans-serif;color:#08aaa5;padding:8px 4px 20px;}}
    .hero{{background:{hero_bg};border:1px solid var(--line);border-radius:23px;padding:25px 30px;margin-bottom:18px;}}
    .hero-kicker{{font-size:10px;letter-spacing:2px;font-weight:800;color:#08a9a2;text-transform:uppercase;}}
    .hero h1{{font-size:32px;line-height:1.1;margin:7px 0;color:{'#ffffff' if DARK else '#142a38'};}}
    .hero p{{font-size:13px;margin:0;color:{'#d7eeee' if DARK else '#6b7782'};}}
    .topline{{display:flex;align-items:center;justify-content:space-between;gap:15px;margin:5px 0 20px;}}
    .section-title{{font:800 18px 'Manrope',sans-serif;color:var(--ink);margin:4px 0 12px;}}
    .muted{{color:var(--muted);font-size:12px;}}
    .panel{{background:var(--surface);border:1px solid var(--line);border-radius:17px;padding:17px;}}
    .trip-feature{{background:var(--surface);border:1px solid var(--line);border-radius:17px;padding:12px;}}
    .trip-feature img{{width:100%;height:190px;object-fit:cover;border-radius:12px;}}
    .trip-card{{background:var(--surface);border:1px solid var(--line);border-radius:15px;padding:9px;height:100%;}}
    .trip-card img{{width:100%;height:135px;object-fit:cover;border-radius:10px;}}
    .trip-card-title{{font-weight:800;color:var(--ink);font-size:14px;margin:8px 0 2px;}}
    .trip-card-meta{{color:var(--muted);font-size:11px;}}
    .pill{{display:inline-block;background:#e4f8f6;color:#078c87;border-radius:20px;padding:4px 9px;font-size:10px;font-weight:800;margin:2px;}}
    .history-row{{display:flex;align-items:center;gap:10px;background:var(--surface);border:1px solid var(--line);padding:10px;border-radius:12px;margin:8px 0;}}
    .history-emoji{{font-size:23px;}}
    .history-name{{font-size:12px;font-weight:800;color:var(--ink);}}
    .history-date{{font-size:10px;color:var(--muted);}}
    .history-rating{{margin-left:auto;color:#078c87;font-size:11px;font-weight:800;}}
    .calendar{{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:17px;}}
    .cal-head{{display:flex;justify-content:space-between;align-items:center;font-size:12px;font-weight:800;margin-bottom:13px;color:var(--ink);}}
    .cal-grid{{display:grid;grid-template-columns:repeat(7,1fr);gap:6px;text-align:center;}}
    .cal-day{{font-size:9px;color:var(--muted);padding:5px 0;}}
    .cal-date{{font-size:11px;padding:6px 0;border-radius:50%;color:var(--ink);}}
    .cal-date.active{{background:#08b9b2;color:white;font-weight:800;}}
    .cal-date.range{{background:#d9f5f2;color:#087d78;font-weight:700;}}
    .kpi-row{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:15px 0;}}
    .kpi{{background:var(--surface);border:1px solid var(--line);border-radius:13px;padding:13px;}}
    .kpi b{{font:800 20px 'Manrope',sans-serif;color:var(--ink);display:block;}}
    .kpi span{{font-size:10px;color:var(--muted);}}
    div.stButton>button{{border-radius:9px;font-weight:700;border:1px solid var(--line);}}
    div.stButton>button[kind="primary"]{{background:#08b9b2;color:white;border:0;}}
    div.stButton>button[kind="primary"]:hover{{background:#079c96;color:white;}}
    div[data-testid="stTabs"] button{{font-weight:700;}}
    .footer{{text-align:center;color:var(--muted);font-size:10px;margin-top:25px;}}
    @media(max-width:900px){{.hero h1{{font-size:26px;}}}}
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------- HELPERS -----------------------------
def money(value):
    return f"₹{round(value):,}"

def score_destination(place, budget, days, interests, season, group):
    score = 0
    reasons = []
    if place["budget"] <= budget:
        score += 3
        reasons.append("within budget")
    elif place["budget"] <= budget * 1.2:
        score += 1
        reasons.append("near budget")
    else:
        score -= 2

    gap = abs(place["days"] - days)
    if gap == 0:
        score += 2
        reasons.append("trip duration match")
    elif gap <= 2:
        score += 1

    matched = set(place["types"]).intersection(interests)
    score += len(matched) * 3
    if matched:
        reasons.append("interest match")

    if season in place["seasons"]:
        score += 2
        reasons.append("season match")

    if group == "Family" and "Family" in place["types"]:
        score += 2
    elif group == "Couple" and "Romantic" in place["types"]:
        score += 2
    elif group == "Friends" and any(x in place["types"] for x in ["Adventure", "Beach", "Nightlife"]):
        score += 2
    elif group == "Solo" and any(x in place["types"] for x in ["Nature", "Culture", "Adventure"]):
        score += 1

    max_score = 7 + max(1, len(interests)) * 3 + 2
    percent = max(1, min(99, round(score / max_score * 100)))
    return score, percent, reasons

def get_matches(budget, days, interests, season, group, count=6):
    output = []
    for place in DESTINATIONS:
        score, percent, reasons = score_destination(place, budget, days, interests, season, group)
        if score > 0:
            output.append({"place": place, "score": score, "percent": percent, "reasons": reasons})
    output.sort(key=lambda x: x["score"], reverse=True)
    return output[:count]

def render_calendar():
    days = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
    # Illustrative dashboard calendar for a 31-day month.
    dates = list(range(1, 32))
    cells = "".join(f'<div class="cal-day">{d}</div>' for d in days)
    cells += '<div></div>' * 2
    for d in dates:
        cls = "cal-date active" if d in (23, 28) else ("cal-date range" if 24 <= d <= 27 else "cal-date")
        cells += f'<div class="{cls}">{d}</div>'
    return f'<div class="calendar"><div class="cal-head"><span>ACTIVITY</span><span>‹ &nbsp; NOV 2026 &nbsp; ›</span></div><div class="cal-grid">{cells}</div></div>'

def safe_image(url, alt):
    return f'<img src="{html.escape(url, quote=True)}" alt="{html.escape(alt, quote=True)}"/>'

# ----------------------------- SIDEBAR NAVIGATION -----------------------------
with st.sidebar:
    st.markdown('<div class="brand">✿ Traveloo</div>', unsafe_allow_html=True)
    st.divider()
    nav_items = ["Home", "Booking", "Explore", "Messages", "Support", "Settings"]
    nav = st.radio(
        "NAVIGATION",
        nav_items,
        index=nav_items.index(st.session_state.nav) if st.session_state.nav in nav_items else 0,
        label_visibility="collapsed",
    )
    st.session_state.nav = nav
    st.divider()
    st.session_state.dark_mode = st.toggle("Dark mode", value=st.session_state.dark_mode)
    st.caption("Traveloo · Personal travel assistant")

# ----------------------------- INPUTS -----------------------------
with st.sidebar:
    st.markdown("### Trip preferences")
    budget = st.slider("Budget per person", 5000, 100000, 25000, 1000, format="₹%d")
    trip_days = st.slider("Trip duration", 2, 10, 4, format="%d days")
    season = st.selectbox("Travel season", ["Winter", "Summer", "Spring", "Autumn", "Monsoon"])
    group = st.selectbox("Travelling with", ["Friends", "Family", "Couple", "Solo"])
    interests = st.multiselect(
        "Interests",
        ["Nature", "Adventure", "Beach", "Culture", "History", "Spiritual", "Romantic", "Nightlife", "Family", "Food", "Shopping"],
        default=["Nature", "Adventure"],
    )
    stay_style = st.selectbox("Stay preference", ["Budget", "Comfort", "Premium"], index=1)

# ----------------------------- PAGE HEADER -----------------------------
st.markdown(
    """
    <div class="hero">
      <div class="hero-kicker">YOUR NEXT JOURNEY STARTS HERE</div>
      <h1>Hello, traveller! ✈️</h1>
      <p>Welcome back. Discover new places, plan your next trip and find destinations picked around your preferences.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Search input is a local filter over the known destination list.
search_col, notif_col = st.columns([8, 1])
with search_col:
    search_text = st.text_input(
        "Search destinations",
        placeholder="⌕  Search a destination, country or travel style...",
        label_visibility="collapsed",
    )
with notif_col:
    st.button("♧", help="Notifications")

# Dashboard recommendations
matches = get_matches(budget, trip_days, interests, season, group, 6) if interests else []
if search_text.strip():
    q = search_text.strip().lower()
    matches = [
        item for item in matches
        if q in item["place"]["name"].lower()
        or q in item["place"]["country"].lower()
        or any(q in t.lower() for t in item["place"]["types"])
    ]

saved_count = len(st.session_state.saved)
st.markdown(
    f"""
    <div class="kpi-row">
      <div class="kpi"><b>{len(DESTINATIONS)}</b><span>DESTINATIONS TO EXPLORE</span></div>
      <div class="kpi"><b>{money(budget)}</b><span>YOUR TRAVEL BUDGET</span></div>
      <div class="kpi"><b>{saved_count}</b><span>SAVED DESTINATIONS</span></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------- HOME DASHBOARD -----------------------------
if nav == "Home":
    left, right = st.columns([1.55, 1], gap="large")

    with left:
        st.markdown('<div class="section-title">Upcoming trip</div>', unsafe_allow_html=True)
        featured = next(p for p in DESTINATIONS if p["name"] == "Manali")
        st.markdown(
            f"""
            <div class="trip-feature">
              {safe_image(featured['image'], featured['name'])}
              <div style="padding:10px 4px 2px;">
                <div style="display:flex;justify-content:space-between;gap:10px;align-items:center;">
                  <div style="font-weight:800;font-size:17px;color:var(--ink);">{featured['name']} mountain escape</div>
                  <span class="pill">FEATURED</span>
                </div>
                <div class="muted">📅 12 Dec – 17 Dec &nbsp; · &nbsp; 📍 {featured['state']}</div>
                <p class="muted" style="margin:10px 0;">{featured['description']}</p>
                <span class="pill">✈ {money(featured['budget'])} estimated</span>
                <span class="pill">★ {featured['rating']} rating</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Explore this destination", type="primary", key="featured_explore"):
            st.session_state.nav = "Explore"
            st.rerun()

    with right:
        st.markdown('<div class="section-title">Travel calendar</div>', unsafe_allow_html=True)
        st.markdown(render_calendar(), unsafe_allow_html=True)
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="panel">
              <div style="font-weight:800;color:var(--ink);margin-bottom:5px;">Travel tip of the day ✨</div>
              <div class="muted">Keep a flexible schedule and check local weather and transport updates before leaving.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
    card_header, see_all = st.columns([5, 1])
    with card_header:
        st.markdown('<div class="section-title">Trips exclusively for you</div>', unsafe_allow_html=True)
    with see_all:
        if st.button("See all →", key="see_all_home"):
            st.session_state.nav = "Explore"
            st.rerun()

    if not interests:
        st.info("Choose at least one interest in the sidebar to get personalised suggestions.")
    elif not matches:
        st.info("No matches for this search. Try another destination or adjust your preferences.")
    else:
        cols = st.columns(3)
        for idx, item in enumerate(matches[:3]):
            p = item["place"]
            with cols[idx]:
                st.markdown(
                    f"""
                    <div class="trip-card">
                      {safe_image(p['image'], p['name'])}
                      <div class="trip-card-title">{p['emoji']} {p['name']} ({p['country']})</div>
                      <div class="trip-card-meta">{money(p['budget'])} · {p['days']} days</div>
                      <div style="margin-top:7px;"><span class="pill">★ {p['rating']}</span><span class="pill">{item['percent']}% match</span></div>
                      <div class="muted" style="margin-top:5px;">{html.escape(p['description'])}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button("View details", key=f"home_{p['name']}", use_container_width=True):
                    st.session_state.nav = "Explore"
                    st.rerun()

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    history_col, saved_col = st.columns([1.15, 1], gap="large")
    with history_col:
        st.markdown('<div class="section-title">Recently completed trips</div>', unsafe_allow_html=True)
        for trip in TRIP_HISTORY[:3]:
            st.markdown(
                f"""
                <div class="history-row">
                  <div class="history-emoji">{trip['emoji']}</div>
                  <div><div class="history-name">{trip['place']} ({trip['country']})</div>
                  <div class="history-date">{trip['dates']} · {trip['status']}</div></div>
                  <div class="history-rating">★ {trip['rating']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    with saved_col:
        st.markdown('<div class="section-title">Saved destinations</div>', unsafe_allow_html=True)
        if not st.session_state.saved:
            st.markdown('<div class="panel muted">Your saved destinations will appear here. Save a trip from the Explore page.</div>', unsafe_allow_html=True)
        else:
            for name in st.session_state.saved:
                st.write("♡", name)

# ----------------------------- EXPLORE PAGE -----------------------------
elif nav == "Explore":
    st.markdown('<div class="section-title">Explore destinations</div>', unsafe_allow_html=True)
    st.caption("Recommendations are ranked using your selected budget, season, travel group and interests.")
    if not interests:
        st.info("Select at least one interest in the sidebar.")
    else:
        all_matches = get_matches(budget, trip_days, interests, season, group, 8)
        if search_text.strip():
            q = search_text.strip().lower()
            all_matches = [
                x for x in all_matches
                if q in x["place"]["name"].lower()
                or q in x["place"]["country"].lower()
                or any(q in t.lower() for t in x["place"]["types"])
            ]
        if not all_matches:
            st.warning("No destinations found. Adjust your preferences or search term.")
        for item in all_matches:
            p = item["place"]
            c1, c2 = st.columns([1.1, 2])
            with c1:
                st.image(p["image"], use_container_width=True)
            with c2:
                st.markdown(f"### {p['emoji']} {p['name']}, {p['country']}")
                st.write(p["description"])
                st.caption(f"Best time: {p['best']} · Suggested duration: {p['days']} days")
                st.markdown(f"**Estimated base budget:** {money(p['budget'])} per person")
                st.progress(item["percent"] / 100, text=f"{item['percent']}% preference match")
                if p["name"] not in st.session_state.saved:
                    if st.button(f"♡ Save {p['name']}", key=f"save_explore_{p['name']}"):
                        st.session_state.saved.append(p["name"])
                        st.rerun()
                else:
                    st.caption("✓ Saved to your trips")
            st.divider()

# ----------------------------- BOOKING PAGE -----------------------------
elif nav == "Booking":
    st.markdown('<div class="section-title">Plan a booking</div>', unsafe_allow_html=True)
    st.info("This student project provides planning estimates only. It does not make real hotel, flight or tour reservations.")
    b1, b2 = st.columns(2)
    with b1:
        booking_place = st.selectbox("Choose destination", [p["name"] for p in DESTINATIONS])
        start_date = st.date_input("Departure date", date.today())
        travellers = st.number_input("Number of travellers", 1, 20, 2)
    with b2:
        booking_days = st.number_input("Number of days", 1, 30, 4)
        booking_type = st.selectbox("Travel category", ["Complete trip", "Hotel stay", "Transport", "Activities"])
        contact_email = st.text_input("Email (optional)")
    selected_place = next(p for p in DESTINATIONS if p["name"] == booking_place)
    approx_total = selected_place["budget"] / selected_place["days"] * booking_days * travellers
    st.metric("Indicative group budget", money(approx_total))
    st.caption("Estimate only. Actual prices depend on dates, availability and booking choices.")
    if st.button("Create sample trip plan", type="primary"):
        st.success(f"Sample plan prepared for {travellers} traveller(s) to {booking_place}, starting {start_date:%d %b %Y}. No booking has been made.")

# ----------------------------- MESSAGES PAGE -----------------------------
elif nav == "Messages":
    st.markdown('<div class="section-title">Messages & travel notes</div>', unsafe_allow_html=True)
    st.info("Use this area to keep notes for your travel plan.")
    note = st.text_area("Write a travel note", placeholder="Example: Check hotel options near the city centre...")
    if st.button("Save note", type="primary"):
        if note.strip():
            st.session_state["travel_note"] = note.strip()
            st.success("Your note is saved for this session.")
    if st.session_state.get("travel_note"):
        st.markdown("**Your saved note**")
        st.write(st.session_state["travel_note"])

# ----------------------------- SUPPORT PAGE -----------------------------
elif nav == "Support":
    st.markdown('<div class="section-title">Travel support</div>', unsafe_allow_html=True)
    with st.expander("How are destinations recommended?"):
        st.write("A rule-based scoring engine compares your budget, duration, interests, season and travel group with destination information.")
    with st.expander("Are the prices live?"):
        st.write("No. Budgets are illustrative estimates stored in the project's knowledge base.")
    with st.expander("Does this website book flights or hotels?"):
        st.write("No. It is a student project prototype for destination advice and trip planning.")
    st.markdown("For emergencies while travelling, contact local emergency services or your travel provider.")

# ----------------------------- SETTINGS PAGE -----------------------------
elif nav == "Settings":
    st.markdown('<div class="section-title">Dashboard settings</div>', unsafe_allow_html=True)
    st.write("Personalise your Traveloo dashboard.")
    dark_choice = st.toggle("Enable dark mode", value=st.session_state.dark_mode, key="settings_dark")
    if dark_choice != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_choice
        st.rerun()
    st.caption("Dark mode changes the dashboard colours. Preferences are kept for the current session.")

st.markdown('<div class="footer">TRAVELOO · TRAVEL DESTINATION ADVISOR · BUILT WITH PYTHON & STREAMLIT</div>', unsafe_allow_html=True)
