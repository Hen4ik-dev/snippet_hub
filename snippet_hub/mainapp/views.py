from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import SignUpForm, SnippetCreateForm
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
    snippet = Snippet.objects.filter(id=id).first()
    if snippet:
        if snippet.author != request.user and snippet.is_private:
            return render(request, "mainapp/error_access_denied.html")
    else:
        return redirect("index")
    return render(request, "mainapp/snippet_detail.html", context={"snippet": snippet})


@login_required
def snippet_update(request, id):
    snippet = Snippet.objects.filter(id=id).first()
    if snippet:
        if snippet.author != request.user:
            return render(request, "mainapp/error_access_denied.html")
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
