from django.views import generic as generic_views
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied

from frontend import models as frontend_models
from servercp import forms as servercp_forms


class ServerListView(generic_views.ListView):
    """
    View displays all servers owned by logged in user.
    """

    template_name = 'servercp/servers.html'
    model = frontend_models.Server
    context_object_name = 'server_list'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by('name')


class ServerInfoView(generic_views.DetailView):
    """
    View displays all information about server including statistics (vote_count, stats_in, stats_out etc...).
    """

    template_name = 'servercp/info.html'
    model = frontend_models.Server
    context_object_name = 'server'

    def get_object(self, queryset=None):
        obj = super(ServerInfoView, self).get_object(queryset)
        if not obj.is_owner(self.request.user):
            raise PermissionDenied()
        return obj


class ServerAddView(generic_views.CreateView):
    """
    View allows user to add server.
    """

    template_name = 'servercp/add.html'
    form_class = servercp_forms.ServerForm
    context_object_name = 'server'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect(reverse('servercp:servers'))


class ServerUpdateView(generic_views.UpdateView):
    """
    View allows user to update server.
    """

    template_name = 'servercp/update.html'
    model = frontend_models.Server
    form_class = servercp_forms.ServerForm
    context_object_name = 'server'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('servercp:update', kwargs={'pk': self.object.pk}))

    def get_object(self, queryset=None):
        obj = super(ServerUpdateView, self).get_object(queryset)
        if not obj.is_owner(self.request.user):
            raise PermissionDenied()
        return obj


class ServerDeleteView(generic_views.DeleteView):
    """
    View allows user to delete server.
    """

    template_name = 'servercp/delete.html'
    model = frontend_models.Server
    context_object_name = 'server'

    def get_success_url(self):
        return reverse('servercp:servers')

    def get_object(self, queryset=None):
        obj = super(ServerDeleteView, self).get_object(queryset)
        if not obj.is_owner(self.request.user):
            raise PermissionDenied()
        return obj