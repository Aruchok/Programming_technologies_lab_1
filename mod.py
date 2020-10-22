import requests
import sqlite3
from sqlalchemy import create_engine, Table, Column, String, Float, MetaData
from sqlalchemy.sql import select
response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Volgograd&appid=3a25edb8b1d5f13a36e4cbd2af97e515")

class WeatherProvider:
    def __init__(self, key):
        self.key = key

    def get_data(self):
        url = 'http://api.openweathermap.org/data/2.5/weather?q=Volgograd&appid=3a25edb8b1d5f13a36e4cbd2af97e515'
        data = requests.get(url).json()
        return [
            {
                'Temp':data['main']['temp'],
                'Feels_like':data['main']['feels_like'],
                'Temp_min':data['main']['temp_min'],
                'Temp_max':data['main']['temp_max'],
                'Humidity':data['main']['humidity'],
            }
        ]


def db_meth(str_conn, data_name):

    engine = create_engine(str_conn)
    metadata = MetaData()
    weather = Table(
        data_name,
        metadata,
        Column('Temp', Float),
        Column('Feels_like', Float),
        Column('Temp_min', Float),
        Column('Temp_max', Float),
        Column('Humidity', Float),
    )
    return engine, metadata, weather

engine, metadata, weather = db_meth('sqlite:///weather.sqlite3', 'weather_data')

metadata.create_all(engine)
c = engine.connect()

provider = WeatherProvider('3a25edb8b1d5f13a36e4cbd2af97e515')
c.execute(weather.insert(), provider.get_data())

for row in c.execute(select([weather])):
    print(row)

# weather_json = response.json()

# Temp = weather_json['main']['temp']
# Feels_like = weather_json['main']['feels_like']
# Temp_min = weather_json['main']['temp_min']
# Temp_max = weather_json['main']['temp_max']
# Wind_speed = weather_json['wind']['speed']
# Humidity = weather_json['main']['humidity']

# result = [(Temp - 273.15, Feels_like - 273.15, Temp_min - 273.15, Temp_max - 273.15, Wind_speed, Humidity)]

# connect = sqlite3.connect("weather_data.db")
# cursor = connect.cursor()

# cursor.execute("""CREATE TABLE weather
#                   (Temp float, Feels_like float, Temp_min float,
#                    Temp_max float, Wind_speed float, Humidity float)
#                """)
# cursor.executemany("INSERT INTO weather VALUES (?,?,?,?,?,?)", result)
# connect.commit()

# print("Температура = ", result[0][0], "Чувствуется = ", result[0][1], "Максимальная = ", result[0][2], 
#       "Минимальная = ", result[0][3], "Скорость ветра = ", result[0][4], "Давление = ", result[0][5])

