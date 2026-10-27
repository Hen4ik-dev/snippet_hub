from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.db.models import Q
from .forms import SignUpForm, SnippetCreateForm, SnippetsSearch
from .models import Snippet


# Create your views here.
def index(request):
    snippets = Snippet.objects.filter(is_private = False).order_by('-created_at')[:10]
    return render(request, "index.html", context = {"snippets" : snippets})


@login_required
def create_snippet(request):
    if request.method == "POST":
        form = SnippetCreateForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.author = request.user
            snippet.save()
            form.save_m2m()
            return redirect("snippet_detail", id=snippet.id)

    else:
        form = SnippetCreateForm()
    return render(request, "mainapp/create_snippet.html", context={"form": form})


@login_required
def main_snippets(request):
    snippets = Snippet.objects.filter(author=request.user).all()
    print(snippets)
    return render(request, "mainapp/snippets_page.html", context={"snippets": snippets})


@login_required
def snippet_detail(request, id):
    if request.method == "POST":
        snippet = Snippet.objects.filter(id=id).first()
        if snippet:
            snippet.delete()
            return redirect("main_snippets")
        return render(request, "mainapp/error_page.html", context={"error_message": "сниппет не найден"})
    else:
        snippet = Snippet.objects.filter(id=id).first()
        if snippet:
            if snippet.author != request.user and snippet.is_private:
                return render(request, "mainapp/error_page.html", context={"error_message": "доступ запрещен"})
        else:
            return redirect("index")
        return render(request, "mainapp/snippet_detail.html", context={"snippet": snippet})


@login_required
def snippet_update(request, id):
    snippet = Snippet.objects.filter(id=id).first()
    if snippet:
        if snippet.author != request.user:
            return render(request, "mainapp/error_page.html", context={"error_message": "Доступ запрещен"})
    else:
        return redirect("index")
    if request.method == "POST":
        form = SnippetCreateForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            #form.save_m2m()
            return redirect("snippet_detail", id=snippet.id)

    else:
        form = SnippetCreateForm(
            initial={
                "title": snippet.title,
                "content": snippet.content,
                #"tags": snippet.tags,
                "language": snippet.language,
                "is_private": snippet.is_private
            }
        )
    return render(request, "mainapp/edit_snippet.html", context={"form": form})


def sign_up(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("app1:index")

    else:
        form = SignUpForm()
    return render(request, "registration/sign_up.html", {"form": form})

@login_required
def profile(request):
    return render(request, "registration/profile.html")

def search_snippets(request):
    if request.method == "POST":
        form = SnippetsSearch(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            requierd = Q(is_private = False)
            optional = Q()
            if data.get("title"):
                optional |= Q(title__icontains = data.get("title"))
            if data.get("content"):
                optional |= Q(content__icontains = data.get("content"))
            if data.get("language"):
                optional |= Q(language__icontains = data.get("language"))
            if optional:
                snippets = Snippet.objects.filter(requierd & optional).all()
            else:
                snippets = Snippet.objects.filter(requierd).all()
            return render(request, "mainapp/search_snippets_results.html", context={"snippets": snippets})
    else:
        form = SnippetsSearch()
    return render(request, "mainapp/search_snippets.html", context={"form": form})

