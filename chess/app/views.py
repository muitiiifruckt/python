from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from .game_logic import ChessLogic
from .game_logic import handle_move  # Предполагается, что у вас есть функция для обработки хода
import json


def make_move(request):
    try:
        data = json.loads(request.body.decode('utf-8'))  # Десериализация JSON из тела запроса
        from_coord = data.get('from')
        to_coord = data.get('to')
        move_result = handle_move(from_coord, to_coord)  # Обработка хода
        return JsonResponse(move_result)
    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
def index(request):
    return render(request, "html/index.html")
def game(request):
    return render(request, "html/game.html")

def about(request):
    return HttpResponse("<h2>Этот сайт является курсовой работой Муртазина Айзата Радиковича 09-141</h2>")

def news(request):
    return HttpResponse("<h2>NEWs</h2>")
def contact(request):
    return HttpResponse("<h2>Настройки</h2>")

