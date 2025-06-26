INSTALLATION_POWER_KW = 2.5
PANEL_EFFICIENCY = 0.2
WMO_CODE_CATEGORY = {
    # Sunny
    0: "sunny",
    # Cloudy
    1: "cloudy",
    2: "cloudy",
    3: "cloudy",
    # Fog
    45: "cloudy",
    48: "cloudy",
    # Drizzle
    51: "rainy",
    53: "rainy",
    55: "rainy",
    # Freezing drizzle
    56: "rainy",
    57: "rainy",
    # Rain
    61: "rainy",
    63: "rainy",
    65: "rainy",
    # Freezing rain
    66: "rainy",
    67: "rainy",
    # Snow fall
    71: "snowy",
    73: "snowy",
    75: "snowy",
    # Snow grains
    77: "snowy",
    # Rain showers
    80: "rainy",
    81: "rainy",
    82: "rainy",
    # Snow showers
    85: "snowy",
    86: "snowy",
    # Thunderstorm
    95: "rainy",
    # Thunderstorm with hail
    96: "rainy",
    99: "rainy",
}

CODE_CATEGORY_TO_VERB = {"snowy": "snowing", "rainy": "raining"}
