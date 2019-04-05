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