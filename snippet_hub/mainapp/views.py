from django.shortcuts import render, redirect
from .models import Snippet
from .forms import SnippetCreateForm

# Create your views here.
def index(request):
    return render(request, 'index.html')

def create_snippet(request):
    if request.method == "POST":
        form = SnippetCreateForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.author = request.user
            snippet.save()
            form.save_m2m()
            #TODO: redirect(to snippet)
            return redirect('index')
    else:
        form = SnippetCreateForm()
    return render(request, 'mainapp/create_snippet.html', context = {'form':form})