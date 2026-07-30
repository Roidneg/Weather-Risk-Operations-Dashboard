import pandas as pd
import plotly.express as px
import requests
import streamlit as st


st.set_page_config(
    page_title="Weather Risk Dashboard",
    page_icon="🌦️",
    layout="wide",
)

st.title("Weather Risk & Operations Dashboard")
st.write("Search for a location to retrieve current weather conditions.")

api_key = st.secrets["OPENWEATHER_API_KEY"]


def get_coordinates(location_query):
    response = requests.get(
        "https://api.openweathermap.org/geo/1.0/direct",
        params={
            "q": location_query,
            "limit": 1,
            "appid": api_key,
        },
        timeout=10,
    )

    if response.status_code != 200:
        return None, "The location service is currently unavailable."

    locations = response.json()

    if not locations:
        return None, "Location not found. Try adding a state or country."

    return locations[0], None


def get_current_weather(latitude, longitude, units):
    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={
            "lat": latitude,
            "lon": longitude,
            "appid": api_key,
            "units": units,
        },
        timeout=10,
    )

    if response.status_code != 200:
        return None, "Current weather data could not be retrieved."

    return response.json(), None

def get_forecast(latitude, longitude, units):
    url = "https://api.openweathermap.org/data/2.5/forecast"

    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": api_key,
        "units": units,
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 401:
            return None, "The OpenWeather API key was rejected."

        if response.status_code != 200:
            return None, (
                f"Forecast request failed with status "
                f"{response.status_code}."
            )

        forecast_data = response.json()
        forecast_rows = []

        for entry in forecast_data["list"]:
            forecast_rows.append(
                {
                    "Date and Time": pd.to_datetime(entry["dt"], unit="s"),
                    "Temperature": entry["main"]["temp"],
                    "Feels Like": entry["main"]["feels_like"],
                    "Humidity": entry["main"]["humidity"],
                    "Conditions": entry["weather"][0]["description"].title(),
                }
            )

        forecast_df = pd.DataFrame(forecast_rows)
        return forecast_df, None

    except requests.RequestException:
        return None, "Unable to connect to the forecast service."

def assess_weather_risk(weather, units):
    temperature = weather["main"]["temp"]
    feels_like = weather["main"]["feels_like"]
    wind_speed = weather["wind"]["speed"]
    visibility_miles = weather.get("visibility", 10000) / 1609.344
    weather_id = weather["weather"][0]["id"]

    if units == "metric":
        temperature = (temperature * 9 / 5) + 32
        feels_like = (feels_like * 9 / 5) + 32
        wind_speed = wind_speed * 2.23694

    high_risk_reasons = []
    moderate_risk_reasons = []

    # High-risk rules
    if feels_like >= 105:
        high_risk_reasons.append(
            f"Dangerous heat index of {feels_like:.1f}°F"
        )

    if temperature <= 10:
        high_risk_reasons.append(
            f"Extreme cold temperature of {temperature:.1f}°F"
        )

    if wind_speed >= 35:
        high_risk_reasons.append(
            f"High wind speed of {wind_speed:.1f} mph"
        )

    if visibility_miles < 1:
        high_risk_reasons.append(
            f"Visibility below one mile"
        )

    if 200 <= weather_id <= 232:
        high_risk_reasons.append("Thunderstorm conditions")

    if weather_id in [771, 781]:
        high_risk_reasons.append("Severe wind or tornado conditions")

    # Moderate-risk rules
    if 95 <= feels_like < 105:
        moderate_risk_reasons.append(
            f"Elevated heat index of {feels_like:.1f}°F"
        )

    if 10 < temperature <= 32:
        moderate_risk_reasons.append(
            f"Freezing temperature of {temperature:.1f}°F"
        )

    if 20 <= wind_speed < 35:
        moderate_risk_reasons.append(
            f"Elevated wind speed of {wind_speed:.1f} mph"
        )

    if 1 <= visibility_miles < 3:
        moderate_risk_reasons.append(
            f"Reduced visibility of {visibility_miles:.1f} miles"
        )

    if 300 <= weather_id <= 622:
        moderate_risk_reasons.append(
            "Rain, freezing precipitation, or snow"
        )

    if 701 <= weather_id <= 762:
        moderate_risk_reasons.append(
            "Atmospheric visibility hazard"
        )

    if high_risk_reasons:
        return "HIGH", high_risk_reasons

    if moderate_risk_reasons:
        return "MODERATE", moderate_risk_reasons

    return "LOW", ["No elevated conditions detected"]
    
