import requests,json,csv,sqlite3,datetime
from datetime import date

class UserInteraction():
    def __init__(self,woied=0,city='',user_date=''):
        self.woied = woied
        self.city = city
        self.user_date = user_date

    def isDateValid(self,user_date):
        today = date.today()
        try:
            newDate = datetime.datetime(int(user_date[0]),int(user_date[1]),int(user_date[2]))
            return True
        except ValueError:
            return False
        else:
            if datetime.date(int(user_date[0]), int(user_date[1]), int(user_date[2])) > today:
                return False
            else:
                return True

    def getDate(self):
        user_date = '2025,15,45'.split(',')
        user_input = input("What date would you like to see the weather for? (Year,Month,Day)")
        user_date = user_input.split(',')
        while True:
            if self.isDateValid(user_date) == False:
                user_input = input("Please enter a valid date in the format (Year,Month,Day)")
                user_date = user_input.split(',')
            else:
                break
        self.user_date = user_date

    def isCityValid(self,data):
        if data == []:
            return False
        elif len(data)>1:
            return False
        else:
            return True

    def getCityData(self,city):
        url = f"https://www.metaweather.com/api/location/search/?query={city}"
        r = requests.get(url)
        return json.loads(r.content)

    def getCity(self):
        city = input('What city would you like to see the weather for?').lower()
        data = self.getCityData(city)
        while True:
            if self.isCityValid(data) == False:
                city = input('That is not a valid city or it is not in the database. Please enter a valid city.').lower()
                data = self.getCityData(city)
            else:
                break
        self.city = city.replace(" ","_")
        self.woied = data[0]['woeid']

    def isThereWeatherData(self,data):
        if len(data) == 0:
            return False
        else:
            return True


class API():
    def __init__(self,woied='',user_date='',location_day_weather_data=[],consolidated_weather_data=[]):
        self.woied = woied
        self.user_date = user_date
        self.location_day_weather_data = location_day_weather_data
        self.consolidated_weather_data = consolidated_weather_data

    def getLocationDayData(self):
        date_dict = {'year':self.user_date[0],'month':self.user_date[1],'day':self.user_date[2]}
        url = f"https://www.metaweather.com/api/location/{self.woied}/{date_dict['year']}/{date_dict['month']}/{date_dict['day']}"
        r = requests.get(url)
        data = json.loads(r.content)
        self.location_day_weather_data = data

    def getConsolidatedWeather(self):
        url = f"https://www.metaweather.com/api/location/{self.woied}/"
        r = requests.get(url)
        data = json.loads(r.content)
        self.consolidated_weather_data = data['consolidated_weather']


class DataBase():
    def __init__(self,conn=''):
        self.conn = sqlite3.connect('metaweather.db')

    def createDataBase(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE weatherdata
                     (woeid integer,
                     air_pressure text,
                     applicable_date text,
                     created text,
                     humidity integer,
                     id integer,
                     max_temp real,
                     min_temp real,
                     predictability integer,
                     the_temp real,
                     visibility real,
                     weather_state_abbr text,
                     weather_state_name text,
                     wind_direction real,
                     wind_direction_compass text,
                     wind_speed real)''')

    def formatDataForDb(self,data,woeid):
        formatted_data = []
        key_list = list(sorted(data[0].keys()))
        for item in data:
            row = [woeid]
            for key in key_list:
                row.append(item[key])
            formatted_data.append(tuple(row))
        return formatted_data

    def addToDatabase(self,data,woied):
        c = self.conn.cursor()
        weather_data = self.formatDataForDb(data,woied)
        c.executemany('INSERT INTO weatherdata VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', weather_data)
        self.conn.commit()
        self.conn.close()


class JSON():
    def saveRawData(self,data,city):
        with open(f"weather_{data[0]['applicable_date']}_{city}.json", 'w') as d:
            json.dump(data, d, indent = 4, sort_keys = True)

class CSV():
    def consolidatedWeatherToCSV(self,data,city):
        with open(f"weather_data_{data[0]['applicable_date']}_{city}.csv", mode='w') as csv_file:
            fieldnames = list(data[0].keys())
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            length_data = len(data) - 1

            for i in range(0,length_data):
                row = tuple(list(data[i].values()))
                csv_data = dict(zip(tuple(fieldnames),row))
                writer.writerow(csv_data)

    def dbToCSV(self,data):
        conn = sqlite3.connect('metaweather.db')
        c = conn.cursor()
        c.execute('SELECT * FROM weatherdata LIMIT 1')
        fieldnames = [description[0] for description in c.description]
        today_date = str(datetime.datetime.now())[:10]
        with open(f"database_export_{today_date}.csv", mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for row in c.execute('SELECT * FROM weatherdata ORDER BY created'):
                data = dict(zip(tuple(fieldnames),row))
                writer.writerow(data)
