from django.shortcuts import render


def redirect_blog(request):
    return render(request, 'weather/index', permanent=True)


