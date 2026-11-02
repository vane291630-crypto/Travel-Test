"""
TravelWise Dashboard: a Traveloo-style travel dashboard powered by a rule-based expert system.
Run:  pip install "streamlit>=1.40" pandas
      streamlit run travelwise_dashboard.py
"""
import calendar
from datetime import date, timedelta

import pandas as pd
import streamlit as st

st.set_page_config(page_title="TravelWise Dashboard", page_icon="✈️", layout="wide")

# ------------------------------------------------------------ knowledge base ---
# name, state, budget (INR/person for suggested days), days, types, seasons, best time,
# activities, transport, emoji, description, optional photo URL (paste your own image links)
RAW = [
    ("Rishikesh","Uttarakhand",7000,3,["Adventure","Nature","Spiritual"],["Winter","Summer"],"Sep-Nov, Feb-May",["River rafting","Ganga Aarti","Laxman Jhula cafes","Yoga session"],"Road or train via Haridwar","🏞️","Riverside escape with rafting, quiet ghats and mountain views.",""),
    ("Jaipur","Rajasthan",9000,3,["Culture","History","Family"],["Winter"],"Oct-Mar",["Amber Fort","City Palace","Hawa Mahal","Bapu Bazaar"],"Road, train or flight","🏰","Pink-city forts, palaces, bazaars and rich food.",""),
    ("Manali","Himachal Pradesh",14000,5,["Adventure","Nature","Romantic"],["Winter","Summer"],"Mar-Jun, Dec-Feb for snow",["Solang Valley","Old Manali","Hadimba Temple","Atal Tunnel"],"Road or overnight bus to Bhuntar","🏔️","Himalayan scenery with treks, snow and cafe-lined lanes.",""),
    ("Udaipur","Rajasthan",12000,3,["Romantic","Culture","Family"],["Winter"],"Oct-Mar",["City Palace","Lake Pichola boat ride","Sajjangarh sunset","Old city walk"],"Train, road or flight","🛶","Lake city of palaces, heritage hotels and sunsets.",""),
    ("Goa","Goa",18000,5,["Beach","Adventure","Nightlife","Family"],["Winter","Summer"],"Nov-Feb",["North Goa beaches","Water sports","Old Goa churches","Fort Aguada"],"Flight, train or road","🏖️","Beaches, food, nightlife and water sports.",""),
    ("Mussoorie","Uttarakhand",10000,3,["Nature","Family","Romantic"],["Summer","Winter"],"Mar-Jun, Sep-Nov",["Mall Road","Gun Hill","Kempty Falls","Lal Tibba"],"Train to Dehradun, then taxi","🌲","Easy hill station with viewpoints and walking routes.",""),
    ("Amritsar","Punjab",8000,2,["Culture","History","Family","Spiritual"],["Winter"],"Oct-Mar",["Golden Temple","Jallianwala Bagh","Wagah-Attari ceremony","Kulcha trail"],"Train, road or flight","🕌","Heritage, hospitality and some of India’s best food.",""),
    ("Srinagar","Jammu and Kashmir",22000,5,["Nature","Romantic","Family"],["Summer","Winter"],"Apr-Oct, winter for snow",["Dal Lake shikara","Mughal Gardens","Houseboat stay","Gulmarg day trip"],"Flight or road","🌊","Lakes, gardens and Himalayan landscapes.",""),
    ("Varanasi","Uttar Pradesh",9000,3,["Spiritual","Culture","History"],["Winter"],"Oct-Mar",["Ganga Aarti","Sunrise boat ride","Sarnath","Old city food walk"],"Train, road or flight","🪔","Ancient spiritual city on the banks of the Ganga.",""),
    ("Darjeeling","West Bengal",19000,5,["Nature","Family","Romantic"],["Summer","Winter"],"Mar-May, Oct-Nov",["Toy train","Tiger Hill sunrise","Tea garden visit","Monasteries"],"Flight or train to Bagdogra/NJP","🚂","Tea gardens, mountain views and a heritage railway.",""),
    ("Pondicherry","Puducherry",15000,4,["Beach","Culture","Romantic"],["Winter"],"Nov-Feb",["Promenade walk","French Quarter","Auroville","Cafe trail"],"Flight to Chennai, then road","🚲","French-style streets, cafes and calm beaches.",""),
    ("Nainital","Uttarakhand",11000,3,["Nature","Family","Romantic"],["Summer","Winter"],"Mar-Jun, Sep-Nov",["Naini Lake boating","Snow View ropeway","Mall Road","Bhimtal"],"Train to Kathgodam, then road","⛰️","Lake town for short family and couple getaways.",""),
    ("Jaisalmer","Rajasthan",13000,3,["Culture","History","Adventure"],["Winter"],"Oct-Feb",["Jaisalmer Fort","Sam dunes camel safari","Patwon Ki Haveli","Desert camp"],"Train, road or flight","🐪","Golden fort city with dune camps under the stars.",""),
    ("Alleppey","Kerala",20000,5,["Nature","Romantic","Family"],["Winter","Monsoon"],"Sep-Mar",["Houseboat cruise","Marari beach","Kumarakom birds","Ayurvedic spa"],"Flight to Kochi, then road","🛥️","Slow backwater cruises and coconut groves.",""),
    ("Kasol","Himachal Pradesh",9500,4,["Adventure","Nature"],["Summer","Winter"],"Mar-Jun, Sep-Nov",["Kheerganga trek","Manikaran hot springs","Tosh village","Riverside cafes"],"Overnight bus to Bhuntar, then taxi","⛺","Riverside valley for trekkers and backpackers.",""),
    ("Kochi","Kerala",16000,4,["Culture","History","Beach","Nature"],["Winter","Monsoon"],"Oct-Mar",["Fort Kochi walk","Chinese fishing nets","Kathakali show","Mattancherry"],"Flight, train or road","🎭","Colonial lanes, art, seafood and harbour views.",""),
]
KEYS = ["name","state","budget","days","types","seasons","best","acts","transport","emoji","desc","img"]
DEST = [dict(zip(KEYS, r)) for r in RAW]
INTERESTS = ["Nature","Adventure","Beach","Culture","History","Spiritual","Romantic","Nightlife","Family"]
MULT = {"Budget": 0.85, "Comfort": 1.0, "Premium": 1.35}
GRADS = [("#7be0d4","#2aa6c9"),("#ffd88a","#ff9a76"),("#b7a6ff","#6f8bff"),("#9be37f","#27b38a"),("#ffb3c7","#ff7a9c"),("#9ad1ff","#4f8cf0")]
inr = lambda n: f"₹{round(n):,}"

