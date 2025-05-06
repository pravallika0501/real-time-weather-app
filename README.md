# 🌦️ Weather + Outfit Planner App

A dynamic Streamlit web app that fetches **real past 1-year weather data** for your location, trains forecasting models, predicts the next 7/14/30/60/90 days, and **suggests outfits** based on the forecast (with emojis 🧥👕🩳🌧️).

✅ **Dynamic, Live Data** (No static old CSVs!)  
✅ **Prophet models** forecast temperature & rainfall  
✅ **Outfit planner** with smart suggestions  
✅ **Interactive charts** and clean table views  

---

## 🚀 Live Demo Flow

1. **User Inputs:**
   - Visual Crossing API Key (free key works!)
   - Location (e.g., `Bengaluru,India`)
   - Days to forecast (7, 14, 30, 60, 90)

2. **App Does:**
   - Pulls **past 365 days weather** up to yesterday
   - Trains Prophet models (temperature + rainfall)
   - Predicts next days
   - Suggests daily outfits (using simple logic)
   - Displays chart + data

---

## 📝 How to Run This App

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/weather-outfit-planner.git
cd weather-outfit-planner

### 2. Install Requirements
pip install -r requirements.txt

### 3. Get Free API Key
Sign up at Visual Crossing Weather API ✅
Copy your API key (free tier gives 1000+ calls per day)

### 4. Run the App
streamlit run app.py


## ✅ Folder Structure

weather-outfit-planner/
├── app.py              
├── requirements.txt    
└── README.md   


## 📦 Tech Stack

Streamlit (Web App Framework)
Prophet (Time Series Forecasting)
Visual Crossing API (Weather data source)
Altair (Charts)

