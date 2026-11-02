"""
TRAVELWISE - Smart Travel Destination Advisor
A polished rule-based expert system built with Python + Streamlit.

Install:
    py -m pip install --upgrade streamlit pandas

Run:
    py -m streamlit run travelwise_app.py
"""

import html
import pandas as pd
import streamlit as st

# ----------------------------- PAGE CONFIG -----------------------------
st.set_page_config(
    page_title="TravelWise | Find Your Next Escape",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------- DESIGN SYSTEM -----------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@500;600;700;800&display=swap');

    :root {
        --navy: #10283f;
        --teal: #087f78;
        --teal-dark: #06645f;
        --ink: #142b3e;
        --muted: #64788a;
        --line: #e1e9ef;
        --paper: #ffffff;
        --bg: #f3f7fa;
        --sand: #f3eadb;
        --orange: #d98b35;
    }
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp { background: var(--bg); color: var(--ink); }
    .block-container { max-width: 1240px; padding-top: 1.4rem; padding-bottom: 3rem; }
    [data-testid="stSidebar"] { background: #fff; border-right: 1px solid var(--line); }
    [data-testid="stSidebar"] .block-container { padding-top: 1.5rem; }
    #MainMenu, footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent; }
    h1, h2, h3 { color: var(--navy); font-family: 'Manrope', sans-serif; }
    .brand { font-family: 'Manrope', sans-serif; font-weight: 800; font-size: 25px; color: var(--navy); }
    .brand span { color: var(--teal); }
    .hero {
        position: relative; overflow: hidden; border-radius: 26px;
        padding: 42px 44px; margin-bottom: 24px; color: white;
        background: linear-gradient(112deg, #10283f 0%, #14566a 58%, #15958a 100%);
    }
    .hero:after {
        content: "✈"; position: absolute; right: 5%; top: -30px;
        font-size: 190px; opacity: .09; transform: rotate(-15deg);
    }
    .hero-kicker { text-transform: uppercase; letter-spacing: 2.8px; font-size: 11px; font-weight: 800; opacity: .78; }
    .hero h1 { color: white; font-size: clamp(34px, 5vw, 55px); line-height: 1.04; margin: 12px 0 12px; max-width: 650px; }
    .hero p { color: #e4f2f3; font-size: 16px; max-width: 620px; margin: 0; line-height: 1.6; }
    .hero-pill { display: inline-block; margin-top: 22px; padding: 8px 13px; border: 1px solid rgba(255,255,255,.3); border-radius: 30px; color: #fff; font-size: 12px; }
    .metric-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 13px; margin: 18px 0 25px; }
    .metric { background: white; border: 1px solid var(--line); border-radius: 16px; padding: 17px 19px; box-shadow: 0 3px 12px rgba(18,43,62,.035); }
    .metric .value { color: var(--navy); font: 800 26px 'Manrope', sans-serif; }
    .metric .label { color: var(--muted); font-size: 12px; margin-top: 3px; }
    .section-eyebrow { color: var(--teal); text-transform: uppercase; letter-spacing: 1.8px; font-size: 10px; font-weight: 800; }
    .destination-card { display: grid; grid-template-columns: minmax(0, 1fr) 155px; background: white; border: 1px solid var(--line); border-radius: 19px; overflow: hidden; margin: 13px 0 8px; box-shadow: 0 5px 18px rgba(18,43,62,.045); }
    .destination-card.best { border: 1.5px solid var(--orange); box-shadow: 0 0 0 2px rgba(217,139,53,.10); }
    .destination-main { padding: 22px 24px; }
    .rank { color: var(--teal); font-size: 10px; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase; }
    .destination-title { font: 800 25px 'Manrope', sans-serif; color: var(--navy); margin: 5px 0 1px; }
    .destination-state { color: var(--muted); font-size: 13px; margin-bottom: 10px; }
    .destination-desc { color: #42596b; font-size: 14px; margin: 0 0 12px; }
    .tag { display: inline-block; border-radius: 30px; padding: 5px 10px; margin: 0 5px 6px 0; background: #f1f6f8; border: 1px solid #e1e9ed; color: #355366; font-size: 11px; font-weight: 700; }
    .tag.match { background: #e6f5f2; border-color: #c6e8e1; color: #08766e; }
    .tag.warning { background: #fff5e8; border-color: #f2d7b4; color: #a75b0c; }
    .detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 11px 20px; margin-top: 10px; }
    .detail-label { display: block; color: #8494a2; font-size: 10px; text-transform: uppercase; letter-spacing: 1px; font-weight: 800; margin-bottom: 3px; }
    .detail-value { color: #294256; font-size: 13px; line-height: 1.45; }
    .match-panel { background: var(--navy); color: white; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 18px 10px; border-left: 2px dashed #78909e; text-align: center; }
    .match-score { font: 800 44px 'Manrope', sans-serif; line-height: 1.1; color: #fff; }
    .match-caption { color: #c6d5df; font-size: 11px; }
    .estimate { color: #fff; font: 800 18px 'Manrope', sans-serif; margin-top: 17px; }
    .card-note { color: #c6d5df; font-size: 10px; }
    .info-panel { background: white; border: 1px solid var(--line); border-radius: 16px; padding: 19px; height: 100%; }
    .info-panel h3 { font-size: 16px; margin: 0 0 8px; }
    .info-panel p { color: var(--muted); font-size: 13px; margin: 0; line-height: 1.5; }
    div.stButton > button, div.stDownloadButton > button { border-radius: 10px; font-weight: 700; border: 0; }
    div.stButton > button[kind="primary"] { background: var(--teal); }
    div.stButton > button[kind="primary"]:hover { background: var(--teal-dark); }
    div[data-testid="stTabs"] button { font-weight: 700; }
    .footer-note { color: #8494a2; font-size: 11px; text-align: center; margin-top: 30px; }
    @media(max-width: 760px) {
        .metric-grid { grid-template-columns: repeat(2, 1fr); }
        .destination-card { grid-template-columns: 1fr; }
        .match-panel { border-left: 0; border-top: 2px dashed #78909e; }
        .detail-grid { grid-template-columns: 1fr; }
        .hero { padding: 30px 25px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------- DESTINATION KNOWLEDGE BASE -----------------------------
# Budgets are approximate estimates per person for the suggested trip length.
RAW_DESTINATIONS = [
    ("Rishikesh", "Uttarakhand", 7000, 3, ["Adventure", "Nature", "Spiritual"], ["Winter", "Summer"], "Sep-Nov, Feb-May", ["River rafting", "Ganga Aarti", "Laxman Jhula cafes", "Yoga session"], "Road or train via Haridwar", "🏞️", "A riverside escape with rafting, quiet ghats and mountain views."),
    ("Jaipur", "Rajasthan", 9000, 3, ["Culture", "History", "Family"], ["Winter"], "October-March", ["Amber Fort", "City Palace", "Hawa Mahal", "Bapu Bazaar"], "Road, train or flight", "🏰", "Pink-city forts, palaces, bazaars and rich food."),
    ("Manali", "Himachal Pradesh", 14000, 5, ["Adventure", "Nature", "Romantic"], ["Winter", "Summer"], "Mar-Jun; Dec-Feb for snow", ["Solang Valley", "Old Manali", "Hadimba Temple", "Atal Tunnel"], "Road or overnight bus", "🏔️", "Himalayan scenery with treks, snow experiences and cafe-lined lanes."),
    ("Udaipur", "Rajasthan", 12000, 3, ["Romantic", "Culture", "Family"], ["Winter"], "October-March", ["City Palace", "Lake Pichola boat ride", "Sajjangarh sunset", "Old city walk"], "Train, road or flight", "🛶", "A lake city of palaces, heritage hotels and beautiful sunsets."),
    ("Goa", "Goa", 18000, 5, ["Beach", "Adventure", "Nightlife", "Family"], ["Winter", "Summer"], "November-February", ["North Goa beaches", "Water sports", "Old Goa churches", "Fort Aguada"], "Flight, train or road", "🏖️", "Beaches, food, nightlife and water sports."),
    ("Mussoorie", "Uttarakhand", 10000, 3, ["Nature", "Family", "Romantic"], ["Summer", "Winter"], "Mar-Jun, Sep-Nov", ["Mall Road", "Gun Hill", "Kempty Falls", "Lal Tibba"], "Train to Dehradun, then taxi", "🌲", "An easy hill-station break with viewpoints and walking routes."),
    ("Amritsar", "Punjab", 8000, 2, ["Culture", "History", "Family", "Spiritual"], ["Winter"], "October-March", ["Golden Temple", "Jallianwala Bagh", "Wagah-Attari ceremony", "Local food trail"], "Train, road or flight", "🕌", "Heritage, hospitality and memorable Punjabi food."),
    ("Srinagar", "Jammu and Kashmir", 22000, 5, ["Nature", "Romantic", "Family"], ["Summer", "Winter"], "April-October; winter for snow", ["Dal Lake shikara", "Mughal Gardens", "Houseboat stay", "Gulmarg day trip"], "Flight or road", "🌊", "Lakes, gardens and beautiful Himalayan landscapes."),
    ("Varanasi", "Uttar Pradesh", 9000, 3, ["Spiritual", "Culture", "History"], ["Winter"], "October-March", ["Ganga Aarti", "Sunrise boat ride", "Sarnath", "Old-city food walk"], "Train, road or flight", "🪔", "An ancient spiritual city on the banks of the Ganga."),
    ("Darjeeling", "West Bengal", 19000, 5, ["Nature", "Family", "Romantic"], ["Summer", "Winter"], "Mar-May, Oct-Nov", ["Toy train", "Tiger Hill sunrise", "Tea garden visit", "Monasteries"], "Flight or train to Bagdogra/NJP, then road", "🚂", "Tea gardens, mountain views and a heritage railway."),
    ("Pondicherry", "Puducherry", 15000, 4, ["Beach", "Culture", "Romantic"], ["Winter"], "November-February", ["Promenade walk", "French Quarter", "Auroville", "Cafe trail"], "Flight to Chennai, then road", "🚲", "French-style streets, cafes and calm beaches."),
    ("Nainital", "Uttarakhand", 11000, 3, ["Nature", "Family", "Romantic"], ["Summer", "Winter"], "Mar-Jun, Sep-Nov", ["Naini Lake boating", "Snow View ropeway", "Mall Road", "Bhimtal"], "Train to Kathgodam, then road", "⛰️", "A lake town for short family and couples' getaways."),
    ("Jaisalmer", "Rajasthan", 13000, 3, ["Culture", "History", "Adventure"], ["Winter"], "October-February", ["Jaisalmer Fort", "Sam dunes camel safari", "Patwon Ki Haveli", "Desert camp"], "Train, road or flight", "🐪", "A golden fort city with desert camps under the stars."),
    ("Alleppey", "Kerala", 20000, 5, ["Nature", "Romantic", "Family"], ["Winter", "Monsoon"], "September-March", ["Houseboat cruise", "Marari beach", "Kumarakom birding", "Backwater village"], "Flight to Kochi, then road", "🛥️", "Slow backwater cruises, houseboats and coconut groves."),
    ("Kasol", "Himachal Pradesh", 9500, 4, ["Adventure", "Nature"], ["Summer", "Winter"], "Mar-Jun, Sep-Nov", ["Kheerganga trek", "Manikaran hot springs", "Tosh village", "Riverside cafes"], "Bus to Bhuntar, then taxi", "⛺", "A riverside valley for trekkers and backpackers."),
    ("Kochi", "Kerala", 16000, 4, ["Culture", "History", "Beach", "Nature"], ["Winter", "Monsoon"], "October-March", ["Fort Kochi walk", "Chinese fishing nets", "Kathakali show", "Mattancherry"], "Flight, train or road", "🎭", "Colonial lanes, art, seafood and harbour views."),
]

FIELDS = ["name", "state", "budget", "days", "types", "seasons", "best", "activities", "transport", "emoji", "description"]
DESTINATIONS = [dict(zip(FIELDS, row)) for row in RAW_DESTINATIONS]
INTERESTS = ["Nature", "Adventure", "Beach", "Culture", "History", "Spiritual", "Romantic", "Nightlife", "Family"]
STAY_MULTIPLIER = {"Budget": 0.85, "Comfort": 1.0, "Premium": 1.35}
COST_SPLIT = {"Stay": 0.35, "Food": 0.20, "Transport": 0.25, "Activities": 0.15, "Other": 0.05}


def money(value):
    return f"₹{round(value):,}"


def estimate_trip(place, days, stay_style):
    total = (place["budget"] / place["days"]) * days * STAY_MULTIPLIER[stay_style]
    breakdown = {key: total * fraction for key, fraction in COST_SPLIT.items()}
    return total, breakdown


# ----------------------------- EXPERT SYSTEM / RULE ENGINE -----------------------------
def evaluate_destination(place, budget, trip_days, interests, season, traveller):
    score = 0
    reasons = []
    warnings = []

    # Rule 1: budget compatibility
    if place["budget"] <= budget:
        score += 3
        reasons.append("fits your budget")
    elif place["budget"] <= budget * 1.20:
        score += 1
        warnings.append("slightly above budget")
    else:
        score -= 3
        warnings.append("above budget")

    # Rule 2: trip duration
    day_gap = abs(place["days"] - trip_days)
    if day_gap == 0:
        score += 2
        reasons.append("matches your trip length")
    elif day_gap <= 2:
        score += 1
        reasons.append("duration is close to your plan")

    # Rule 3: interests
    matched = [item for item in place["types"] if item in interests]
    score += 3 * len(matched)
    if matched:
        reasons.append("interests: " + ", ".join(matched))

    # Rule 4: season
    if season in place["seasons"]:
        score += 2
        reasons.append(f"good option for {season.lower()}")
    else:
        warnings.append(f"season may not be ideal ({season.lower()})")

    # Rule 5: traveller group
    types = place["types"]
    group_bonus = 0
    if traveller == "Family" and "Family" in types:
        group_bonus = 2
    elif traveller == "Couple" and "Romantic" in types:
        group_bonus = 2
    elif traveller == "Friends" and any(x in types for x in ["Adventure", "Beach", "Nightlife"]):
        group_bonus = 2
    elif traveller == "Solo" and any(x in types for x in ["Adventure", "Culture", "Nature"]):
        group_bonus = 1
    if group_bonus:
        score += group_bonus
        reasons.append(f"suits {traveller.lower()} travel")

    # Convert score to an easy-to-read relative match indicator.
    max_score = 7 + (3 * max(1, len(interests))) + 2
    match_percent = max(1, min(100, round((score / max_score) * 100)))
    return {
        "place": place,
        "score": score,
        "match": match_percent,
        "reasons": reasons,
        "warnings": warnings,
    }


def get_recommendations(budget, trip_days, interests, season, traveller, count):
    evaluated = [
        evaluate_destination(p, budget, trip_days, interests, season, traveller)
        for p in DESTINATIONS
    ]
    evaluated = [item for item in evaluated if item["score"] > 0]
    evaluated.sort(key=lambda item: item["score"], reverse=True)
    return evaluated[:count]


def render_destination_card(result, rank, days, stay_style, interests):
    place = result["place"]
    total, _ = estimate_trip(place, days, stay_style)
    tags = "".join(
        f'<span class="tag {"match" if tag in interests else ""}">{html.escape(tag)}</span>'
        for tag in place["types"]
    )
    warnings = "".join(
        f'<span class="tag warning">{html.escape(warning)}</span>'
        for warning in result["warnings"]
    )
    reasons = html.escape("; ".join(result["reasons"]) or "Some preferences match")
    return f"""
    <div class="destination-card {'best' if rank == 1 else ''}">
      <div class="destination-main">
        <div class="rank">{"★ Best match" if rank == 1 else f"Destination match #{rank}"}</div>
        <div class="destination-title">{place['emoji']} {html.escape(place['name'])}</div>
        <div class="destination-state">{html.escape(place['state'])} · Suggested stay: {place['days']} days</div>
        <p class="destination-desc">{html.escape(place['description'])}</p>
        <div>{tags}{warnings}</div>
        <div class="detail-grid">
          <div><span class="detail-label">Best time to visit</span><span class="detail-value">{html.escape(place['best'])}</span></div>
          <div><span class="detail-label">How to reach</span><span class="detail-value">{html.escape(place['transport'])}</span></div>
          <div><span class="detail-label">Popular activities</span><span class="detail-value">{html.escape(', '.join(place['activities'][:3]))}</span></div>
          <div><span class="detail-label">Why recommended</span><span class="detail-value">{reasons}</span></div>
        </div>
      </div>
      <div class="match-panel">
        <div class="match-score">{result['match']}%</div>
        <div class="match-caption">preference match</div>
        <div class="estimate">{money(total)}</div>
        <div class="card-note">estimated / person</div>
      </div>
    </div>
    """


# ----------------------------- SESSION STATE -----------------------------
if "saved_destinations" not in st.session_state:
    st.session_state.saved_destinations = []


# ----------------------------- SIDEBAR -----------------------------
with st.sidebar:
    st.markdown('<div class="brand">✈️ Travel<span>Wise</span></div>', unsafe_allow_html=True)
    st.caption("YOUR PERSONAL DESTINATION ADVISOR")
    st.divider()

    st.markdown("### Build your trip")
    budget = st.slider("Budget per person", 5000, 50000, 15000, 1000, format="₹%d")
    trip_days = st.slider("Trip duration", 2, 10, 4, 1, format="%d days")
    season = st.selectbox("When are you travelling?", ["Winter", "Summer", "Monsoon"])
    traveller = st.selectbox("Who is travelling?", ["Friends", "Family", "Couple", "Solo"])
    interests = st.multiselect("What do you enjoy?", INTERESTS, default=["Nature", "Adventure"])
    stay_style = st.selectbox("Preferred stay style", ["Budget", "Comfort", "Premium"], index=1)
    result_count = st.slider("Number of recommendations", 3, 8, 5)
    sort_option = st.selectbox("Sort recommendations by", ["Best match", "Lowest estimated cost", "Shortest suggested trip"])
    st.divider()
    st.caption("Travel estimates are indicative and are not live booking prices.")


# ----------------------------- MAIN HEADER -----------------------------
st.markdown(
    """
    <div class="hero">
      <div class="hero-kicker">Explore India · Travel smarter</div>
      <h1>Where should you go next?</h1>
      <p>Tell us what you love, what you want to spend and when you want to travel.
      We'll find destinations that fit your style.</p>
      <span class="hero-pill">✦ PERSONALIZED RECOMMENDATIONS &nbsp; · &nbsp; RULE-BASED EXPERT SYSTEM</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# Current matches for dashboard metrics and tabs.
recommendations = get_recommendations(
    budget, trip_days, interests, season, traveller, result_count
) if interests else []

# Apply optional sorting without changing the scoring engine.
if sort_option == "Lowest estimated cost":
    recommendations.sort(key=lambda item: estimate_trip(item["place"], trip_days, stay_style)[0])
elif sort_option == "Shortest suggested trip":
    recommendations.sort(key=lambda item: item["place"]["days"])

st.markdown(
    f"""
    <div class="metric-grid">
      <div class="metric"><div class="value">{len(DESTINATIONS)}</div><div class="label">Destinations in knowledge base</div></div>
      <div class="metric"><div class="value">{money(budget)}</div><div class="label">Your travel budget</div></div>
      <div class="metric"><div class="value">{trip_days} days</div><div class="label">Your planned duration</div></div>
      <div class="metric"><div class="value">{len(st.session_state.saved_destinations)}</div><div class="label">Saved destinations</div></div>
    </div>
    """,
    unsafe_allow_html=True,
)

tab_matches, tab_compare, tab_saved, tab_about = st.tabs(
    ["✦ Recommended for you", "⇄ Compare destinations", "♡ Saved trips", "ⓘ How it works"]
)

# ----------------------------- MATCHES TAB -----------------------------
with tab_matches:
    st.markdown('<div class="section-eyebrow">Your shortlist</div>', unsafe_allow_html=True)
    st.subheader("Destinations picked for your travel style")

    if not interests:
        st.info("Choose at least one interest in the sidebar to generate recommendations.")
    elif not recommendations:
        st.warning("No strong matches were found. Try increasing your budget or changing your travel preferences.")
    else:
        st.caption(f"Showing {len(recommendations)} recommendations based on your selected preferences.")
        for rank, result in enumerate(recommendations, start=1):
            place = result["place"]
            st.markdown(
                render_destination_card(result, rank, trip_days, stay_style, interests),
                unsafe_allow_html=True,
            )
            save_col, details_col = st.columns([1, 5])
            with save_col:
                already_saved = place["name"] in st.session_state.saved_destinations
                if st.button(
                    "✓ Saved" if already_saved else "♡ Save trip",
                    key=f"save_{place['name']}",
                    disabled=already_saved,
                    use_container_width=True,
                ):
                    st.session_state.saved_destinations.append(place["name"])
                    st.rerun()
            with details_col:
                with st.expander(f"View estimated cost breakdown and {trip_days}-day outline"):
                    total, breakdown = estimate_trip(place, trip_days, stay_style)
                    metric_col1, metric_col2 = st.columns(2)
                    metric_col1.metric("Estimated total per person", money(total))
                    metric_col2.metric("Compared with your budget", money(budget - total), delta=money(budget - total))
                    breakdown_df = pd.DataFrame(
                        {"Estimated amount (₹)": breakdown}
                    )
                    st.bar_chart(breakdown_df)
                    st.caption("Illustrative cost split: stay 35%, food 20%, transport 25%, activities 15%, other 5%.")
                    st.markdown("**Suggested activity outline**")
                    for day in range(trip_days):
                        first_activity = place["activities"][(day * 2) % len(place["activities"])]
                        second_activity = place["activities"][(day * 2 + 1) % len(place["activities"])]
                        st.write(f"**Day {day + 1}:** {first_activity} and {second_activity}")

        export_rows = []
        for rank, item in enumerate(recommendations, 1):
            p = item["place"]
            estimated, _ = estimate_trip(p, trip_days, stay_style)
            export_rows.append({
                "Rank": rank,
                "Destination": p["name"],
                "State": p["state"],
                "Match percentage": item["match"],
                "Estimated cost per person (INR)": round(estimated),
                "Best time": p["best"],
                "Suggested days": p["days"],
            })
        export_df = pd.DataFrame(export_rows)
        st.download_button(
            "⬇ Download recommendations as CSV",
            data=export_df.to_csv(index=False).encode("utf-8"),
            file_name="travelwise_recommendations.csv",
            mime="text/csv",
        )

    st.markdown(
        '<div class="footer-note">Estimates are approximate planning guides. Confirm current transport, accommodation, weather and local conditions before booking.</div>',
        unsafe_allow_html=True,
    )

# ----------------------------- COMPARE TAB -----------------------------
with tab_compare:
    st.markdown('<div class="section-eyebrow">Side-by-side view</div>', unsafe_allow_html=True)
    st.subheader("Compare destinations before you decide")
    all_names = [p["name"] for p in DESTINATIONS]
    selected_names = st.multiselect(
        "Select two to four destinations",
        all_names,
        default=["Jaipur", "Goa"],
        max_selections=4,
    )
    if len(selected_names) < 2:
        st.info("Select at least two destinations to compare.")
    else:
        selected_places = [next(p for p in DESTINATIONS if p["name"] == name) for name in selected_names]
        compare_data = []
        for p in selected_places:
            estimate, _ = estimate_trip(p, trip_days, stay_style)
            compare_data.append({
                "Destination": p["name"],
                "State": p["state"],
                "Estimated cost": money(estimate),
                "Suggested days": p["days"],
                "Best season": ", ".join(p["seasons"]),
                "Travel style": ", ".join(p["types"]),
                "How to reach": p["transport"],
            })
        st.dataframe(pd.DataFrame(compare_data), use_container_width=True, hide_index=True)
        cost_chart = pd.DataFrame(
            {"Estimated cost (₹)": [estimate_trip(p, trip_days, stay_style)[0] for p in selected_places]},
            index=[p["name"] for p in selected_places],
        )
        st.markdown("#### Estimated trip cost comparison")
        st.bar_chart(cost_chart)

# ----------------------------- SAVED TAB -----------------------------
with tab_saved:
    st.markdown('<div class="section-eyebrow">Your personal shortlist</div>', unsafe_allow_html=True)
    st.subheader("Saved destinations")
    if not st.session_state.saved_destinations:
        st.info("You haven't saved any destinations yet. Go to Recommended for you and select Save trip.")
    else:
        saved_rows = []
        for name in list(st.session_state.saved_destinations):
            place = next(p for p in DESTINATIONS if p["name"] == name)
            left, right = st.columns([5, 1])
            left.markdown(f"**{place['emoji']} {place['name']}**, {place['state']} · Approx. {money(place['budget'])} for {place['days']} days")
            if right.button("Remove", key=f"remove_{name}"):
                st.session_state.saved_destinations.remove(name)
                st.rerun()
            saved_rows.append({"Destination": place["name"], "State": place["state"], "Approx. budget (INR)": place["budget"], "Best time": place["best"]})
        st.download_button(
            "⬇ Download saved destinations",
            data=pd.DataFrame(saved_rows).to_csv(index=False).encode("utf-8"),
            file_name="travelwise_saved_destinations.csv",
            mime="text/csv",
        )

# ----------------------------- ABOUT TAB -----------------------------
with tab_about:
    st.markdown('<div class="section-eyebrow">Behind the recommendations</div>', unsafe_allow_html=True)
    st.subheader("How TravelWise makes a recommendation")
    columns = st.columns(4)
    stages = [
        ("01 · INPUT", "The user selects budget, trip length, season, travel group, interests and stay style."),
        ("02 · KNOWLEDGE BASE", "The system stores destination budgets, trip durations, seasons, activities and transport details."),
        ("03 · RULE ENGINE", "IF–THEN rules compare the user's choices with each destination and calculate a score."),
        ("04 · OUTPUT", "The system ranks destinations and explains why each one matches the user's preferences."),
    ]
    for column, (heading, description) in zip(columns, stages):
        with column:
            st.markdown(f'<div class="info-panel"><div class="section-eyebrow">{heading}</div><p style="margin-top:10px">{description}</p></div>', unsafe_allow_html=True)

    st.markdown("#### Example rules used by the expert system")
    st.code(
        """
IF destination budget is within the user's budget:
    Add 3 points
ELSE IF destination budget is within 20% above the user's budget:
    Add 1 point
ELSE:
    Subtract 3 points

IF destination duration matches the user's trip duration:
    Add 2 points

IF a destination type matches a selected interest:
    Add 3 points for each matching interest

IF the destination is suitable for the selected season:
    Add 2 points

IF destination type matches the travelling group:
    Add a group suitability bonus

Finally:
    Rank destinations by total score
    Display the top recommendations
        """,
        language="text",
    )
    st.caption("This is a rule-based expert system. It does not train a machine-learning model or use live booking data.")

# ----------------------------- FOOTER -----------------------------
st.markdown(
    '<div class="footer-note">TRAVELWISE · STUDENT EXPERT SYSTEM PROJECT · BUILT WITH PYTHON & STREAMLIT</div>',
    unsafe_allow_html=True,
)