# --------------------------------------------------------------- rule engine ---
def score_place(p, budget, days, interests, season, who):
    s, why, warn = 0, [], []
    if p["budget"] <= budget: s += 3; why.append("fits budget")
    elif p["budget"] <= budget * 1.2: s += 1; warn.append("a little over budget")
    else: s -= 3; warn.append("over budget")
    gap = abs(p["days"] - days)
    if gap == 0: s += 2; why.append("ideal length")
    elif gap <= 2: s += 1
    hit = [t for t in p["types"] if t in interests]
    s += 3 * len(hit)
    if hit: why.append(", ".join(hit))
    if season in p["seasons"]: s += 2; why.append(f"good in {season.lower()}")
    else: warn.append(f"not ideal in {season.lower()}")
    t, bonus = p["types"], 0
    if (who == "Family" and "Family" in t) or (who == "Couple" and "Romantic" in t) or \
       (who == "Friends" and any(x in t for x in ["Adventure","Beach","Nightlife"])): bonus = 2
    elif who == "Solo" and any(x in t for x in ["Adventure","Culture","Nature"]): bonus = 1
    if bonus: s += bonus; why.append(f"suits {who.lower()} travel")
    pct = max(1, min(100, round(s / (9 + 3 * len(interests)) * 100)))
    return {"p": p, "score": s, "pct": pct, "why": why, "warn": warn}

def recommend(budget, days, interests, season, who):
    res = [score_place(p, budget, days, interests, season, who) for p in DEST]
    return sorted([r for r in res if r["score"] > 0], key=lambda r: r["score"], reverse=True)

def est(p, days, style): return p["budget"] / p["days"] * days * MULT[style]

# ------------------------------------------------------------------- state ---
st.session_state.setdefault("saved", [])

