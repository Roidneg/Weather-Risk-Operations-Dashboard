# Weather Risk & Operations Dashboard

A live weather analytics dashboard that converts current conditions and five-day forecast data into an operational risk assessment.

Built with Python, Streamlit, pandas, Plotly, and the OpenWeather API.

![Weather Risk & Operations Dashboard](assets/weather-dashboard.png)

## Project Overview

The Weather Risk & Operations Dashboard retrieves live weather data for a user-selected location and presents it through an interactive web interface.

Rather than functioning as a basic weather lookup tool, the application applies transparent, rule-based logic to identify potentially hazardous conditions such as extreme heat, freezing temperatures, strong winds, low visibility, thunderstorms, and other atmospheric hazards.

## Features

* Search weather conditions by city, state, and country
* View live temperature, feels-like temperature, humidity, wind speed, visibility, and atmospheric pressure
* Switch between Fahrenheit and Celsius
* Generate a Low, Moderate, or High operational risk assessment
* Display the specific conditions responsible for elevated risk
* Explore a five-day forecast at three-hour intervals
* Compare forecast temperature with feels-like temperature
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

## Risk Assessment Logic

The dashboard uses a rule-based risk engine to classify current conditions.

### High Risk

Examples include:

* Dangerous heat index
* Extreme cold
* High wind speeds
* Severely restricted visibility
* Thunderstorms
* Squalls or tornado conditions

### Moderate Risk

Examples include:

* Elevated heat index
* Freezing temperatures
* Strong winds
* Reduced visibility
* Rain, snow, drizzle, or other atmospheric hazards

### Low Risk

A Low Risk classification indicates that none of the configured elevated-risk thresholds were detected.

The risk assessment is a portfolio demonstration and should not be treated as an official weather warning.

## Project Structure

```text
Weather Project Live API/
├── .streamlit/
│   └── secrets.toml
├── assets/
│   └── weather-dashboard.png
├── .gitignore
├── app.py
├── README.md
└── requirements.txt
```

The local `secrets.toml` file is excluded from version control and must not be uploaded to GitHub.

## Local Installation

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Create a `.streamlit` folder and add a `secrets.toml` file:

```toml
OPENWEATHER_API_KEY = "your_api_key_here"
```

Obtain an API key from the [OpenWeather website](https://openweathermap.org/api).

Run the application:

```bash
streamlit run app.py
```

Streamlit will provide a local address that can be opened in a web browser.

## Data Processing

The OpenWeather forecast endpoint returns weather readings in three-hour intervals. The application converts those readings into a pandas DataFrame and calculates:

* Daily minimum temperature
* Daily maximum temperature
* Daily average temperature
* Daily average humidity
* Dominant daily weather conditions

Plotly is used to visualize temperature and feels-like temperature across the forecast period.

## Testing

The application has been tested with:

* Valid locations
* Invalid locations
* Blank location searches
* Fahrenheit and Celsius measurements
* Multiple international locations
* Current-weather and forecast API responses

## Future Improvements

Potential enhancements include:

* Weather alerts from an official alert provider
* Downloadable forecast reports
* Location history
* Precipitation and wind visualizations
* Map-based weather exploration
* Automated testing
* Historical weather comparisons

## Disclaimer

This application is an educational portfolio project. Its operational risk assessment is generated through custom rules and is not an official meteorological warning or emergency alert.

Weather data is provided by [OpenWeather](https://openweathermap.org/).
