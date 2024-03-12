from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from .game_logic import ChessLogic


# Предполагается, что используется AJAX для передачи хода
def make_move(request):
    if request.method == 'POST':
        move = request.POST.get('move')
        game_id = request.POST.get('game_id')
        # Здесь должна быть логика для поиска соответствующей игры

        chess_logic = ChessLogic()  # Создать новый экземпляр логики шахмат
        if chess_logic.make_move(move):
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid move'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


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

