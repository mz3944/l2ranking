# Create your views here.
from django.views import generic as generic_views
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied

from frontend import models as frontend_models
from servercp import forms as servercp_forms


class ServerListView(generic_views.ListView):
    template_name = 'servercp/servers.html'
    model = frontend_models.Server
    context_object_name = 'server_list'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by('name')


class ServerStatisticsView(generic_views.DetailView):
    template_name = 'servercp/server_stats.html'
    model = frontend_models.Server
    context_object_name = 'server'

    def get_object(self, queryset=None):
        obj = super(ServerDeleteView, self).get_object(queryset)
        if self.request.user.id is not obj.user.id:
            raise PermissionDenied()
        return obj


class ServerAddView(generic_views.CreateView):
    template_name = 'servercp/server_add.html'
    model = frontend_models.Server
    context_object_name = 'server'
    form_class = servercp_forms.ServerCreateUpdateForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect(reverse('servercp:servers'))


class ServerDeleteView(generic_views.DeleteView):
    template_name = 'servercp/server_delete.html'
    model = frontend_models.Server
    context_object_name = 'server'

    def get_success_url(self):
        return reverse('servercp:servers')

    def get_object(self, queryset=None):
        obj = super(ServerDeleteView, self).get_object(queryset)
        if self.request.user.id is not obj.user.id:
            raise PermissionDenied()
        return obj


class ServerUpdateView(generic_views.UpdateView):
    template_name = 'servercp/server_update.html'
    model = frontend_models.Server
    context_object_name = 'server'
    form_class = servercp_forms.ServerCreateUpdateForm

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('servercp:server_update', kwargs={'pk': self.object.pk}))

    def get_object(self, queryset=None):
        obj = super(ServerUpdateView, self).get_object(queryset)
        if self.request.user.id is not obj.user.id:
            raise PermissionDenied()
        return obj