# ----------------------------------------------------------------- sidebar ---
with st.sidebar:
    st.markdown('<div class="logo">🕊️ TravelWise</div>', unsafe_allow_html=True)
    page = st.radio("Menu", ["🏠  Home", "🧭  Explore", "❤️  Saved trips", "⚙️  How it works"], label_visibility="collapsed")
    st.markdown("---")
    st.caption("Trip preferences")
    budget = st.slider("Budget per person (₹)", 5000, 50000, 15000, 1000)
    days = st.slider("Trip length (days)", 2, 10, 4)
    start = st.date_input("Start date", date.today() + timedelta(days=14))
    season = st.selectbox("Season", ["Winter", "Summer", "Monsoon"])
    who = st.selectbox("Travelling with", ["Friends", "Family", "Couple", "Solo"])
    interests = st.multiselect("Interests", INTERESTS, default=["Nature", "Adventure"])
    style = st.selectbox("Stay style", list(MULT), index=1)
    name = st.text_input("Your name", "Traveller")
    dark = st.toggle("Dark mode")

# ------------------------------------------------------------------ styling ---
V = dict(bg="#11161c", card="#1b222b", text="#eef3f7", muted="#93a1ae", line="#2a343f", side="#161c23", shade="rgba(0,0,0,.35)") if dark else \
    dict(bg="#f3f5f8", card="#ffffff", text="#16202a", muted="#7a8794", line="#e6ebf0", side="#ffffff", shade="rgba(30,60,90,.08)")
