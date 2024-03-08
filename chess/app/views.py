from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, "index.html")
def game(request):
    return render(request, "game.html")

def about(request):
    return HttpResponse("<h2>Этот сайт является курсовой работой Муртазина Айзата Радиковича 09-141</h2>")

def news(request):
    return HttpResponse("<h2>NEWs</h2>")
def contact(request):
    return HttpResponse("<h2>Настройки</h2>")

