# Weather Risk & Operations Dashboard

A live weather analytics application that transforms current conditions and five-day forecast data into a clear operational risk assessment.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://weather-risk-operations-dashboard-irpxzg3hkgsrnt6skuslht.streamlit.app/)

**Live application:** [Launch the Weather Risk & Operations Dashboard](https://weather-risk-operations-dashboard-irpxzg3hkgsrnt6skuslht.streamlit.app/)

![Weather Risk & Operations Dashboard](assets/weather-dashboard.png)

## Project Overview

The Weather Risk & Operations Dashboard retrieves live weather data for a user-selected location and presents it through an interactive Streamlit interface.

Rather than functioning as a basic weather lookup tool, the application applies transparent, rule-based logic to identify potentially hazardous conditions such as extreme heat, freezing temperatures, strong winds, low visibility, thunderstorms, and other atmospheric hazards.

## Features

* Search by city, state, and country
* Retrieve live weather data through the OpenWeather API
* View temperature, feels-like temperature, humidity, wind speed, visibility, and atmospheric pressure
* Switch between Fahrenheit and Celsius
* Generate Low, Moderate, or High operational risk classifications
* Display the conditions responsible for an elevated risk level
* Explore a five-day forecast at three-hour intervals
* Compare temperature and feels-like temperature in an interactive Plotly chart
* Review daily minimum, maximum, and average temperatures
* View average daily humidity and dominant weather conditions
* Handle blank searches, invalid locations, API errors, and connection failures
* Protect API credentials using Streamlit secrets

## Technologies Used

* Python
* Streamlit
* pandas
* Plotly
* Requests
* OpenWeather Geocoding API
* OpenWeather Current Weather API
* OpenWeather Five-Day Forecast API
* Streamlit Community Cloud

## Operational Risk Assessment

The dashboard evaluates current weather conditions using a custom rule-based risk engine.

### High Risk

High-risk conditions may include:

* Dangerous heat index
* Extreme cold
* High wind speeds
* Severely restricted visibility
* Thunderstorms
* Squalls or tornado conditions

### Moderate Risk

Moderate-risk conditions may include:

* Elevated heat index
* Freezing temperatures
* Strong winds
* Reduced visibility
* Rain, snow, or drizzle
* Other atmospheric hazards

### Low Risk

A Low Risk classification indicates that none of the configured elevated-risk thresholds were detected.

The application displays the specific rule that triggered an elevated classification, making the assessment easier to understand and evaluate.

## Forecast Analytics

The OpenWeather forecast endpoint returns weather readings in three-hour intervals. The application converts these readings into a pandas DataFrame and calculates:

* Daily minimum temperature
* Daily maximum temperature
* Daily average temperature
* Daily average humidity
* Dominant daily weather conditions

Plotly is used to create an interactive five-day visualization comparing forecast temperature with the corresponding feels-like temperature.

## Project Structure

```text
Weather-Risk-Operations-Dashboard/
├── .streamlit/
│   └── secrets.toml
├── assets/
│   └── weather-dashboard.png
├── .gitignore
├── app.py
├── README.md
└── requirements.txt
```

The local `.streamlit/secrets.toml` file is excluded from version control and must never be uploaded to GitHub.

## Local Installation

Clone the repository:

```bash
git clone https://github.com/Roidneg/Weather-Risk-Operations-Dashboard.git
cd Weather-Risk-Operations-Dashboard
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Create a `.streamlit` directory inside the project folder. Within it, create a file named `secrets.toml`:

```toml
OPENWEATHER_API_KEY = "your_api_key_here"
```

You can obtain an API key from the [OpenWeather website](https://openweathermap.org/api).

Run the application:

```bash
streamlit run app.py
```

Streamlit will provide a local address that can be opened in a web browser.

## Deployment

The application is deployed through Streamlit Community Cloud:

https://weather-risk-operations-dashboard-irpxzg3hkgsrnt6skuslht.streamlit.app/

The API key is stored securely through Streamlit’s cloud secrets management and is not included in the repository.

## Testing

The application has been tested with:

* Valid and invalid locations
* Blank location searches
* Fahrenheit and Celsius measurements
* Multiple domestic and international locations
* Current-weather and forecast API responses
* Rule-based risk classifications
* Local and cloud deployments

## Future Improvements

Potential enhancements include:

* Official severe-weather alerts
* Downloadable forecast reports
* Search history
* Precipitation and wind visualizations
* Map-based weather exploration
* Automated unit testing
* Historical weather comparisons

## Disclaimer

This application is an educational portfolio project. Its operational risk assessment is generated through custom rules and should not be treated as an official meteorological warning, emergency alert, or safety recommendation.

Weather data is provided by [OpenWeather](https://openweathermap.org/).
