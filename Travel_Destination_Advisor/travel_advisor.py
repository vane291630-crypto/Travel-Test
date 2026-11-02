import streamlit as st

st.set_page_config(page_title="TravelWise | Destination Advisor", page_icon="✈️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
html, body, [class*="css"] {font-family:'DM Sans',sans-serif;}
.stApp {background:#f4f7fb;}
.hero {padding:40px;border-radius:22px;color:white;background:linear-gradient(115deg,#102a43,#176b87,#38a3a5);margin-bottom:24px;}
.hero h1 {font-family:'Manrope',sans-serif;font-size:40px;font-weight:800;margin:8px 0;}
.hero p {font-size:16px;opacity:.92;margin:0;}
.result-card {background:white;border:1px solid #e4ebf2;border-radius:16px;padding:20px;margin:12px 0;box-shadow:0 4px 15px rgba(20,45,70,.05);}
.destination-name {color:#102a43;font-family:'Manrope',sans-serif;font-size:23px;font-weight:800;}
.tag {display:inline-block;background:#e8f5f5;color:#176b70;padding:5px 10px;border-radius:20px;font-size:12px;margin:3px;}
.muted {color:#647789;font-size:13px;}
div.stButton>button {background:#176b87;color:white;border:0;border-radius:10px;font-weight:700;}
div.stButton>button:hover {background:#12566d;color:white;}
</style>
""", unsafe_allow_html=True)

# Knowledge base: approximate budget per person in Indian rupees.
DESTINATIONS = [
    {"name":"Rishikesh, Uttarakhand","budget":7000,"days":3,"types":["Adventure","Nature","Spiritual"],"seasons":["Winter","Summer","Monsoon"],"best":"September-November and February-May","activities":"River rafting, Ganga Aarti, cafes, yoga and short hikes","transport":"Road or train via Haridwar","emoji":"🏞️","description":"A riverside escape with adventure, peaceful ghats and mountain views."},
    {"name":"Jaipur, Rajasthan","budget":9000,"days":3,"types":["Culture","History","Family"],"seasons":["Winter"],"best":"October-March","activities":"Amber Fort, City Palace, Hawa Mahal and local markets","transport":"Road, train or flight","emoji":"🏰","description":"A colourful heritage city known for forts, architecture, shopping and food."},
    {"name":"Manali, Himachal Pradesh","budget":14000,"days":5,"types":["Adventure","Nature","Romantic"],"seasons":["Winter","Summer"],"best":"March-June; December-February for snow experiences","activities":"Solang Valley, Old Manali, mountain drives and nature walks","transport":"Road or overnight bus; nearest airport is Bhuntar","emoji":"🏔️","description":"A Himalayan getaway for mountain scenery and outdoor activities."},
    {"name":"Udaipur, Rajasthan","budget":12000,"days":3,"types":["Romantic","Culture","Family"],"seasons":["Winter"],"best":"October-March","activities":"City Palace, Lake Pichola boat ride and heritage streets","transport":"Train, road or flight","emoji":"🛶","description":"A relaxed lake city with palaces, heritage hotels and sunset views."},
    {"name":"Goa","budget":18000,"days":5,"types":["Beach","Adventure","Nightlife","Family"],"seasons":["Winter","Summer"],"best":"November-February","activities":"Beaches, forts, water sports, markets and cafes","transport":"Flight, train or road","emoji":"🏖️","description":"A beach destination offering relaxation, food, nightlife and water activities."},
    {"name":"Mussoorie, Uttarakhand","budget":10000,"days":3,"types":["Nature","Family","Romantic"],"seasons":["Summer","Winter"],"best":"March-June and September-November","activities":"Mall Road, Gun Hill, Kempty Falls and scenic walks","transport":"Road or train to Dehradun followed by taxi","emoji":"🌲","description":"A hill station with viewpoints, cafes and scenic walking routes."},
    {"name":"Amritsar, Punjab","budget":8000,"days":2,"types":["Culture","History","Family","Spiritual"],"seasons":["Winter"],"best":"October-March","activities":"Golden Temple, Jallianwala Bagh and Wagah-Attari ceremony","transport":"Train, road or flight","emoji":"🕌","description":"A cultural destination known for its heritage, hospitality and food."},
    {"name":"Srinagar, Jammu and Kashmir","budget":22000,"days":5,"types":["Nature","Romantic","Family"],"seasons":["Summer","Winter"],"best":"April-October; winter for snow scenery","activities":"Dal Lake, gardens, houseboats and mountain excursions","transport":"Flight or road","emoji":"🌊","description":"A scenic valley destination with lakes, gardens and Himalayan landscapes."},
    {"name":"Varanasi, Uttar Pradesh","budget":9000,"days":3,"types":["Spiritual","Culture","History"],"seasons":["Winter"],"best":"October-March","activities":"Ganga Aarti, sunrise boat ride, temples and old-city lanes","transport":"Train, road or flight","emoji":"🪔","description":"A heritage and spiritual city on the banks of the Ganga."},
    {"name":"Darjeeling, West Bengal","budget":19000,"days":5,"types":["Nature","Family","Romantic"],"seasons":["Summer","Winter"],"best":"March-May and October-November","activities":"Toy train, tea gardens, viewpoints and monasteries","transport":"Flight or train to Bagdogra/NJP, then road","emoji":"🚂","description":"A hill town famous for tea gardens, mountain views and its heritage railway."},
    {"name":"Pondicherry","budget":15000,"days":4,"types":["Beach","Culture","Romantic"],"seasons":["Winter"],"best":"November-February","activities":"Promenade, French Quarter, cafes and nearby beaches","transport":"Flight to Chennai followed by road; train and bus options","emoji":"🚲","description":"A relaxed coastal town with French-inspired streets and cafes."},
    {"name":"Nainital, Uttarakhand","budget":11000,"days":3,"types":["Nature","Family","Romantic"],"seasons":["Summer","Winter"],"best":"March-June and September-November","activities":"Naini Lake, ropeway, viewpoints and nearby lakes","transport":"Train to Kathgodam followed by road","emoji":"⛰️","description":"A popular lake town suited to short family and couples' holidays."}
]

def recommend_destinations(budget, trip_days, interests, season, traveller):
    """Rule-based scoring engine for the travel expert system."""
    matches = []
    for place in DESTINATIONS:
        score, reasons = 0, []

        if place["budget"] <= budget:
            score += 3
            reasons.append("within your approximate budget")
        elif place["budget"] <= budget * 1.20:
            score += 1
            reasons.append("slightly above your budget")
        else:
            score -= 3

        day_gap = abs(place["days"] - trip_days)
        if day_gap == 0:
            score += 2
            reasons.append("matches your trip duration")
        elif day_gap <= 2:
            score += 1

        interest_matches = set(interests).intersection(place["types"])
        score += 3 * len(interest_matches)
        if interest_matches:
            reasons.append("matches your interests: " + ", ".join(sorted(interest_matches)))

        if season in place["seasons"]:
            score += 2
            reasons.append("suitable for your selected season")

        if traveller == "Family" and "Family" in place["types"]:
            score += 2
        elif traveller == "Couple" and "Romantic" in place["types"]:
            score += 2
        elif traveller == "Solo" and any(x in place["types"] for x in ["Adventure","Culture","Nature"]):
            score += 1
        elif traveller == "Friends" and any(x in place["types"] for x in ["Adventure","Beach","Nightlife"]):
            score += 2

        if score > 0:
            matches.append({"score":score,"place":place,"reasons":reasons})

    matches.sort(key=lambda item:item["score"], reverse=True)
    return matches[:5]

st.markdown("""
<div class="hero">
  <div style="letter-spacing:3px;font-size:12px;font-weight:700;">SMART TRAVEL PLANNING · RULE-BASED EXPERT SYSTEM</div>
  <h1>Find Your Next Escape ✈️</h1>
  <p>Discover destinations that match your budget, interests and travel style.</p>
</div>
""", unsafe_allow_html=True)

input_col, output_col = st.columns([1, 1.6], gap="large")

with input_col:
    st.subheader("🧳 Plan Your Trip")
    st.caption("Enter your preferences below.")
    budget = st.slider("Your budget per person (₹)", 5000, 50000, 15000, 1000)
    trip_days = st.select_slider("Trip duration", options=[2,3,4,5,6,7,10], value=4, format_func=lambda x:f"{x} days")
    season = st.selectbox("Preferred travel season", ["Winter","Summer","Monsoon"])
    traveller = st.selectbox("Who are you travelling with?", ["Friends","Family","Couple","Solo"])
    interests = st.multiselect("Select your travel interests", ["Nature","Adventure","Beach","Culture","History","Spiritual","Romantic","Nightlife","Family"], default=["Nature","Adventure"])
    find_button = st.button("Find My Destinations ✨", use_container_width=True)
    st.info("Tip: Select multiple interests to get more relevant suggestions.")

with output_col:
    st.subheader("🌍 Your Destination Matches")
    if find_button:
        if not interests:
            st.warning("Please select at least one travel interest.")
        else:
            results = recommend_destinations(budget, trip_days, interests, season, traveller)
            if not results:
                st.warning("No close matches found. Try increasing your budget or changing your preferences.")
            else:
                st.success(f"We found {len(results)} destinations for your preferences!")
                for rank, result in enumerate(results, start=1):
                    p = result["place"]
                    st.markdown(f"""
                    <div class="result-card">
                      <div class="muted">MATCH #{rank} · ADVISOR SCORE: {result['score']}</div>
                      <div class="destination-name">{p['emoji']} {p['name']}</div>
                      <p>{p['description']}</p>
                      <span class="tag">Approx. ₹{p['budget']:,} per person</span>
                      <span class="tag">{p['days']} suggested days</span>
                      <span class="tag">{', '.join(p['types'][:3])}</span>
                      <p><b>Best time to visit:</b> {p['best']}</p>
                      <p><b>Popular activities:</b> {p['activities']}</p>
                      <p><b>How to reach:</b> {p['transport']}</p>
                      <p class="muted"><b>Why recommended:</b> {'; '.join(result['reasons'])}.</p>
                    </div>
                    """, unsafe_allow_html=True)
                st.caption("Budgets are approximate estimates, not live prices. Check current transport, weather and accommodation before travelling.")
    else:
        st.markdown("""
        <div class="result-card" style="text-align:center;padding:42px 18px;">
          <div style="font-size:52px;">🧭</div>
          <h3 style="color:#102a43;">Your journey starts here</h3>
          <p class="muted">Choose your preferences and click <b>Find My Destinations</b> to see your recommendations.</p>
        </div>
        """, unsafe_allow_html=True)

st.divider()
st.subheader("⚙️ How This Expert System Works")
c1,c2,c3,c4 = st.columns(4)
with c1:
    st.markdown("### 1. Input")
    st.write("Collects budget, trip duration, season and interests.")
with c2:
    st.markdown("### 2. Knowledge Base")
    st.write("Stores destination budgets, seasons and activities.")
with c3:
    st.markdown("### 3. Rule Engine")
    st.write("Uses IF–THEN rules to compare preferences and calculate scores.")
with c4:
    st.markdown("### 4. Output")
    st.write("Ranks and displays the five best matching destinations.")

with st.expander("View example IF–THEN rules"):
    st.code("""
IF destination budget <= user's budget:
    Add 3 points
IF destination interest matches user's interest:
    Add 3 points for each match
IF selected season is suitable:
    Add 2 points
IF traveller type matches destination:
    Add extra points
Finally, sort by score and display the top 5 destinations.
""", language="text")

st.markdown("<p class='muted' style='text-align:center;margin-top:25px;'>TravelWise · Student Expert System Project · Built with Python and Streamlit</p>", unsafe_allow_html=True)
