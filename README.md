# weather_api_script

*Pull Weather Data from metaweather api and save to database and to csv files*

You are asked to pick a city and a date and if they are valid you get the weather data back from the metaweather API.


## Installation

1. Download this repository
2. `cd` into repository directory
3. Run `python weather_api.py` to run the script.
4. The repository comes with an empty database ready to use. If you want to delete that database and start over. Simply create a new database instance with db = DataBase(), and then run db.createDataBase().



## Usage
1. Enter a Valid city
2. Enter a Valid Date
3. The script will do the following:
4. Add the raw data to the DataBase
5. Create a CSV file for the consolidated weather information for the city
6. Create a CSV file that is a snapshot of the current database
7. Create a JSON file of the raw data from the API

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/seanoughton/meta_weather_api.

## License

The app is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).

## Code of Conduct
This project is intended to be a safe, welcoming space for collaboration, and contributors are expected to adhere to the [Contributor Covenant](http://contributor-covenant.org) code of conduct.
