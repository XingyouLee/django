from datetime import date
from .models import Post
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .form import CommentForm
from django.http import HttpResponseRedirect
# # Class-based views
class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    context_object_name = "posts"
    queryset = Post.objects.all().order_by("-date")[:3]


class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    context_object_name = "all_posts"
    queryset = Post.objects.all().order_by("-date")

class PostDetailView(DetailView):
    template_name = "blog/post-detail.html"
    model = Post
    # context_object_name = "post"
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            return post_id in stored_posts
        return False
        
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = self.object
        context["tags"] = self.object.tag.all()
        context["comment_form"] = CommentForm()
        context["saved_for_later"] = self.is_stored_post(self.request, self.object.id)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.save()
            return redirect("post-detail-page", slug=self.object.slug)
        
        context = self.get_context_data(object=self.object)
        context["comment_form"] = form
        context["saved_for_later"] = self.is_stored_post(self.request, self.object.id)
        return self.render_to_response(context)

class ReadLaterView(ListView):
    def get(self, request, *args, **kwargs):
        stored_posts = request.session.get("stored_posts")
        context = {}
        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True
        return render(request, "blog/stored-posts.html", context)
    def post(self, request, *args, **kwargs):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is None:
            stored_posts = []
        post_id = int(request.POST["post_id"])
        if post_id not in stored_posts:
            stored_posts.append(post_id)
            request.session["stored_posts"] = stored_posts
        else:
            stored_posts.remove(post_id)
            request.session["stored_posts"] = stored_posts
        # return HttpResponseRedirect("/")
        return redirect('posts-page')
# # # Function-based views

# def starting_page(request):
#     latest_posts = Post.objects.all().order_by("-date")[:3]
#     return render(request, "blog/index.html", {
#       "posts": latest_posts
#     })


# def posts(request):
#     all_posts = Post.objects.all().order_by("-date")
#     return render(request, "blog/all-posts.html", {
#       "all_posts": all_posts
#     })


# def post_detail(request, slug):
#     identified_post = Post.objects.get(slug=slug)
#     return render(request, "blog/post-detail.html", {
#       "post": identified_post,
#       "tags": identified_post.tag.all()
#     })