page_bg = "#11161c" if dark else "linear-gradient(135deg,#7eeadb 0%,#86e6e0 45%,#fdf6c9 100%)"
st.markdown(f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
:root{{--bg:{V['bg']};--card:{V['card']};--text:{V['text']};--muted:{V['muted']};--line:{V['line']};--teal:#12c6c4;--shade:{V['shade']};}}
html,body,[class*="css"]{{font-family:'Poppins',sans-serif;}}
.stApp{{background:{page_bg};}}
#MainMenu,footer,header[data-testid="stHeader"]{{visibility:hidden;height:0;}}
.block-container{{background:var(--bg);border-radius:28px;margin-top:28px;padding:28px 34px;max-width:1280px;box-shadow:0 20px 50px var(--shade);color:var(--text);}}
section[data-testid="stSidebar"]{{background:{V['side']};}}
section[data-testid="stSidebar"] *{{color:var(--text);}}
.logo{{font-weight:700;font-size:20px;color:var(--teal);margin:6px 0 18px;}}
h1,h2,h3,p,label,span{{color:var(--text);}}
.hello b{{font-size:24px;}} .hello div{{color:var(--muted);font-size:14px;}}
.sec{{font-weight:600;font-size:19px;margin:22px 0 12px;display:flex;justify-content:space-between;}}
.sec span{{font-size:13px;font-weight:500;color:var(--muted);}}
.card{{background:var(--card);border-radius:20px;padding:14px;box-shadow:0 4px 18px var(--shade);}}
.upcoming{{display:grid;grid-template-columns:230px 1fr;gap:18px;}}
.tile{{border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:64px;background-size:cover;background-position:center;}}
.pill{{display:inline-block;border:1px solid var(--line);border-radius:10px;padding:4px 10px;font-size:13px;margin:0 6px 8px 0;}}
.muted{{color:var(--muted);font-size:13px;}}
.route{{border:1.5px solid var(--text);border-radius:10px;padding:5px 12px;font-size:13px;display:inline-block;margin:6px 0 12px;}}
.route b{{color:var(--teal);font-weight:600;}}
.cta{{background:var(--teal);color:#fff!important;text-align:center;border-radius:12px;padding:9px;font-weight:600;font-size:14px;}}
.trip{{padding:12px;}} .trip .tile{{height:150px;font-size:56px;margin-bottom:10px;position:relative;}}
.badge{{position:absolute;top:0;right:12px;background:#ffd23f;color:#3a2c00;font-size:12px;font-weight:700;padding:6px 8px 10px;border-radius:0 0 8px 8px;}}
.trip h4{{margin:0;font-size:15px;font-weight:600;}} .price{{font-weight:600;margin:4px 0;}}
.row{{display:flex;justify-content:space-between;font-size:13px;margin-top:8px;}}
.cal{{width:100%;text-align:center;font-size:13px;border-collapse:separate;border-spacing:0 4px;}}
.cal th{{color:var(--muted);font-size:11px;font-weight:500;}}
.cal td{{padding:7px 0;}} .cal td.in{{background:rgba(18,198,196,.18);}}
.cal td.edge span{{background:var(--teal);color:#fff;border-radius:50%;padding:6px 8px;}}
.done{{display:flex;align-items:center;gap:12px;padding:12px;margin-bottom:10px;}}
.done .dot{{width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:20px;background:rgba(18,198,196,.15);}}
.done .nm{{font-weight:600;font-size:14px;}}
.tagbtn{{margin-left:auto;background:var(--teal);color:#fff!important;border-radius:10px;padding:6px 14px;font-size:13px;font-weight:600;}}
div.stButton>button{{background:var(--card);color:var(--text);border:1px solid var(--line);border-radius:12px;font-weight:600;}}
div.stButton>button:hover{{border-color:var(--teal);color:var(--teal);}}
div[data-testid="stTextInput"] input{{border-radius:14px;}}
.avatar{{width:46px;height:46px;border-radius:50%;background:#ffd0dc;display:flex;align-items:center;justify-content:center;font-size:24px;margin-left:auto;}}
@media(max-width:800px){{.upcoming{{grid-template-columns:1fr;}}}}
</style>""", unsafe_allow_html=True)

# ------------------------------------------------------------------ helpers ---
def tile(p, i, extra=""):
    if p["img"]:
        return f'<div class="tile" style="background-image:url(\'{p["img"]}\')">{extra}</div>'
    c1, c2 = GRADS[i % len(GRADS)]
    return f'<div class="tile" style="background:linear-gradient(135deg,{c1},{c2})">{extra}{p["emoji"]}</div>'

def trip_card(r, i):
    p = r["p"]
    badge = '<div class="badge">Best<br>match</div>' if i == 0 else ""
    return (f'<div class="card trip">{tile(p, i, badge)}<h4>{p["name"]} ({p["state"]})</h4>'
            f'<div class="price">{inr(est(p, days, style))} <span class="muted">per person</span></div>'
            f'<div class="muted">{p["desc"]}</div>'
            f'<div class="row"><span>🎯 {r["pct"]}% match</span><span>{p["days"]} days</span></div></div>')

def calendar_html(start, days):
    end = start + timedelta(days=days - 1)
    cal = calendar.Calendar(firstweekday=6).monthdayscalendar(start.year, start.month)
    head = "".join(f"<th>{d}</th>" for d in ["SUN","MON","TUE","WED","THU","FRI","SAT"])
    rows = ""
    for wk in cal:
        tds = ""
        for d in wk:
            if d == 0: tds += "<td></td>"; continue
            cur = date(start.year, start.month, d)
            cls = "in" if start <= cur <= end else ""
            cls += " edge" if cur in (start, end) else ""
            tds += f'<td class="{cls}"><span>{d}</span></td>'
        rows += f"<tr>{tds}</tr>"
    return (f'<div class="card"><div class="row" style="margin:0 6px 8px"><b>ACTIVITY</b>'
            f'<b style="color:var(--teal)">{start.strftime("%b %Y").upper()}</b></div>'
            f'<table class="cal"><tr>{head}</tr>{rows}</table></div>')

def saved_html():
    if not st.session_state.saved:
        return '<div class="card muted" style="text-align:center">No saved trips yet. Tap Save on a card.</div>'
    out = ""
    for n in st.session_state.saved[:4]:
        p = next(x for x in DEST if x["name"] == n)
        out += (f'<div class="card done"><div class="dot">{p["emoji"]}</div><div><div class="nm">{n} ({p["state"]})</div>'
                f'<div class="muted">{inr(est(p, days, style))} · {days} days</div></div><div class="tagbtn">Saved</div></div>')
    return out

def card_grid(rs, key):
    cols = st.columns(3)
    for k, r in enumerate(rs):
        with cols[k % 3]:
            st.markdown(trip_card(r, k), unsafe_allow_html=True)
            n = r["p"]["name"]
            if n in st.session_state.saved:
                st.button("♥ Saved", key=f"{key}{n}", disabled=True, use_container_width=True)
            elif st.button("♡ Save trip", key=f"{key}{n}", use_container_width=True):
                st.session_state.saved.append(n); st.rerun()

# --------------------------------------------------------------------- data ---
results = recommend(budget, days, interests, season, who) if interests else []

# -------------------------------------------------------------------- pages ---
if page.endswith("Home"):
    h1, h2, h3 = st.columns([1.3, 1.6, .4])
    h1.markdown(f'<div class="hello"><b>Hello {name}!</b><div>Welcome back and explore new trips</div></div>', unsafe_allow_html=True)
    q = h2.text_input("Search", placeholder="Search a destination, e.g. Goa", label_visibility="collapsed")
    h3.markdown('<div class="avatar">🙂</div>', unsafe_allow_html=True)
    if q: results = [r for r in results if q.lower() in (r["p"]["name"] + r["p"]["state"]).lower()]

    left, right = st.columns([2.1, 1], gap="large")
    with left:
        st.markdown('<div class="sec">Upcoming trip</div>', unsafe_allow_html=True)
        if results:
            r = results[0]; p = r["p"]
            end = start + timedelta(days=days - 1)
            st.markdown(
                f'<div class="card upcoming">{tile(p, 0)}<div><h4 style="margin:4px 0 8px">{p["name"]} trip</h4>'
                f'<span class="pill">📅 {start.strftime("%d %b")} - {end.strftime("%d %b")}</span>'
                f'<span class="pill">📍 {p["state"]}</span><div class="muted">{p["desc"]} Best time: {p["best"]}.</div>'
                f'<div class="route">✈ From <b>Delhi</b> to <b>{p["name"]}</b></div>'
                f'<div class="cta">{inr(est(p, days, style))} per person · {r["pct"]}% match</div></div></div>', unsafe_allow_html=True)
        else:
            st.info("No matches yet. Add interests or raise your budget in the sidebar.")
        st.markdown('<div class="sec">Trips exclusively for you<span>Top matches</span></div>', unsafe_allow_html=True)
        card_grid(results[1:4], "h")
        st.markdown('<div class="sec">Budget-friendly picks</div>', unsafe_allow_html=True)
        cheap = sorted(results, key=lambda r: r["p"]["budget"])[:3]
        card_grid(cheap, "c")
    with right:
        st.markdown('<div class="sec">Calendar</div>', unsafe_allow_html=True)
        st.markdown(calendar_html(start, days), unsafe_allow_html=True)
        st.markdown('<div class="sec">Saved trips</div>', unsafe_allow_html=True)
        st.markdown(saved_html(), unsafe_allow_html=True)

elif page.endswith("Explore"):
    st.markdown('<div class="sec">Explore all matches</div>', unsafe_allow_html=True)
    if not results: st.info("Pick at least one interest in the sidebar.")
    sort = st.radio("Sort by", ["Best match", "Lowest cost", "Shortest trip"], horizontal=True)
    if sort == "Lowest cost": results = sorted(results, key=lambda r: r["p"]["budget"])
    if sort == "Shortest trip": results = sorted(results, key=lambda r: r["p"]["days"])
    card_grid(results[:9], "e")
    if results:
        df = pd.DataFrame([{"Destination": r["p"]["name"], "State": r["p"]["state"], "Match %": r["pct"],
                            "Est. cost (INR)": round(est(r["p"], days, style)), "Best time": r["p"]["best"],
                            "Why": "; ".join(r["why"])} for r in results])
        st.markdown('<div class="sec">Compare table</div>', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button("Download CSV", df.to_csv(index=False).encode(), "travelwise_results.csv", "text/csv")

elif page.endswith("Saved trips"):
    st.markdown('<div class="sec">Saved trips</div>', unsafe_allow_html=True)
    if not st.session_state.saved: st.info("Nothing saved yet.")
    for n in list(st.session_state.saved):
        p = next(x for x in DEST if x["name"] == n)
        a, b = st.columns([5, 1])
        a.markdown(f'<div class="card done"><div class="dot">{p["emoji"]}</div><div><div class="nm">{n}, {p["state"]}</div>'
                   f'<div class="muted">{inr(est(p, days, style))} for {days} days · Best time: {p["best"]} · {", ".join(p["acts"][:3])}</div></div></div>',
                   unsafe_allow_html=True)
        if b.button("Remove", key=f"rm{n}"): st.session_state.saved.remove(n); st.rerun()

else:
    st.markdown('<div class="sec">How the expert system works</div>', unsafe_allow_html=True)
    st.code("""IF destination budget <= user budget:          +3
ELSE IF within 20% above budget:               +1
ELSE:                                          -3
IF trip length equals suggested days:          +2
ELSE IF difference is 1 or 2 days:             +1
IF destination type matches an interest:       +3 per match
IF selected season is suitable:                +2
IF traveller group fits destination type:      +1 or +2
Sort by score, show the top results, convert to match %.""", language="text")
    st.caption("Budgets are approximate estimates, not live prices. To show real photos, paste image URLs in the last field of each destination in RAW.")
