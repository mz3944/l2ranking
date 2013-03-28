from django.core.urlresolvers import reverse
from django.views import generic as generic_views

from usercp import forms as usercp_forms


class Register(generic_views.CreateView):
    """
    User registration view.
    """

    template_name = 'usercp/register.html'
    form_class = usercp_forms.RegisterForm

    def get_success_url(self):
        return reverse('usercp:login')