from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from .game_logic import ChessLogic
from .game_logic import handle_move  # Предполагается, что у вас есть функция для обработки хода
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

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
def signup(request):
    # ваш код для обработки запроса регистрации
    return render(request, 'templates/registration/login.html')
def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # получаем имя пользователя и пароль из формы
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # выполняем аутентификацию
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

