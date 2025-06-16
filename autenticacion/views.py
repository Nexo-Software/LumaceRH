from allauth.account.views import SignupView, LoginView
from .forms import CustomSignupForm, CustomLoginForm
# Create your views here.

class MyCustomSignupView(SignupView):
    template_name = 'registrar.html'
    form_class = CustomSignupForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

class MyCustomLoginView(LoginView):
    template_name = 'iniciar.html'
    form_class = CustomLoginForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context