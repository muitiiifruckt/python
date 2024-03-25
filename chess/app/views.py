from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from .game_logic import ChessLogic
from .game_logic import handle_move  # Предполагается, что у вас есть функция для обработки хода


def make_move(request):
    if request.method == 'POST':
        from_coord = request.POST.get('from')
        to_coord = request.POST.get('to')
        # Вызов функции для обработки хода
        move_result = handle_move(from_coord, to_coord)
        return JsonResponse(move_result)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)
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

