import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
from prophet import Prophet
import altair as alt

# ✅ Function 1: Fetch Past 1-Year Weather Data
@st.cache_data(ttl=86400)
def fetch_weather(api_key, location, days=365):
    end_date = datetime.today() - timedelta(days=1)
    start_date = end_date - timedelta(days=days)

    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{start_date.date()}/{end_date.date()}?unitGroup=metric&key={api_key}&include=days&contentType=csv"
    response = requests.get(url)
    if response.status_code == 200:
        from io import StringIO
        df = pd.read_csv(StringIO(response.text))
        return df
    else:
        st.error("API Error: " + response.text)
        return None

# ✅ Function 2: Forecast

def forecast_weather(df, forecast_days):
    # Temperature
    df_temp = df[['datetime', 'temp']].rename(columns={'datetime': 'ds', 'temp': 'y'})
    model_temp = Prophet()
    model_temp.fit(df_temp)
    future_temp = model_temp.make_future_dataframe(periods=forecast_days)
    forecast_temp = model_temp.predict(future_temp)

    # Rain
    df_rain = df[['datetime', 'precip']].rename(columns={'datetime': 'ds', 'precip': 'y'})
    model_rain = Prophet()
    model_rain.fit(df_rain)
    future_rain = model_rain.make_future_dataframe(periods=forecast_days)
    forecast_rain = model_rain.predict(future_rain)

    # Combine
    forecast = pd.DataFrame({
        'date': forecast_temp['ds'].tail(forecast_days),
        'pred_temp': forecast_temp['yhat'].tail(forecast_days).round(1),
        'pred_rain': forecast_rain['yhat'].tail(forecast_days).round(1)
    })
    return forecast

# ✅ Function 3: Outfits + Icons

def suggest_outfits(df_forecast):
    def rule(temp, rain):
        if temp < 20:
            return "🧥 Jacket"
        elif 20 <= temp <= 30:
            if rain >= 5:
                return "🌧️ Raincoat, umbrella, waterproof shoes"
            else:
                return "👕 T-shirt and jeans"
        else:
            return "🩳 Shorts, sunglasses"

    df_forecast['outfit'] = df_forecast.apply(lambda row: rule(row['pred_temp'], row['pred_rain']), axis=1)
    return df_forecast


# ✅ Streamlit App

st.set_page_config(page_title="Weather + Outfit Planner", page_icon="🌦️", layout="wide")
st.title("🌦️ Dynamic Weather Forecast + Outfit Planner")

api_key = st.text_input("🔑 Enter Visual Crossing API Key", type="password")
location = st.text_input("📍 Enter Location (e.g., Bengaluru,India)", value="Bengaluru,India")
forecast_days = st.selectbox("📅 Days to Forecast", [7, 14, 30, 60, 90], index=2)

if st.button("🚀 Fetch & Predict"):
    if api_key and location:
        with st.spinner("Fetching past 1 year data..."):
            df_weather = fetch_weather(api_key, location)
            if df_weather is not None:
                st.success("✅ Data fetched!")

                st.subheader("🕒 Past 7 Days Real Weather")
                st.dataframe(df_weather.tail(7))

                with st.spinner("Training + predicting..."):
                    forecast = forecast_weather(df_weather, forecast_days)
                    forecast_with_outfit = suggest_outfits(forecast)

                    st.success("✅ Forecast ready!")

                    st.subheader("👕 Outfit Planner")
                    st.dataframe(forecast_with_outfit)

                    st.subheader("📊 Forecast Chart")
                    chart = alt.Chart(forecast_with_outfit).transform_fold(
                        ["pred_temp", "pred_rain"]
                    ).mark_line().encode(
                        x='date:T',
                        y='value:Q',
                        color='key:N'
                    )
                    st.altair_chart(chart, use_container_width=True)

    else:
        st.warning("Please enter API key and location!")
