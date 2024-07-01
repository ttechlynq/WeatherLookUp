import urllib.error
from django.shortcuts import render
from django.views.generic import TemplateView
import json
import urllib.request
import urllib.parse
from .forms import CityForm

def HomePage(request):

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = request.POST['city']
            encode_city = urllib.parse.quote(city)
            API_KEY = '218d42d6cdb2d6296942e17d81223078' 
            url = f'http://api.openweathermap.org/data/2.5/weather?q={encode_city}&appid={API_KEY}'
            try:
                weatherSource = urllib.request.urlopen(url).read()
                weatherInfo = json.loads(weatherSource)

                temp_kelvin = weatherInfo['main']['temp']
                temp_celsius = temp_kelvin - 273.15

                icon_code = weatherInfo['weather'][0]['icon']
                icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
                info = {
                    "country_code": str(weatherInfo['sys']['country']), 
                    "coordinate": str(weatherInfo['coord']['lon']) + ' ' + str(weatherInfo['coord']['lat']), 
                    "temp": f"{temp_celsius:.2f}°C",
                    "pressure": str(weatherInfo['main']['pressure']), 
                    "humidity": str(weatherInfo['main']['humidity']),
                    "icon_url": icon_url
                }
            
            except urllib.error.HTTPError as e:
                info = {'error': 'HTTP Error: {e.code}'}
            except urllib.error.URLError as e:
                info = {'error': f'URL Error: {e.reason}'}
            except json.JSONDecodeError:
                info = {'error': 'Error decoding the weather.'}
        else:
            info = {'error': 'Invalid form submission'}
            
    else:
        form = CityForm()
        info = {}
    context = {
        'form': form,
        'info': info
    }
    return render(request, 'home.html', context)

class AboutPage(TemplateView):
    template_name = 'about.html'