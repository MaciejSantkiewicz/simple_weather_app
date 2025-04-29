import sys
import requests

from style import style #CSS style file for formating the widets
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                                                       QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt, QSettings



class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        
       
      
        #APP Widgets
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Check Weather", self)
        self.location = QLabel(self)
        self.temperature_label = QLabel(self)
        self.temperature_label_f = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)

        #Invoking the UI
        self.initUI()

        #Creating the settings
        self.settings = QSettings("Weather", "WeatherApp")
        
        #Loading the last searched city 
        last_city = self.settings.value("last_city", "")
        self.city_input.setText(last_city)
        if last_city:
            self.get_weather()

    #UI setup
    def initUI(self):

        #Setting basics of the window the position to be on the middle of the screen
        self.setWindowTitle("Weather app")
        self.resize(400, 300)
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)  

        #Creating layout of Widgets
        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.location)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.temperature_label_f)
        
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        
        #Invoking the layout
        self.setLayout(vbox)
      
        
        #Adjustment to the layout
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.location.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.temperature_label_f.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        
        
        #Naming the styles for each widget
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.temperature_label.setObjectName("temperture_label")
        self.emoji_label.setObjectName("emoji_label")
        self.get_weather_button.setObjectName("get_weather_button")
        self.description_label.setObjectName("description_label")
        self.temperature_label_f.setObjectName("temperature_label_f")
        self.location.setObjectName("location")
       
        #Getting the settings of the formationg from style.py file
        self.setStyleSheet(style)
        
        #Connecting button to get weather function 
        self.get_weather_button.clicked.connect(self.get_weather)
        #Setting that allows to click button with Enter key
        self.city_input.returnPressed.connect(self.get_weather)
        
    #Main function
    def get_weather(self):
        #https://api.openweathermap.org - registration is required to get th API key
        api_key = "" #paste the API key here

        #Configuration the http request to API
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    

        #Getting the response
        try:
          response = requests.get(url)

          response.raise_for_status()

          data = response.json()
          if data["cod"] == 200:
              self.display_weather(data)

        #Error handling - it will apear in the app if user or app finds an error
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nPlease check your API credentials")
                case 403:
                    self.display_error("Forbidden:\nAccess is denied")
                case 404:
                    self.display_error("Not found:\nCity not Found")
                case 500:
                    self.display_error("Internal Sever Error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_error("Service unavailabel:\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occured:\{http_error}")
        
        except requests.exceptions.ConnectionError:
            self.display_error("Connection error:\nCheck your internet connection")
        
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")

        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck the URL")
        
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request error:{req_error}")

        
       
    #Function to show the error
    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 15px; color: red")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()
        self.temperature_label_f.clear()
        self.location.clear()
    
    #Function to update the widget from the JSON file we get from weather API
    def display_weather(self, data):
        
        self.temperature_label.setStyleSheet("font-size: 55px")
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        temperature_f = (temperature_k * 9/5) -459.67

        weather_id = weather_description = data["weather"][0]["id"]
        city = data["name"]
        country = data["sys"]["country"]

        local_daytime = data['dt']
        
        weather_description = data["weather"][0]["description"]

        self.settings.setValue("last_city", city) #saving the last searched city to settings

        self.temperature_label.setText(f"{temperature_c:.1f}°C")
        self.temperature_label_f.setText(f"{temperature_f:.1f}°F")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(f"{weather_description.capitalize()}")
        self.location.setText(f"{city},{country}")
        
    #Setting up the correct emoji to show up based on the id of the weather we get from the API
    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "⛅"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "🌨️"
        elif 700 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""
        
#Lunching the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())