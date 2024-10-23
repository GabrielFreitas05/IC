from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render

def home(request):
    return render(request, 'core/simple.html')



def registrar_usuario(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        try:
            user = User.objects.create_user(username=email, email=email, password=senha)
            messages.success(request, 'Registro realizado com sucesso!')
            return redirect('login')
        except:
            messages.error(request, 'Erro ao registrar. E-mail já utilizado.')
    return render(request, 'registrar.html')

def login_usuario(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        user = authenticate(username=email, password=senha)
        if user:
            login(request, user)
            return redirect('tela_usuario')
        else:
            messages.error(request, 'Login ou senha incorretos.')
    return render(request, 'login.html')
from django.http import HttpResponse

