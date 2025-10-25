import streamlit as st
import pandas as pd  # Used only to display tables if needed, but not for core logic
from datetime import datetime

# --- 1. Data and Helper Functions ---

# Mock data structure mirroring the React component
WEATHER_DATA = {
    'London': {
        'current': {'temp': 18, 'condition': 'Partly Cloudy', 'humidity': 65, 'windSpeed': 12, 'visibility': 10,
                    'pressure': 1013, 'feelsLike': 16, 'icon': 'cloud'},
        'forecast': [
            {'day': 'Mon', 'high': 20, 'low': 14, 'condition': 'Sunny', 'icon': 'sun'},
            {'day': 'Tue', 'high': 19, 'low': 13, 'condition': 'Cloudy', 'icon': 'cloud'},
            {'day': 'Wed', 'high': 17, 'low': 12, 'condition': 'Rainy', 'icon': 'rain'},
            {'day': 'Thu', 'high': 18, 'low': 13, 'condition': 'Partly Cloudy', 'icon': 'cloud'},
            {'day': 'Fri', 'high': 21, 'low': 15, 'condition': 'Sunny', 'icon': 'sun'}
        ]
    },
    'Paris': {
        'current': {'temp': 22, 'condition': 'Sunny', 'humidity': 55, 'windSpeed': 8, 'visibility': 12,
                    'pressure': 1015, 'feelsLike': 21, 'icon': 'sun'},
        'forecast': [
            {'day': 'Mon', 'high': 24, 'low': 16, 'condition': 'Sunny', 'icon': 'sun'},
            {'day': 'Tue', 'high': 23, 'low': 17, 'condition': 'Sunny', 'icon': 'sun'},
            {'day': 'Wed', 'high': 21, 'low': 15, 'condition': 'Cloudy', 'icon': 'cloud'},
            {'day': 'Thu', 'high': 19, 'low': 14, 'condition': 'Rainy', 'icon': 'rain'},
            {'day': 'Fri', 'high': 20, 'low': 15, 'condition': 'Partly Cloudy', 'icon': 'cloud'}
        ]
    },
    'Tokyo': {
        'current': {'temp': 26, 'condition': 'Rainy', 'humidity': 80, 'windSpeed': 15, 'visibility': 6,
                    'pressure': 1010, 'feelsLike': 28, 'icon': 'rain'},
        'forecast': [
            {'day': 'Mon', 'high': 27, 'low': 22, 'condition': 'Rainy', 'icon': 'rain'},
            {'day': 'Tue', 'high': 28, 'low': 23, 'condition': 'Cloudy', 'icon': 'cloud'},
            {'day': 'Wed', 'high': 29, 'low': 24, 'condition': 'Partly Cloudy', 'icon': 'cloud'},
            {'day': 'Thu', 'high': 30, 'low': 25, 'condition': 'Sunny', 'icon': 'sun'},
            {'day': 'Fri', 'high': 29, 'low': 24, 'condition': 'Sunny', 'icon': 'sun'}
        ]
    },
    'New York': {
        'current': {'temp': 15, 'condition': 'Cloudy', 'humidity': 70, 'windSpeed': 18, 'visibility': 8,
                    'pressure': 1012, 'feelsLike': 13, 'icon': 'cloud'},
        'forecast': [
            {'day': 'Mon', 'high': 16, 'low': 10, 'condition': 'Cloudy', 'icon': 'cloud'},
            {'day': 'Tue', 'high': 14, 'low': 9, 'condition': 'Rainy', 'icon': 'rain'},
            {'day': 'Wed', 'high': 17, 'low': 11, 'condition': 'Partly Cloudy', 'icon': 'cloud'},
            {'day': 'Thu', 'high': 19, 'low': 13, 'condition': 'Sunny', 'icon': 'sun'},
            {'day': 'Fri', 'high': 20, 'low': 14, 'condition': 'Sunny', 'icon': 'sun'}
        ]
    },
    'Dubai': {
        'current': {'temp': 35, 'condition': 'Sunny', 'humidity': 45, 'windSpeed': 10, 'visibility': 15,
                    'pressure': 1008, 'feelsLike': 38, 'icon': 'sun'},
        'forecast': [
            {'day': 'Mon', 'high': 36, 'low': 28, 'condition': 'Sunny', 'icon': 'sun'},
            {'day': 'Tue', 'high': 37, 'low': 29, 'condition': 'Sunny', 'icon': 'sun'},
            {'day': 'Wed', 'high': 36, 'low': 28, 'condition': 'Sunny', 'icon': 'sun'},
            {'day': 'Thu', 'high': 35, 'low': 27, 'condition': 'Partly Cloudy', 'icon': 'cloud'},
            {'day': 'Fri', 'high': 34, 'low': 26, 'condition': 'Sunny', 'icon': 'sun'}
        ]
    }
}


def get_icon_html(icon_key, size='4rem'):
    """Returns an SVG/Emoji representing the weather condition."""
    # Using emojis for simplicity in Streamlit
    icons = {
        'sun': f'<span style="font-size: {size}; color: #FFD700;">☀️</span>',
        'cloud': f'<span style="font-size: {size}; color: #D3D3D3;">☁️</span>',
        'rain': f'<span style="font-size: {size}; color: #6495ED;">🌧️</span>'
    }
    return icons.get(icon_key, icons['cloud'])


def get_background_css(icon_key):
    """Returns CSS gradient based on weather condition."""
    gradients = {
        'sun': 'linear-gradient(135deg, #FFD700, #FFA500, #FF6347);',  # Yellow/Orange/Red
        'cloud': 'linear-gradient(135deg, #A9A9A9, #808080, #696969);',  # Grays
        'rain': 'linear-gradient(135deg, #1E90FF, #4682B4, #483D8B);'  # Blues/Purples
    }
    return gradients.get(icon_key, gradients['sun'])


