from datetime import datetime, timedelta
from django.shortcuts import redirect, get_object_or_404
from django.views import generic as generic_views

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

    def get_queryset(self):
        return self.model.objects.all().order_by('-vote_count')

class ServerDetailView(generic_views.DetailView):
    template_name = 'server.html'
    model = frontend_models.Server
    context_object_name = 'server'

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
                create_date__gt=datetime.now() - timedelta(minutes=5)
            )
        except frontend_models.Vote.DoesNotExist:
            server.add_vote()
            frontend_models.Vote.objects.create(
                character=form.cleaned_data['character'],
                server=server,
                ip_address=self.request.META.get('REMOTE_ADDR')
            )

        return redirect('servers')

class CategoryDetailView(generic_views.DetailView):
    template_name = 'category.html'
    model = frontend_models.Category
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)

        context.update({
            'server_list': frontend_models.Server.objects.filter(category=self.get_object().pk).order_by('-vote_count'),
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

class NewsDetailView(generic_views.DetailView):
    template_name = 'news_detail.html'
    model = frontend_models.News
    context_object_name = 'news'
