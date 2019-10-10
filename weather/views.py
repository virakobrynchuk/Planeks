from django.shortcuts import render
from .models import City
from .forms import CityForm


# Create your views here.
def index_html(request):

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    all_cities = []

    for city in cities:
        city_info = {'city': city.name, 'temp': city.temp, 'icon': city.img}
        all_cities.append(city_info)

    context = {'all_info': all_cities}

    return render(request, 'weather/index.html', context)


