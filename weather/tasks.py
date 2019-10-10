from blogengine.celery import app
from .models import City
import requests


app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'weather.tasks.take_temp',
        'schedule': 299.0,
        'args': []
    },
}
app.conf.timezone = 'UTC'

@app.task
def take_temp():
    appid = '8d11f7124dbdaaeb041949a8c9f55860'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid
    cities = City.objects.all()

    for city in cities:
        res = requests.get(url.format(city.name)).json()
        city.temp = res['main']['temp']
        city.img = res['weather'][0]['icon']
        city.save()
