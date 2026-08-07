import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Bengaluru Weather & AQI", page_icon="🌤️", layout="wide")

# Minimal CSS just to remove the huge blank space at the top
st.markdown("<style>.block-container { padding-top: 2rem; padding-bottom: 0rem; }</style>", unsafe_allow_html=True)

st.title("🌤️ Bengaluru Live Weather & Air Quality")
st.markdown("Automated Data Lake Pipeline | Updated every 6 hours")
st.divider()

# --- DATA LOADING ---
@st.cache_data(ttl=300)
def load_data():
    try:
        df = pd.read_csv("gold/master_air_quality.csv")
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception:
        return None

# --- GAUGE GENERATOR ---
def create_gauge(value, max_val, title):
    """Creates a beautiful, perfectly sized speedometer gauge."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number", 
        value=value, 
        title={'text': title, 'font': {'size': 20, 'color': 'white'}},
        number={'font': {'color': 'white'}, 'valueformat': ".1f" if max_val < 150 else "d"},
        gauge={
            'axis': {'range': [None, max_val], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "rgba(255, 255, 255, 0.9)", 'thickness': 0.15},
            'steps': [
                {'range': [0, max_val * 0.33], 'color': "#00E400"},   # Green (Good)
                {'range': [max_val * 0.33, max_val * 0.66], 'color': "#FFFF00"}, # Yellow (Moderate)
                {'range': [max_val * 0.66, max_val], 'color': "#FF7E00"} # Orange (Unhealthy)
            ],
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 0
        }
    ))
    
    # Make the background transparent so it blends with dark mode
    fig.update_layout(
        height=220, 
        margin=dict(l=20, r=20, t=40, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

# --- MAIN APP ---
df = load_data()

if df is not None and not df.empty:
    latest = df.iloc[-1]
    
    # ROW 1: Weather Metrics (Clean and simple)
    st.subheader("🌡️ Current Weather")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Location", latest['location'])
    c2.metric("Last Updated", latest['timestamp'].strftime("%b %d, %H:%M"))
    c3.metric("Temperature", f"{latest['temperature_c']} °C")
    c4.metric("Relative Humidity", f"{latest['humidity_pct']} %")
    
    st.write("") # Spacer

    # ROW 2: Air Quality Gauges (The visual centerpieces)
    st.subheader("🌬️ Air Quality Indices")
    g1, g2, g3 = st.columns(3)
    
    with g1:
        st.plotly_chart(create_gauge(latest['official_aqi'], 150, "US AQI"), use_container_width=True)
    with g2:
        st.plotly_chart(create_gauge(latest['pm25_level'], 50, "PM 2.5 (µg/m³)"), use_container_width=True)
    with g3:
        st.plotly_chart(create_gauge(latest['pm10_level'], 100, "PM 10 (µg/m³)"), use_container_width=True)

    # ROW 3: Historical Trends
    st.divider()
    st.subheader("📈 Historical Trends")
    if len(df) > 1:
        st.line_chart(data=df, x="timestamp", y=["official_aqi", "temperature_c"], height=250)
    else:
        st.info("📊 The trend chart will automatically draw a line here as soon as your GitHub Action runs for the second time!")

else:
    st.error("Pipeline failure: Unable to locate 'gold/master_air_quality.csv'.")