from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def signup(request):
	form = UserCreationForm(request.POST or None)
	if form.is_valid():
		form.save()

	return render(request, 'nuevousuario.html', {'form': form})