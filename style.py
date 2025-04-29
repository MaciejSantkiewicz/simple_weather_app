style = """
    WeatherApp {
        background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 lightblue,   
        stop: 1 white   
        );
        color: black;
        font-family: Calibri, sans-serif;
    }

    QLabel#city_label {
        font-size: 20px;
        font-style: italic;
        color: black;
    }

    QLineEdit#city_input {
        font-size: 20px;
        padding: 6px;
        border: 1px solid #90caf9;
        border-radius: 6px;
        background-color: #ffffff;
    }

    QPushButton#get_weather_button {
        font-size: 22px;
        font-weight: bold;
        padding: 10px 10px;
        background-color: #2196f3;
        color: white;
        border: none;
        border-radius: 6px;
    }

    QPushButton#get_weather_button:hover {
        background-color: #1976d2;
    }

    QLabel#temperture_label {
        font-size: 55px;
        color: black;
        font-weight: bold;
    }

    QLabel#location {
        font-size: 15px;
        color: black;
    }

    
    QLabel#temperature_label_f {
        font-size: 15px;
        color: black;
    }

    QLabel#emoji_label {
        font-size: 100px;
        font-family: "Segoe UI Emoji", "Segoe UI Symbol", sans-serif;
    }

    QLabel#description_label {
        font-size: 24px;
        color: black;
    }

    
"""
