import Image, ImageDraw, ImageFont

from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views import generic as generic_views
from django.views.decorators.cache import cache_page

from frontend import forms as frontend_forms
from frontend import models as frontend_models

class HomeView(generic_views.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        context.update({
            'new_servers': frontend_models.Server.objects.all().order_by('-create_date')[:5],
            'top_servers': frontend_models.Server.objects.all().order_by('-vote_count')[:5],
            'latest_news': frontend_models.News.objects.all().order_by('-create_date')[:5],
        })

        return context

class ServerListView(generic_views.ListView):
    template_name = 'servers.html'
    model = frontend_models.Server
    context_object_name = 'server_list'
    paginate_by = settings.SERVERS_PER_PAGE

    def get_queryset(self):
        return self.model.objects.all().order_by('-vote_count')

class ServerDetailView(generic_views.DetailView):
    template_name = 'server.html'
    model = frontend_models.Server
    context_object_name = 'server'

    def get_context_data(self, **kwargs):
        context = super(ServerDetailView, self).get_context_data(**kwargs)

        context.update({
            'reviews': frontend_models.Review.objects.filter(server=self.object),
        })

        return context

class ReviewCreateView(generic_views.CreateView):
    template_name = 'review_create.html'
    form_class = frontend_forms.ReviewForm

    def form_valid(self, form):
        server = get_object_or_404(frontend_models.Server, pk=self.kwargs.get('pk'))
        obj = form.save(commit=False)
        obj.server = server
        obj.user = self.request.user
        obj.save()
        return redirect('server', pk=server.id)

class ServerVoteView(generic_views.FormView):
    template_name = 'vote.html'
    form_class = frontend_forms.VoteForm

    def get_context_data(self, **kwargs):
        context = super(ServerVoteView, self).get_context_data(**kwargs)

        context.update({
            'server': get_object_or_404(frontend_models.Server, pk=self.kwargs.get('pk')),
        })

        return context

    def form_valid(self, form):
        server = get_object_or_404(frontend_models.Server, pk=self.kwargs.get('pk'))

        try:
            frontend_models.Vote.objects.get(
                ip_address=self.request.META.get('REMOTE_ADDR'),
                create_date__gt=timezone.now() - timedelta(minutes=settings.VOTE_INTERVAL)
            )
        except frontend_models.Vote.DoesNotExist:
            server.add_vote()
            frontend_models.Vote.objects.create(
                character=form.cleaned_data['character'],
                server=server,
                ip_address=self.request.META.get('REMOTE_ADDR')
            )

        return redirect('servers')

class CategoryDetailView(generic_views.ListView):
    template_name = 'category.html'
    model = frontend_models.Server
    context_object_name = 'server_list'
    paginate_by = settings.SERVERS_PER_PAGE

    def get_queryset(self):
        return self.model.objects.filter(category=self.kwargs.get('pk')).order_by('-vote_count')

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)

        context.update({
            'category': get_object_or_404(frontend_models.Category, pk=self.kwargs.get('pk')),
        })

        return context

class SearchView(generic_views.FormView):
    template_name = 'search.html'
    form_class = frontend_forms.SearchForm

# News

class NewsListView(generic_views.ListView):
    template_name = 'news.html'
    model = frontend_models.News
    context_object_name = 'news_list'

    def get_queryset(self):
        return self.model.objects.all().order_by('-create_date')

class NewsDetailView(generic_views.DetailView):
    template_name = 'news_detail.html'
    model = frontend_models.News
    context_object_name = 'news'

# Dynamic Banner
@cache_page(settings.BANNER_LIFETIME)
def dynamic_banner(request, pk):

    server = get_object_or_404(frontend_models.Server, pk=pk)

    response = HttpResponse(mimetype="image/png")
    size = (468, 60)
    img = Image.new('RGBA', size, '#000000')
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), server.name)
    draw.text((300, 10), str(timezone.now()))
    img.save(response, 'png')

    return response