with st.form("weather_search"):
    location_query = st.text_input(
        "Location",
        value="Shreveport, LA, US",
        help="Enter a city, state, and country when possible.",
    )

    unit_choice = st.selectbox(
        "Temperature units",
        options=["Fahrenheit", "Celsius"],
    )

    submitted = st.form_submit_button("Analyze Weather")


if submitted:
    if not location_query.strip():
        st.warning("Please enter a location.")
    else:
        units = "imperial" if unit_choice == "Fahrenheit" else "metric"
        temperature_symbol = "°F" if units == "imperial" else "°C"
        wind_unit = "mph" if units == "imperial" else "m/s"

        location, location_error = get_coordinates(location_query)

        if location_error:
            st.error(location_error)
        else:
            weather, weather_error = get_current_weather(
                location["lat"],
                location["lon"],
                units,
            )
            forecast, forecast_error = get_forecast(
                location["lat"],
                location["lon"],
                units,
            )

            if weather_error:
                st.error(weather_error)
            else:
                st.subheader(
                    f"{weather['name']}, {weather['sys']['country']}"
                )

                condition = weather["weather"][0]["description"].title()
                st.write(f"**Current conditions:** {condition}")
                risk_level, risk_reasons = assess_weather_risk(weather, units)

                st.subheader("Operational Risk Assessment")

                risk_message = f"{risk_level} RISK — " + "; ".join(risk_reasons)

                if risk_level == "HIGH":
                    st.error(risk_message)
                elif risk_level == "MODERATE":
                    st.warning(risk_message)
                else:
                    st.success(risk_message)

                st.caption(
                    "This rule-based assessment is a portfolio demonstration "
                    "and is not an official weather warning."
                )

                col1, col2, col3, col4 = st.columns(4)

                col1.metric(
                    "Temperature",
                    f"{weather['main']['temp']:.1f}{temperature_symbol}",
                )
                col2.metric(
                    "Feels Like",
                    f"{weather['main']['feels_like']:.1f}{temperature_symbol}",
                )
                col3.metric(
                    "Humidity",
                    f"{weather['main']['humidity']}%",
                )
                col4.metric(
                    "Wind Speed",
                    f"{weather['wind']['speed']:.1f} {wind_unit}",
                )

                col5, col6 = st.columns(2)

                col5.metric(
                    "Visibility",
                    f"{weather.get('visibility', 0) / 1000:.1f} km",
                )
                col6.metric(
                    "Atmospheric Pressure",
                    f"{weather['main']['pressure']} hPa",
                )
            st.divider()
            st.subheader("5-Day Temperature Forecast")

            if forecast_error:
                st.warning(forecast_error)

            elif forecast.empty:
                st.warning("No forecast data was returned.")

            else:
                forecast_chart = px.line(
                    forecast,
                    x="Date and Time",
                    y=["Temperature", "Feels Like"],
                    labels={
                        "value": f"Temperature ({temperature_symbol})",
                        "variable": "Measurement",
                    },
                    title="Temperature Trend at Three-Hour Intervals",
                    markers=True,
                )

                forecast_chart.update_layout(
                    hovermode="x unified",
                    legend_title_text="",
                    xaxis_title="Date and Time",
                    yaxis_title=f"Temperature ({temperature_symbol})",
                )

                st.plotly_chart(
                    forecast_chart,
                    use_container_width=True,
                )
                daily_forecast = (
                    forecast.assign(
                        Date=forecast["Date and Time"].dt.date
                    )
                    .groupby("Date", as_index=False)
                    .agg(
                        Minimum=("Temperature", "min"),
                        Maximum=("Temperature", "max"),
                        Average=("Temperature", "mean"),
                        Humidity=("Humidity", "mean"),
                        Conditions=(
                            "Conditions",
                            lambda values: values.mode().iloc[0],
                        ),
                    )
                )

                daily_forecast[
                    ["Minimum", "Maximum", "Average", "Humidity"]
                ] = daily_forecast[
                    ["Minimum", "Maximum", "Average", "Humidity"]
                ].round(1)

                daily_forecast = daily_forecast.rename(
                    columns={
                        "Minimum": f"Minimum ({temperature_symbol})",
                        "Maximum": f"Maximum ({temperature_symbol})",
                        "Average": f"Average ({temperature_symbol})",
                        "Humidity": "Average Humidity (%)",
                    }
                )

                st.subheader("Daily Forecast Summary")
                st.dataframe(
                    daily_forecast,
                    use_container_width=True,
                    hide_index=True,
                )

                st.success("Live weather data retrieved successfully.")
                st.caption("Weather data provided by OpenWeather.")
