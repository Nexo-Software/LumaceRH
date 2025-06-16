# forms.py
from allauth.account.forms import SignupForm, LoginForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'signup_form'
        self.helper.form_method = 'post'
        self.helper.add_input(
            Submit(
                'submit', 
                'Crear cuenta',
                css_class='btn btn-primary mt-3',
                icon='user-plus'
            )
        )
class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'login_form'
        self.helper.form_method = 'post'
        self.helper.add_input(
            Submit(
                'submit',
                'Iniciar sesión',
                css_class='btn btn-primary mt-3',
                icon='sign-in-alt'
            )
        )