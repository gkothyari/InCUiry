from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Answer
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Post, Answer


def home(request):
    context = {"posts": Post.objects.all()}
    return render(request, "blog/home.html", context)


class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"  # <app>/<model>_<viewtype>.html
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_posts.html"  # <app>/<model>_<viewtype>.html
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-date_posted")


class PostDetailView(DetailView):
    model = Post
    fields = ["answers"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        user = self.request.user
        Answer.objects.create(form.instance)
        return super().form_valid(form)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# class AddAnswerView(LoginRequiredMixin, CreateView):
#     model = Answer
#     template_name = "blog/add_answers.html"
#     fields = '__all__'


def AddAnswerView(request, pk):
    print(request)
    if request.method == "POST":
        answer = request.POST.get("answer")
        Answer.objects.create(
            post=Post.objects.get(pk=pk),
            answer_text=answer,
            posted_by=request.user,
        )
        return HttpResponseRedirect(reverse("post-detail", args=(pk,)))
    else:
        if request.user.is_authenticated:
            return render(request, "blog/add_answers.html", {"pk": pk})
        else:
            return HttpResponseRedirect(reverse("login"))


def about(request):
    return render(request, "blog/about.html", {"title": "About"})
