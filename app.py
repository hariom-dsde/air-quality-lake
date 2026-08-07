import streamlit as st
import pandas as pd

# 1. Set up the page title
st.set_page_config(page_title="Bengaluru Air Quality", page_icon="🌤️")
st.title("Bengaluru Live Air Quality Dashboard 🌤️")
st.markdown("This dashboard automatically pulls live data from our Data Lake's Gold Layer.")

# 2. Load the data from our Gold folder
@st.cache_data # This makes the app run faster by caching the data
def load_data():
    try:
        # We use Pandas to read the master CSV file
        df = pd.read_csv("gold/master_air_quality.csv")
        # Convert the timestamp string into a real date object so the chart looks nice
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception as e:
        return None

df = load_data()

# 3. Build the user interface
if df is not None and not df.empty:
    # Show the raw data table
    st.subheader("Raw Data (Gold Layer)")
    st.dataframe(df)
    
    # Create a line chart showing pollution over time
    st.subheader("Pollution Trends")
    st.line_chart(
        data=df,
        x="timestamp", 
        y=["pm10_level", "pm25_level"] # Plots both lines on the same graph
    )
    
    # Show the most recent reading
    latest = df.iloc[-1]
    st.metric(label="Latest PM2.5", value=latest['pm25_level'])
    
else:
    st.error("No data found in the Gold layer yet! Make sure your pipeline has run.")