"""
TravelWise: rule-based travel expert system (Streamlit)
Run:  pip install "streamlit>=1.40" pandas
      streamlit run travelwise_streamlit.py
"""
import pandas as pd
import streamlit as st

st.set_page_config(page_title="TravelWise | Destination Advisor", page_icon="✈️", layout="wide")

# ---------------------------------------------------------------- styling ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=Figtree:wght@400;500;600;700&display=swap');
:root{--ink:#0c2033;--muted:#566b7d;--line:#d3dee8;--accent:#0b7a75;--hot:#e07b00;--chip:#f3f7fa;}
html,body,[class*="css"]{font-family:'Figtree',sans-serif;}
.stApp{background:#e8eff5;color:var(--ink);}
#MainMenu,footer,header[data-testid="stHeader"]{visibility:hidden;height:0;}
.block-container{padding-top:1.5rem;max-width:1200px;}
section[data-testid="stSidebar"]{background:#fff;border-right:1px solid var(--line);}
section[data-testid="stSidebar"] *{color:var(--ink);}
.brand{font-family:'Bricolage Grotesque',serif;font-weight:800;font-size:22px;color:var(--ink);}
h1.hero{font-family:'Bricolage Grotesque',serif;font-weight:800;font-size:56px;line-height:1.02;letter-spacing:-.03em;margin:.4rem 0 .6rem;max-width:14ch;color:var(--ink);}
.lead{color:var(--muted);font-size:17px;max-width:54ch;margin-bottom:1.4rem;}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:22px;}
.kpi{background:#fff;border:1px solid var(--line);border-radius:14px;padding:14px 18px;}
.kpi b{display:block;font-family:'Bricolage Grotesque',serif;font-size:26px;color:var(--ink);}
.kpi span{font-size:13px;color:var(--muted);}
.pass{display:grid;grid-template-columns:1fr 180px;background:#fff;border:1px solid var(--line);border-radius:18px;margin-top:18px;overflow:hidden;}
.pass.first{border-color:var(--hot);box-shadow:0 0 0 1px var(--hot);}
.main{padding:22px 24px;}
.route{font-family:'Bricolage Grotesque',serif;font-weight:800;font-size:27px;letter-spacing:-.02em;color:var(--ink);}
.state{color:var(--muted);font-size:14px;margin:2px 0 8px;}
.desc{margin:0 0 12px;color:var(--ink);}
.tag{display:inline-block;background:var(--chip);border:1px solid var(--line);border-radius:6px;padding:2px 9px;font-size:12.5px;font-weight:600;margin:0 6px 6px 0;color:var(--ink);}
.tag.ok{border-color:var(--accent);color:var(--accent);}
.tag.bad{border-color:var(--hot);color:var(--hot);}
.facts{display:grid;grid-template-columns:1fr 1fr;gap:4px 20px;font-size:14px;margin-top:6px;}
.facts small{display:block;color:var(--muted);font-size:12.5px;}
.facts div{margin-bottom:6px;}
.stub{background:var(--ink);color:#fff;padding:22px 14px;text-align:center;display:flex;flex-direction:column;justify-content:center;border-left:2px dashed var(--line);}
.pct{font-family:'Bricolage Grotesque',serif;font-weight:800;font-size:48px;line-height:1;}
.stub small{opacity:.75;font-size:13px;}
.stub .cost{margin-top:12px;font-weight:700;font-size:18px;}
div.stButton>button{background:var(--accent);color:#fff;border:0;border-radius:99px;font-weight:700;}
div.stButton>button:hover{background:#09615d;color:#fff;}
.note{color:var(--muted);font-size:13px;margin-top:20px;}
@media(max-width:700px){.pass{grid-template-columns:1fr}.stub{border-left:0;border-top:2px dashed var(--line)}.kpis{grid-template-columns:1fr 1fr}.facts{grid-template-columns:1fr}h1.hero{font-size:38px}}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------- knowledge base ---
# name, state, budget (INR per person for suggested days), days, types, seasons,
# best time, activities, transport, emoji, description
RAW = [
    ("Rishikesh","Uttarakhand",7000,3,["Adventure","Nature","Spiritual"],["Winter","Summer"],"Sep-Nov, Feb-May",["River rafting","Ganga Aarti","Laxman Jhula cafes","Yoga session"],"Road or train via Haridwar","🏞️","Riverside escape with rafting, quiet ghats and mountain views."),
    ("Jaipur","Rajasthan",9000,3,["Culture","History","Family"],["Winter"],"Oct-Mar",["Amber Fort","City Palace","Hawa Mahal","Bapu Bazaar"],"Road, train or flight","🏰","Pink-city forts, palaces, bazaars and rich food."),
    ("Manali","Himachal Pradesh",14000,5,["Adventure","Nature","Romantic"],["Winter","Summer"],"Mar-Jun, Dec-Feb for snow",["Solang Valley","Old Manali","Hadimba Temple","Atal Tunnel"],"Road or overnight bus to Bhuntar","🏔️","Himalayan scenery with treks, snow and cafe-lined lanes."),
    ("Udaipur","Rajasthan",12000,3,["Romantic","Culture","Family"],["Winter"],"Oct-Mar",["City Palace","Lake Pichola boat ride","Sajjangarh sunset","Old city walk"],"Train, road or flight","🛶","Lake city of palaces, heritage hotels and sunsets."),
    ("Goa","Goa",18000,5,["Beach","Adventure","Nightlife","Family"],["Winter","Summer"],"Nov-Feb",["North Goa beaches","Water sports","Old Goa churches","Fort Aguada"],"Flight, train or road","🏖️","Beaches, food, nightlife and water sports."),
    ("Mussoorie","Uttarakhand",10000,3,["Nature","Family","Romantic"],["Summer","Winter"],"Mar-Jun, Sep-Nov",["Mall Road","Gun Hill","Kempty Falls","Lal Tibba"],"Train to Dehradun, then taxi","🌲","Easy hill station with viewpoints and walking routes."),
    ("Amritsar","Punjab",8000,2,["Culture","History","Family","Spiritual"],["Winter"],"Oct-Mar",["Golden Temple","Jallianwala Bagh","Wagah-Attari ceremony","Kulcha trail"],"Train, road or flight","🕌","Heritage, hospitality and some of India’s best food."),
    ("Srinagar","Jammu and Kashmir",22000,5,["Nature","Romantic","Family"],["Summer","Winter"],"Apr-Oct, winter for snow",["Dal Lake shikara","Mughal Gardens","Houseboat stay","Gulmarg day trip"],"Flight or road","🌊","Lakes, gardens and Himalayan landscapes."),
    ("Varanasi","Uttar Pradesh",9000,3,["Spiritual","Culture","History"],["Winter"],"Oct-Mar",["Ganga Aarti","Sunrise boat ride","Sarnath","Old city food walk"],"Train, road or flight","🪔","Ancient spiritual city on the banks of the Ganga."),
    ("Darjeeling","West Bengal",19000,5,["Nature","Family","Romantic"],["Summer","Winter"],"Mar-May, Oct-Nov",["Toy train","Tiger Hill sunrise","Tea garden visit","Monasteries"],"Flight or train to Bagdogra/NJP","🚂","Tea gardens, mountain views and a heritage railway."),
    ("Pondicherry","Puducherry",15000,4,["Beach","Culture","Romantic"],["Winter"],"Nov-Feb",["Promenade walk","French Quarter","Auroville","Cafe trail"],"Flight to Chennai, then road","🚲","French-style streets, cafes and calm beaches."),
    ("Nainital","Uttarakhand",11000,3,["Nature","Family","Romantic"],["Summer","Winter"],"Mar-Jun, Sep-Nov",["Naini Lake boating","Snow View ropeway","Mall Road","Bhimtal"],"Train to Kathgodam, then road","⛰️","Lake town for short family and couple getaways."),
    ("Jaisalmer","Rajasthan",13000,3,["Culture","History","Adventure"],["Winter"],"Oct-Feb",["Jaisalmer Fort","Sam dunes camel safari","Patwon Ki Haveli","Desert camp"],"Train, road or flight","🐪","Golden fort city with dune camps under the stars."),
    ("Alleppey","Kerala",20000,5,["Nature","Romantic","Family"],["Winter","Monsoon"],"Sep-Mar",["Houseboat cruise","Marari beach","Kumarakom birds","Ayurvedic spa"],"Flight to Kochi, then road","🛥️","Slow backwater cruises and coconut groves."),
    ("Kasol","Himachal Pradesh",9500,4,["Adventure","Nature"],["Summer","Winter"],"Mar-Jun, Sep-Nov",["Kheerganga trek","Manikaran hot springs","Tosh village","Riverside cafes"],"Overnight bus to Bhuntar, then taxi","⛺","Riverside valley for trekkers and backpackers."),
    ("Kochi","Kerala",16000,4,["Culture","History","Beach","Nature"],["Winter","Monsoon"],"Oct-Mar",["Fort Kochi walk","Chinese fishing nets","Kathakali show","Mattancherry"],"Flight, train or road","🎭","Colonial lanes, art, seafood and harbour views."),
]
KEYS = ["name","state","budget","days","types","seasons","best","acts","transport","emoji","desc"]
DESTINATIONS = [dict(zip(KEYS, r)) for r in RAW]

INTERESTS = ["Nature","Adventure","Beach","Culture","History","Spiritual","Romantic","Nightlife","Family"]
MULT = {"Budget": 0.85, "Comfort": 1.0, "Premium": 1.35}
SPLIT = {"Stay": .35, "Food": .20, "Transport": .25, "Activities": .15, "Other": .05}

def inr(n):
    return f"₹{round(n):,}"

# ------------------------------------------------------------- rule engine ---
def score_place(p, budget, days, interests, season, who):
    s, why, warn = 0, [], []
    if p["budget"] <= budget:
        s += 3; why.append("fits budget")
    elif p["budget"] <= budget * 1.2:
        s += 1; warn.append("a little over budget")
    else:
        s -= 3; warn.append("over budget")

    gap = abs(p["days"] - days)
    if gap == 0:
        s += 2; why.append("ideal length")
    elif gap <= 2:
        s += 1

    hit = [t for t in p["types"] if t in interests]
    s += 3 * len(hit)
    if hit:
        why.append(", ".join(hit))

    if season in p["seasons"]:
        s += 2; why.append(f"good in {season.lower()}")
    else:
        warn.append(f"not ideal in {season.lower()}")

    t = p["types"]
    bonus = 0
    if (who == "Family" and "Family" in t) or (who == "Couple" and "Romantic" in t) \
       or (who == "Friends" and any(x in t for x in ["Adventure", "Beach", "Nightlife"])):
        bonus = 2
    elif who == "Solo" and any(x in t for x in ["Adventure", "Culture", "Nature"]):
        bonus = 1
    if bonus:
        s += bonus; why.append(f"suits {who.lower()} travel")

    max_score = 9 + 3 * len(interests)
    pct = max(1, min(100, round(s / max_score * 100)))
    return {"place": p, "score": s, "pct": pct, "why": why, "warn": warn}

def recommend(budget, days, interests, season, who, top_n):
    res = [score_place(p, budget, days, interests, season, who) for p in DESTINATIONS]
    res = [r for r in res if r["score"] > 0]
    res.sort(key=lambda r: r["score"], reverse=True)
    return res[:top_n]

def estimate(p, days, style):
    total = p["budget"] / p["days"] * days * MULT[style]
    return total, {k: total * v for k, v in SPLIT.items()}

def pass_html(r, rank, days, style, interests):
    p = r["place"]
    total, _ = estimate(p, days, style)
    tags = "".join(f'<span class="tag {"ok" if t in interests else ""}">{t}</span>' for t in p["types"])
    tags += "".join(f'<span class="tag bad">{w}</span>' for w in r["warn"])
    why = "; ".join(r["why"]) or "Partial match"
    first = " first" if rank == 1 else ""
    return (
        f'<div class="pass{first}"><div class="main">'
        f'<div class="route">{p["emoji"]} {p["name"]}</div>'
        f'<div class="state">{p["state"]} · suggested {p["days"]} days</div>'
        f'<p class="desc">{p["desc"]}</p><div>{tags}</div>'
        f'<div class="facts">'
        f'<div><small>Best time</small>{p["best"]}</div>'
        f'<div><small>How to reach</small>{p["transport"]}</div>'
        f'<div><small>Top activities</small>{", ".join(p["acts"][:3])}</div>'
        f'<div><small>Why it ranks here</small>{why}</div>'
        f'</div></div>'
        f'<div class="stub"><div class="pct">{r["pct"]}%</div><small>match</small>'
        f'<div class="cost">{inr(total)}</div><small>est. per person</small></div></div>'
    )

# ------------------------------------------------------------------- state ---
if "saved" not in st.session_state:
    st.session_state.saved = []

# ----------------------------------------------------------------- sidebar ---
with st.sidebar:
    st.markdown('<div class="brand">✈️ TravelWise</div>', unsafe_allow_html=True)
    st.write("")
    budget = st.slider("Budget per person (₹)", 5000, 50000, 15000, 1000)
    days = st.slider("Trip length (days)", 2, 10, 4)
    season = st.pills("Season", ["Winter", "Summer", "Monsoon"], default="Winter") or "Winter"
    who = st.pills("Travelling with", ["Friends", "Family", "Couple", "Solo"], default="Friends") or "Friends"
    interests = st.pills("Interests", INTERESTS, selection_mode="multi", default=["Nature", "Adventure"]) or []
    style = st.pills("Stay style", list(MULT), default="Comfort") or "Comfort"
    top_n = st.slider("Number of results", 3, 8, 5)
    sort_by = st.selectbox("Sort by", ["Best match", "Lowest cost", "Shortest trip"])

# -------------------------------------------------------------------- main ---
st.markdown('<h1 class="hero">Where should you go next?</h1>'
            '<div class="lead">Set your budget, season and interests. TravelWise ranks destinations across India, '
            'explains each match and estimates what the trip will cost.</div>', unsafe_allow_html=True)

st.markdown(
    f'<div class="kpis"><div class="kpi"><b>{len(DESTINATIONS)}</b><span>Destinations</span></div>'
    f'<div class="kpi"><b>{inr(budget)}</b><span>Budget per person</span></div>'
    f'<div class="kpi"><b>{days} days</b><span>Trip length</span></div>'
    f'<div class="kpi"><b>{len(st.session_state.saved)}</b><span>Saved trips</span></div></div>',
    unsafe_allow_html=True)

tab_match, tab_compare, tab_saved, tab_about = st.tabs(["Matches", "Compare", "Saved trips", "How it works"])

with tab_match:
    if not interests:
        st.info("Pick at least one interest in the sidebar to see matches.")
    else:
        results = recommend(budget, days, interests, season, who, top_n)
        if sort_by == "Lowest cost":
            results.sort(key=lambda r: r["place"]["budget"])
        elif sort_by == "Shortest trip":
            results.sort(key=lambda r: r["place"]["days"])

        if not results:
            st.warning("No close matches. Raise your budget or try another season.")
        for rank, r in enumerate(results, 1):
            p = r["place"]
            st.markdown(pass_html(r, rank, days, style, interests), unsafe_allow_html=True)
            c1, c2 = st.columns([1, 4])
            with c1:
                done = p["name"] in st.session_state.saved
                if st.button("Saved ✓" if done else "Save trip", key=f"s_{p['name']}", disabled=done):
                    st.session_state.saved.append(p["name"])
                    st.rerun()
            with c2:
                with st.expander(f"Cost breakdown and {days}-day plan"):
                    total, parts = estimate(p, days, style)
                    st.metric(f"Estimated total ({style.lower()} stay)", inr(total),
                              delta=f"{inr(budget - total)} vs your budget")
                    st.bar_chart(pd.DataFrame({"₹ per person": parts}))
                    for d in range(days):
                        a, b = p["acts"][(d * 2) % 4], p["acts"][(d * 2 + 1) % 4]
                        st.write(f"**Day {d + 1}:** {a} and {b}")

        if results:
            df = pd.DataFrame([{"Rank": i, "Destination": r["place"]["name"], "State": r["place"]["state"],
                                "Match %": r["pct"], "Budget (INR)": r["place"]["budget"],
                                "Suggested days": r["place"]["days"]} for i, r in enumerate(results, 1)])
            st.download_button("Download results (CSV)", df.to_csv(index=False).encode(), "travelwise_results.csv", "text/csv")
        st.markdown('<div class="note">Budgets are approximate estimates, not live prices. Check transport, weather and stays before booking.</div>',
                    unsafe_allow_html=True)

with tab_compare:
    names = [p["name"] for p in DESTINATIONS]
    pick = st.multiselect("Pick 2 to 4 destinations", names, default=["Jaipur", "Goa"], max_selections=4)
    if len(pick) < 2:
        st.info("Choose at least two destinations.")
    else:
        rows = {}
        for n in pick:
            p = next(x for x in DESTINATIONS if x["name"] == n)
            rows[n] = {"State": p["state"], "Budget": inr(p["budget"]), "Suggested days": p["days"],
                       "Best time": p["best"], "Types": ", ".join(p["types"]),
                       "Seasons": ", ".join(p["seasons"]), "How to reach": p["transport"]}
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
        st.bar_chart(pd.DataFrame({"Budget (INR)": [next(x for x in DESTINATIONS if x["name"] == n)["budget"] for n in pick]}, index=pick))

with tab_saved:
    if not st.session_state.saved:
        st.info("Nothing saved yet. Use Save trip on any match.")
    else:
        for n in list(st.session_state.saved):
            p = next(x for x in DESTINATIONS if x["name"] == n)
            c1, c2 = st.columns([5, 1])
            c1.markdown(f"**{p['emoji']} {n}**, {p['state']}: about {inr(p['budget'])} for {p['days']} days. Best time: {p['best']}")
            if c2.button("Remove", key=f"r_{n}"):
                st.session_state.saved.remove(n)
                st.rerun()
        st.download_button("Download saved trips (TXT)", "\n".join(st.session_state.saved), "saved_trips.txt")

with tab_about:
    c = st.columns(4)
    items = [("Input", "Budget, trip length, season, travel group, interests and stay style."),
             ("Knowledge base", f"{len(DESTINATIONS)} destinations with budgets, seasons, activities and transport."),
             ("Rule engine", "IF-THEN rules add or subtract points, then the score becomes a match percentage."),
             ("Output", "Ranked boarding-pass cards, cost estimates, day plans and comparisons.")]
    for col, (h, t) in zip(c, items):
        col.markdown(f"### {h}")
        col.write(t)
    st.code("""IF destination budget <= user budget:          +3
ELSE IF within 20% above budget:               +1
ELSE:                                          -3
IF trip length equals suggested days:          +2
ELSE IF difference is 1 or 2 days:             +1
IF destination type matches an interest:       +3 per match
IF selected season is suitable:                +2
IF traveller group fits destination type:      +1 or +2
Sort by score, show the top N, convert to match %.""", language="text")
