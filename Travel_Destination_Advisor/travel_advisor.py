import html
import pandas as pd
import streamlit as st

st.set_page_config(page_title="TravelWise | Destination Advisor", page_icon="✈️", layout="wide")

# ----------------------------------------------------------------------------
# Styling
# ----------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,600;9..144,700&display=swap');
:root{--ink:#10283a;--sea:#0e7c86;--sea-dark:#0a5d65;--mist:#eef3f6;--line:#dbe4ea;--gold:#f0a81c;--muted:#5d7080;}
html, body, [class*="css"]{font-family:'Plus Jakarta Sans',sans-serif;}
.stApp{background:var(--mist);}
#MainMenu, footer{visibility:hidden;}
section[data-testid="stSidebar"]{background:#fff;border-right:1px solid var(--line);}
.hero{padding:38px 40px;border-radius:20px;color:#fff;margin-bottom:22px;
  background:linear-gradient(120deg,#10283a 0%,#0e5f6e 60%,#0e7c86 100%);}
.hero h1{font-family:'Fraunces',serif;font-size:42px;font-weight:700;margin:0 0 8px 0;color:#fff;}
.hero p{font-size:16px;opacity:.9;margin:0;max-width:640px;}
.kpi{background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px 18px;}
.kpi b{display:block;font-size:24px;color:var(--ink);font-family:'Fraunces',serif;}
.kpi span{font-size:13px;color:var(--muted);}
.card{background:#fff;border:1px solid var(--line);border-radius:14px;padding:22px;margin:14px 0 6px 0;}
.card.top{border-left:6px solid var(--gold);}
.rank{font-size:13px;color:var(--muted);font-weight:600;}
.dest{font-family:'Fraunces',serif;font-size:26px;font-weight:700;color:var(--ink);margin:2px 0 6px 0;}
.pct{float:right;text-align:center;background:var(--ink);color:#fff;border-radius:10px;padding:8px 14px;}
.pct b{font-size:22px;display:block;line-height:1.1;}
.pct span{font-size:11px;opacity:.8;}
.tag{display:inline-block;background:#e3f2f3;color:var(--sea-dark);padding:4px 11px;border-radius:6px;font-size:12px;font-weight:600;margin:2px 4px 2px 0;}
.tag.warn{background:#fdf0d5;color:#8a5a00;}
.fact{font-size:14px;color:#2b3f4e;margin:6px 0;}
.fact b{color:var(--ink);}
.muted{color:var(--muted);font-size:13px;}
.bar{height:8px;border-radius:6px;background:#e5ecf0;overflow:hidden;margin:3px 0 9px 0;}
.bar div{height:100%;background:var(--sea);}
div.stButton>button, div.stDownloadButton>button{background:var(--sea);color:#fff;border:0;border-radius:10px;font-weight:700;padding:.55rem 1rem;}
div.stButton>button:hover, div.stDownloadButton>button:hover{background:var(--sea-dark);color:#fff;}
button[data-baseweb="tab"]{font-weight:600;}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# Knowledge base (approximate budget per person in INR for the suggested days)
# ----------------------------------------------------------------------------
def D(name, budget, days, types, seasons, best, acts, transport, emoji, desc, lat, lon, tip):
    return dict(name=name, budget=budget, days=days, types=types, seasons=seasons, best=best,
                activities=acts, transport=transport, emoji=emoji, description=desc,
                lat=lat, lon=lon, tip=tip)

DESTINATIONS = [
    D("Rishikesh, Uttarakhand", 7000, 3, ["Adventure","Nature","Spiritual"], ["Winter","Summer"],
      "September-November and February-May",
      ["River rafting","Ganga Aarti at Triveni Ghat","Cafe hopping at Laxman Jhula","Yoga session","Short trek to Neer Garh waterfall"],
      "Road or train via Haridwar", "🏞️", "Riverside escape with adventure, peaceful ghats and mountain views.", 30.0869, 78.2676,
      "Rafting is closed during peak monsoon, so check operator status."),
    D("Jaipur, Rajasthan", 9000, 3, ["Culture","History","Family"], ["Winter"],
      "October-March",
      ["Amber Fort","City Palace and Jantar Mantar","Hawa Mahal","Bapu Bazaar shopping","Nahargarh sunset"],
      "Road, train or flight", "🏰", "Colourful heritage city known for forts, architecture, shopping and food.", 26.9124, 75.7873,
      "Start forts early to beat heat and crowds."),
    D("Manali, Himachal Pradesh", 14000, 5, ["Adventure","Nature","Romantic"], ["Winter","Summer"],
      "March-June; December-February for snow",
      ["Solang Valley activities","Old Manali cafes","Hadimba Temple","Atal Tunnel and Sissu","Jogini Waterfall walk"],
      "Road or overnight bus; nearest airport is Bhuntar", "🏔️", "Himalayan getaway for mountain scenery and outdoor activities.", 32.2396, 77.1887,
      "Winter roads can close, so check conditions before leaving."),
    D("Udaipur, Rajasthan", 12000, 3, ["Romantic","Culture","Family"], ["Winter"],
      "October-March",
      ["City Palace","Lake Pichola boat ride","Jagdish Temple and old city","Sajjangarh sunset","Local thali dinner"],
      "Train, road or flight", "🛶", "Relaxed lake city with palaces, heritage hotels and sunset views.", 24.5854, 73.7125,
      "Book lakeside dinners in advance for weekends."),
    D("Goa", 18000, 5, ["Beach","Adventure","Nightlife","Family"], ["Winter","Summer"],
      "November-February",
      ["North Goa beaches","Water sports at Baga","Old Goa churches","Fort Aguada","South Goa quiet beaches"],
      "Flight, train or road", "🏖️", "Beach destination with relaxation, food, nightlife and water activities.", 15.2993, 74.1240,
      "Rent a scooter for flexibility, but carry a valid licence."),
    D("Mussoorie, Uttarakhand", 10000, 3, ["Nature","Family","Romantic"], ["Summer","Winter"],
      "March-June and September-November",
      ["Mall Road","Gun Hill","Kempty Falls","Camel's Back Road walk","Lal Tibba viewpoint"],
      "Road or train to Dehradun, then taxi", "🌲", "Hill station with viewpoints, cafes and scenic walking routes.", 30.4598, 78.0644,
      "Weekends are crowded; midweek is calmer."),
    D("Amritsar, Punjab", 8000, 2, ["Culture","History","Family","Spiritual"], ["Winter"],
      "October-March",
      ["Golden Temple","Jallianwala Bagh","Wagah-Attari ceremony","Kulcha and lassi trail"],
      "Train, road or flight", "🕌", "Cultural destination known for heritage, hospitality and food.", 31.6340, 74.8723,
      "Visit the Golden Temple early morning or late night."),
    D("Srinagar, Jammu and Kashmir", 22000, 5, ["Nature","Romantic","Family"], ["Summer","Winter"],
      "April-October; winter for snow scenery",
      ["Dal Lake shikara ride","Mughal Gardens","Houseboat stay","Gulmarg day trip","Pahalgam excursion"],
      "Flight or road", "🌊", "Scenic valley with lakes, gardens and Himalayan landscapes.", 34.0837, 74.7973,
      "Check current travel advisories before booking."),
    D("Varanasi, Uttar Pradesh", 9000, 3, ["Spiritual","Culture","History"], ["Winter"],
      "October-March",
      ["Ganga Aarti at Dashashwamedh","Sunrise boat ride","Kashi Vishwanath area","Sarnath","Old-city food walk"],
      "Train, road or flight", "🪔", "Heritage and spiritual city on the banks of the Ganga.", 25.3176, 82.9739,
      "Use a licensed guide for the old-city lanes."),
    D("Darjeeling, West Bengal", 19000, 5, ["Nature","Family","Romantic"], ["Summer","Winter"],
      "March-May and October-November",
      ["Toy train ride","Tiger Hill sunrise","Tea garden visit","Monasteries","Batasia Loop"],
      "Flight or train to Bagdogra/NJP, then road", "🚂", "Hill town known for tea gardens, mountain views and its heritage railway.", 27.0410, 88.2663,
      "Book the toy train joyride ahead."),
    D("Pondicherry", 15000, 4, ["Beach","Culture","Romantic"], ["Winter"],
      "November-February",
      ["Promenade walk","French Quarter","Auroville","Paradise Beach","Cafe trail"],
      "Flight to Chennai, then road; train and bus options", "🚲", "Relaxed coastal town with French-inspired streets and cafes.", 11.9416, 79.8083,
      "Rent a cycle to explore the French Quarter."),
    D("Nainital, Uttarakhand", 11000, 3, ["Nature","Family","Romantic"], ["Summer","Winter"],
      "March-June and September-November",
      ["Naini Lake boating","Snow View ropeway","Mall Road","Bhimtal and Sattal lakes"],
      "Train to Kathgodam, then road", "⛰️", "Popular lake town suited to short family and couples' holidays.", 29.3919, 79.4542,
      "Avoid peak-summer weekends for fewer queues."),
    D("Jaisalmer, Rajasthan", 13000, 3, ["Culture","History","Adventure"], ["Winter"],
      "October-February",
      ["Jaisalmer Fort","Sam sand dunes camel safari","Patwon Ki Haveli","Gadisar Lake","Desert camp evening"],
      "Train, road or flight", "🐪", "Golden desert city with a living fort and star-lit dune camps.", 26.9157, 70.9083,
      "Pack warm layers; desert nights get cold in winter."),
    D("Kerala Backwaters (Alleppey)", 20000, 5, ["Nature","Romantic","Family"], ["Winter","Monsoon"],
      "September-March",
      ["Houseboat cruise","Marari beach","Kumarakom bird sanctuary","Ayurvedic spa","Kathakali show"],
      "Flight to Kochi, then road", "🛶", "Calm backwaters, coconut groves and slow houseboat journeys.", 9.4981, 76.3388,
      "Choose a shared houseboat to cut costs."),
    D("Kasol and Parvati Valley", 9500, 4, ["Adventure","Nature"], ["Summer","Winter"],
      "March-June and September-November",
      ["Kheerganga trek","Cafe hopping","Manikaran hot springs","Tosh village walk"],
      "Overnight bus to Bhuntar, then taxi", "⛺", "Riverside valley loved by trekkers and backpackers.", 32.0100, 77.3150,
      "Respect local rules and keep the valley clean."),
]

INTERESTS = ["Nature","Adventure","Beach","Culture","History","Spiritual","Romantic","Nightlife","Family"]
STYLE_MULT = {"Budget": 0.85, "Comfort": 1.0, "Premium": 1.35}
SPLIT = {"Stay": .35, "Food": .20, "Transport": .25, "Activities": .15, "Miscellaneous": .05}

# ----------------------------------------------------------------------------
# Rule engine
# ----------------------------------------------------------------------------
def recommend(budget, days, interests, season, traveller, top_n):
    out = []
    max_score = 3 + 2 + 3 * len(interests) + 2 + 2
    for p in DESTINATIONS:
        b = {"Budget": 0, "Duration": 0, "Interests": 0, "Season": 0, "Traveller": 0}
        why, warn = [], []

        if p["budget"] <= budget:
            b["Budget"] = 3; why.append("fits your budget")
        elif p["budget"] <= budget * 1.2:
            b["Budget"] = 1; warn.append("slightly above budget")
        else:
            b["Budget"] = -3; warn.append("over budget")

        gap = abs(p["days"] - days)
        if gap == 0:
            b["Duration"] = 2; why.append("ideal trip length")
        elif gap <= 2:
            b["Duration"] = 1

        hit = sorted(set(interests) & set(p["types"]))
        b["Interests"] = 3 * len(hit)
        if hit:
            why.append("matches " + ", ".join(hit))

        if season in p["seasons"]:
            b["Season"] = 2; why.append(f"good in {season.lower()}")
        else:
            warn.append(f"not ideal in {season.lower()}")

        t = p["types"]
        if (traveller == "Family" and "Family" in t) or (traveller == "Couple" and "Romantic" in t) \
           or (traveller == "Friends" and any(x in t for x in ["Adventure","Beach","Nightlife"])):
            b["Traveller"] = 2
        elif traveller == "Solo" and any(x in t for x in ["Adventure","Culture","Nature"]):
            b["Traveller"] = 1
        if b["Traveller"]:
            why.append(f"suits {traveller.lower()} travel")

        score = sum(b.values())
        if score > 0:
            out.append(dict(score=score, pct=max(1, min(100, round(score / max_score * 100))),
                            place=p, breakdown=b, why=why, warn=warn))
    out.sort(key=lambda r: r["score"], reverse=True)
    return out[:top_n]

def cost_estimate(place, days, style):
    per_day = place["budget"] / place["days"]
    total = per_day * days * STYLE_MULT[style]
    return {k: round(total * v, -1) for k, v in SPLIT.items()}

def itinerary(place, days):
    acts = place["activities"]
    plan = []
    for d in range(days):
        picks = [acts[(d * 2 + i) % len(acts)] for i in range(2)]
        plan.append((f"Day {d + 1}", picks[0] if picks[0] != picks[1] else picks[0], picks[1]))
    return plan

# ----------------------------------------------------------------------------
# Session state
# ----------------------------------------------------------------------------
st.session_state.setdefault("shortlist", [])
st.session_state.setdefault("results", None)

# ----------------------------------------------------------------------------
# Sidebar inputs
# ----------------------------------------------------------------------------
with st.sidebar:
    st.header("🧳 Plan your trip")
    budget = st.slider("Budget per person (₹)", 5000, 50000, 15000, 1000)
    days = st.select_slider("Trip length", [2, 3, 4, 5, 6, 7, 10], value=4, format_func=lambda x: f"{x} days")
    season = st.selectbox("Travel season", ["Winter", "Summer", "Monsoon"])
    traveller = st.selectbox("Travelling with", ["Friends", "Family", "Couple", "Solo"])
    interests = st.multiselect("Interests", INTERESTS, default=["Nature", "Adventure"])
    style = st.radio("Stay style", list(STYLE_MULT), index=1, horizontal=True)
    top_n = st.slider("Number of results", 3, 8, 5)
    go = st.button("Find my destinations", use_container_width=True)
    st.caption("Select several interests for sharper matches.")

if go:
    if not interests:
        st.sidebar.warning("Pick at least one interest.")
    else:
        st.session_state.results = recommend(budget, days, interests, season, traveller, top_n)
        st.session_state.query = dict(budget=budget, days=days, season=season, traveller=traveller, style=style)

# ----------------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------------
st.markdown("""
<div class="hero">
  <h1>Find your next escape ✈️</h1>
  <p>Tell us your budget, season and interests. TravelWise ranks destinations across India, explains each match and estimates what your trip will cost.</p>
</div>
""", unsafe_allow_html=True)

k = st.columns(4)
for col, (val, lab) in zip(k, [(len(DESTINATIONS), "Destinations in database"),
                               (f"₹{budget:,}", "Your budget per person"),
                               (f"{days} days", "Trip length"),
                               (len(st.session_state.shortlist), "Saved to shortlist")]):
    col.markdown(f'<div class="kpi"><b>{val}</b><span>{lab}</span></div>', unsafe_allow_html=True)

tab_rec, tab_plan, tab_cmp, tab_map, tab_short, tab_about = st.tabs(
    ["Matches", "Trip planner", "Compare", "Map", "Shortlist", "How it works"])

results = st.session_state.results
names = [r["place"]["name"] for r in results] if results else []

# ----------------------------------------------------------------------------
# Matches
# ----------------------------------------------------------------------------
with tab_rec:
    if results is None:
        st.info("Set your preferences in the sidebar and choose **Find my destinations**.")
    elif not results:
        st.warning("No close matches. Try a higher budget, another season or more interests.")
    else:
        q = st.session_state.query
        sort_by = st.radio("Sort by", ["Best match", "Lowest cost", "Shortest trip"], horizontal=True)
        view = list(results)
        if sort_by == "Lowest cost":
            view.sort(key=lambda r: r["place"]["budget"])
        elif sort_by == "Shortest trip":
            view.sort(key=lambda r: r["place"]["days"])

        for rank, r in enumerate(view, 1):
            p = r["place"]
            tags = "".join(f'<span class="tag">{html.escape(t)}</span>' for t in p["types"])
            warns = "".join(f'<span class="tag warn">{html.escape(w)}</span>' for w in r["warn"])
            st.markdown(f"""
            <div class="card {'top' if rank == 1 and sort_by == 'Best match' else ''}">
              <div class="pct"><b>{r['pct']}%</b><span>match</span></div>
              <div class="rank">Match {rank}</div>
              <div class="dest">{p['emoji']} {html.escape(p['name'])}</div>
              <p class="fact">{html.escape(p['description'])}</p>
              <span class="tag">About ₹{p['budget']:,} per person</span>
              <span class="tag">{p['days']} suggested days</span>{tags}{warns}
              <div class="fact"><b>Best time:</b> {html.escape(p['best'])}</div>
              <div class="fact"><b>Top activities:</b> {html.escape(', '.join(p['activities'][:4]))}</div>
              <div class="fact"><b>How to reach:</b> {html.escape(p['transport'])}</div>
              <div class="fact"><b>Local tip:</b> {html.escape(p['tip'])}</div>
              <div class="fact"><b>Why it ranks here:</b> {html.escape('; '.join(r['why']) or 'partial match')}.</div>
            </div>""", unsafe_allow_html=True)

            with st.expander("Score breakdown"):
                for key, val in r["breakdown"].items():
                    width = max(0, min(100, val / 3 * 100)) if val > 0 else 0
                    st.markdown(f'<div class="muted">{key}: {val:+d}</div>'
                                f'<div class="bar"><div style="width:{width}%"></div></div>', unsafe_allow_html=True)
            if p["name"] in st.session_state.shortlist:
                st.caption("✅ Saved to shortlist")
            elif st.button("Save to shortlist", key=f"save_{p['name']}"):
                st.session_state.shortlist.append(p["name"])
                st.rerun()

        df = pd.DataFrame([{"Rank": i, "Destination": r["place"]["name"], "Match %": r["pct"],
                            "Score": r["score"], "Budget (₹)": r["place"]["budget"],
                            "Days": r["place"]["days"]} for i, r in enumerate(results, 1)])
        st.download_button("Download results (CSV)", df.to_csv(index=False).encode(),
                           "travelwise_results.csv", "text/csv")
        st.caption("Budgets are approximate estimates, not live prices. Check transport, weather and stay costs before booking.")

# ----------------------------------------------------------------------------
# Trip planner (budget + itinerary)
# ----------------------------------------------------------------------------
with tab_plan:
    if not results:
        st.info("Run a search first to unlock the trip planner.")
    else:
        choice = st.selectbox("Choose a destination", names)
        p = next(r["place"] for r in results if r["place"]["name"] == choice)
        q = st.session_state.query
        left, right = st.columns([1, 1.2], gap="large")
        with left:
            st.subheader("Cost estimate")
            est = cost_estimate(p, q["days"], q["style"])
            total = sum(est.values())
            st.metric(f"Estimated total ({q['days']} days, {q['style'].lower()} stay)", f"₹{total:,.0f}",
                      delta=f"₹{q['budget'] - total:,.0f} vs your budget", delta_color="normal")
            st.bar_chart(pd.DataFrame({"₹ per person": est}))
            groups = st.number_input("Number of travellers", 1, 12, 2)
            st.write(f"**Group total for {groups}:** ₹{total * groups:,.0f}")
        with right:
            st.subheader("Suggested itinerary")
            for d, a, b in itinerary(p, q["days"]):
                st.markdown(f"**{d}**")
                st.write(f"Morning: {a}")
                st.write(f"Afternoon and evening: {b}")
            st.caption("Itineraries are starting points built from popular activities. Adjust for opening hours and travel time.")

# ----------------------------------------------------------------------------
# Compare
# ----------------------------------------------------------------------------
with tab_cmp:
    pool = [p["name"] for p in DESTINATIONS]
    pick = st.multiselect("Pick 2 to 4 destinations", pool, default=names[:3] if names else [], max_selections=4)
    if len(pick) < 2:
        st.info("Choose at least two destinations to compare.")
    else:
        rows = []
        for n in pick:
            p = next(x for x in DESTINATIONS if x["name"] == n)
            rows.append({"Destination": n, "Budget (₹)": p["budget"], "Days": p["days"],
                         "Best time": p["best"], "Types": ", ".join(p["types"]),
                         "Seasons": ", ".join(p["seasons"]), "Reach": p["transport"]})
        cdf = pd.DataFrame(rows).set_index("Destination").T
        st.dataframe(cdf, use_container_width=True)
        st.bar_chart(pd.DataFrame({"Budget (₹)": [r["Budget (₹)"] for r in rows]}, index=[r["Destination"] for r in rows]))

# ----------------------------------------------------------------------------
# Map
# ----------------------------------------------------------------------------
with tab_map:
    shown = [r["place"] for r in results] if results else DESTINATIONS
    st.caption("Showing your matches." if results else "Showing all destinations. Run a search to see only your matches.")
    st.map(pd.DataFrame([{"lat": p["lat"], "lon": p["lon"]} for p in shown]), zoom=4)

# ----------------------------------------------------------------------------
# Shortlist
# ----------------------------------------------------------------------------
with tab_short:
    sl = st.session_state.shortlist
    if not sl:
        st.info("Nothing saved yet. Use **Save to shortlist** on any match.")
    else:
        for n in sl:
            p = next(x for x in DESTINATIONS if x["name"] == n)
            c1, c2 = st.columns([5, 1])
            c1.markdown(f"**{p['emoji']} {n}** — about ₹{p['budget']:,} for {p['days']} days. Best time: {p['best']}")
            if c2.button("Remove", key=f"rm_{n}"):
                sl.remove(n)
                st.rerun()
        text = "\n".join(f"{n}" for n in sl)
        st.download_button("Download shortlist (TXT)", text, "shortlist.txt")

# ----------------------------------------------------------------------------
# About
# ----------------------------------------------------------------------------
with tab_about:
    c = st.columns(4)
    for col, (h, t) in zip(c, [("Input", "Budget, trip length, season, travel group, interests and stay style."),
                               ("Knowledge base", f"{len(DESTINATIONS)} destinations with budgets, seasons, activities and tips."),
                               ("Rule engine", "IF-THEN rules add or subtract points, then convert the score to a match percentage."),
                               ("Output", "Ranked matches, score breakdowns, cost estimates, itineraries and a map.")]):
        col.markdown(f"### {h}")
        col.write(t)
    st.code("""IF destination budget <= user budget:            +3
ELSE IF within 20% above budget:                 +1
ELSE:                                            -3
IF trip length equals suggested days:            +2
ELSE IF difference is 1 or 2 days:               +1
IF destination type matches an interest:         +3 per match
IF selected season is suitable:                  +2
IF traveller group fits destination type:        +1 or +2
Sort by score, show the top N, convert to match %.""", language="text")

st.markdown('<p class="muted" style="text-align:center;margin-top:28px;">TravelWise, a rule-based expert system built with Python and Streamlit</p>',
            unsafe_allow_html=True)
