__A code will output the weather based on the date and location.__

__Requirements__

 Python 3.8.0 

__How to run__
1. create virtual env python -m venv .venv
2. activate virtual env . .venv/bin/activate
3. install dependencies pip install -r requirements.txt
4. get your credentials from https://www.visualcrossing.com/weather-api
5. Start the server using uWSGI: uwsgi --http 0.0.0.0:8000 --wsgi-file get_weather.py --callable app --processes 4 --threads 2 --stats 127.0.0.1:9191

__How to test__
1. Open Postman and create a new request.
2. In the URL field, enter the URL of your server and the path to your endpoint.
3. Choose the request method - POST.
4. In the Body tab, select the JSON data format and enter the required data such as token, name, location, and date.