# --- 2. Streamlit Layout and Logic ---

# Initialize Session State
if 'city' not in st.session_state:
    st.session_state.city = 'London'
if 'search_input' not in st.session_state:
    st.session_state.search_input = ''

st.set_page_config(layout="wide", page_title="Weather Dashboard")


# --- Search and Button Logic ---

def handle_search():
    """Handles the city search logic."""
    normalized_input = st.session_state.search_input.strip()
    matched_city = next(
        (c for c in WEATHER_DATA.keys() if c.lower() == normalized_input.lower()),
        None
    )
    if matched_city:
        st.session_state.city = matched_city
        st.session_state.search_input = ''  # Clear input
        st.toast(f"Switched to {matched_city}!")
    else:
        st.error(f"City '{normalized_input}' not found in mock data.")


def set_city_from_button(city_name):
    """Callback for quick-select buttons."""
    st.session_state.city = city_name


# --- Styling (Mimicking Tailwind/Glassmorphism) ---

current_data = WEATHER_DATA.get(st.session_state.city, WEATHER_DATA['London'])
bg_css = get_background_css(current_data['current']['icon'])

st.markdown(f"""
<style>
.stApp {{
    background: {bg_css};
    background-attachment: fixed;
    transition: background 1.0s ease-in-out;
}}
.glass-container {{
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 1rem;
    padding: 2rem;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.3);
    color: white;
    margin-bottom: 1.5rem;
}}
h1, h2, h3, h4, .stMarkdown p, .stMarkdown span {{
    color: white;
}}
</style>
""", unsafe_allow_html=True)


# --- Main Dashboard Component ---

def weather_dashboard_app():
    st.title("🌤️ Weather Dashboard")

    # 3-Column layout for search bar and button
    search_col, button_col = st.columns([4, 1])

    with search_col:
        st.text_input(
            "Search for a city:",
            key="search_input",
            placeholder="London, Paris, Tokyo, New York, Dubai...",
            label_visibility="collapsed"
        )
    with button_col:
        st.button("Search 🔍", on_click=handle_search, use_container_width=True)

    # Quick Select Buttons
    st.markdown("#### Quick Select Cities")
    button_cols = st.columns(len(WEATHER_DATA))
    for i, city_name in enumerate(WEATHER_DATA.keys()):
        button_cols[i].button(
            city_name,
            key=f"btn_{city_name}",
            on_click=set_city_from_button,
            args=(city_name,),
            type="primary" if st.session_state.city == city_name else "secondary",
            use_container_width=True
        )

    st.markdown("---")

    # --- Current Weather Section ---
    current = current_data['current']

    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown(f"### 📍 Current Weather in {st.session_state.city}", unsafe_allow_html=True)

    # Main Current Weather Display (2 columns)
    current_col_temp, current_col_metrics = st.columns([1, 2])

    with current_col_temp:
        st.markdown(f"""
            <div style='text-align: center; margin-top: 20px;'>
                {get_icon_html(current['icon'], size='6rem')}
                <div style='font-size: 4rem; font-weight: bold;'>{current['temp']}°C</div>
                <div style='font-size: 1.5rem;'>{current['condition']}</div>
                <div style='font-size: 1rem; color: rgba(255,255,255,0.7);'>Feels like {current['feelsLike']}°C</div>
            </div>
        """, unsafe_allow_html=True)

    with current_col_metrics:
        # Detailed Metrics Grid (2x2)
        metric_cols = st.columns(2)

        # Helper function for metric cards
        def display_metric(col, icon, label, value, unit):
            col.markdown(f"""
            <div style='background: rgba(255, 255, 255, 0.1); padding: 10px; border-radius: 10px; margin-bottom: 10px;'>
                <span style='font-size: 1rem; color: rgba(255,255,255,0.7);'>
                    {icon} {label}
                </span>
                <div style='font-size: 2rem; font-weight: bold;'>{value} {unit}</div>
            </div>
            """, unsafe_allow_html=True)

        display_metric(metric_cols[0], '💧', "Humidity", current['humidity'], "%")
        display_metric(metric_cols[1], '💨', "Wind Speed", current['windSpeed'], "km/h")
        display_metric(metric_cols[0], '👁️', "Visibility", current['visibility'], "km")
        display_metric(metric_cols[1], '🎚️', "Pressure", current['pressure'], "mb")

    st.markdown('</div>', unsafe_allow_html=True)  # Close glass-container

    # --- 5-Day Forecast Section ---
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown("### 🗓️ 5-Day Forecast", unsafe_allow_html=True)

    forecast_cols = st.columns(5)

    for i, day in enumerate(WEATHER_DATA[st.session_state.city]['forecast']):
        with forecast_cols[i]:
            st.markdown(f"""
            <div style='text-align: center; padding: 10px; border-radius: 10px; background: rgba(0, 0, 0, 0.2);'>
                <div style='font-weight: bold; margin-bottom: 5px;'>{day['day']}</div>
                {get_icon_html(day['icon'], size='3rem')}
                <div style='font-size: 0.9rem; color: rgba(255,255,255,0.9); margin: 5px 0;'>{day['condition']}</div>
                <div style='font-size: 1.1rem;'>
                    <span style='font-weight: bold;'>{day['high']}°</span> 
                    <span style='color: rgba(255,255,255,0.6);'>{day['low']}°</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # Close glass-container


if __name__ == '__main__':
    weather_dashboard_app()