# Django
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.db.models import Q, CharField # Q para consultas complejas
from django.shortcuts import get_object_or_404, redirect
from django.db import transaction
# Vistas
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from formtools.wizard.views import SessionWizardView
# Formularios
from .forms import PostulanteInfoForm, PostulanteDireccionForm, PostulantePuestoForm, PostulanteNotasForm, RegistroUsuarioForm, EmpleadoForm, EmpleadoPuestoForm, EmpleadoNotasForm
# Modelos
from .models import PostulanteModel, EmpleadoModel
from incidencia.models import IncidenciasEmpleados, TipoIncidenciasModel
from django.contrib.auth.models import User
from contrato.models import ContratoModel
# Mixins
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# Postgres
from django.contrib.postgres.lookups import Unaccent

# Registrar búsqueda insensible a acentos (en tu modelo o al inicio de la app)
CharField.register_lookup(Unaccent)


class PostulanteListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = PostulanteModel # Modelo a utilizar
    template_name = 'postulante_list.html' # Plantilla a utilizar
    context_object_name = 'postulantes'
    permission_required = 'empleado.view_postulante'
    # Modificar el query para que solo mueste a los que estan como pendientes
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(estado='Pendiente')

class NuevoUsuarioView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = User # Modelo a utilizar
    form_class = RegistroUsuarioForm # Formulario a utilizar
    template_name = 'nuevo_usuario.html' # Plantilla a utilizar
    success_url = reverse_lazy('postulante_create') # URL de redirección al crear el usuario
    permission_required = 'user.add_postulante'

    def form_valid(self, form):
        # Obtener el nombre sin espacios
        first_name = form.cleaned_data['first_name']
        no_spaces_name = first_name.replace(' ', '')
        # Obtener el apellido
        last_name = form.cleaned_data['last_name']
        no_spaces_last_name = last_name.replace(' ', '')

        fusion = no_spaces_name + no_spaces_last_name
        username = fusion

        i = 1  # Contador para evitar duplicados
        while User.objects.filter(username=username.lower()).exists():
            username = f"{fusion}{i}"
            i += 1

        # Asignar el username y correo electrónico definitivos
        form.instance.username = username.lower()
        form.instance.email = f'{username.lower()}@florcatorce.com'

        # Guardar el usuario
        user = form.save(commit=False)
        user.is_active = False  # El usuario se crea como inactivo
        user.save()

        # <-- CORRECIÓN 2: Ya no se necesita esta línea, es un error potencial
        # new_user = User.objects.get(username=fusion)

        # Redirigir al formulario de postulante con el ID del usuario recién creado
        # Usamos el 'pk' (clave primaria) del objeto 'user' que acabamos de guardar
        return redirect('postulante_create', usuario=user.pk)

class PostulanteWizardView(LoginRequiredMixin, PermissionRequiredMixin, SessionWizardView):
    permission_required = 'empleado.add_postulante'
    template_name = 'postulante_wizard_form.html'
    form_list = [
        ('direccion', PostulanteDireccionForm),
        ('puesto', PostulantePuestoForm),
        ('notas', PostulanteNotasForm),
    ]
    
    def done(self, form_list, **kwargs):
        form_data = {}
        for form in form_list:
            form_data.update(form.cleaned_data)
        pk_usuario = self.kwargs.get('usuario')
        # 404 user
        asociado = get_object_or_404(User, id=pk_usuario)

        # Añadir los campos created_by y updated_by al diccionario form_data
        form_data['usuario'] = asociado
        form_data['created_by'] = self.request.user
        form_data['updated_by'] = self.request.user
        PostulanteModel.objects.create(**form_data)
        return HttpResponseRedirect(reverse_lazy('postulante_list'))

class PostulanteDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = PostulanteModel # Modelo a utilizar
    template_name = 'postulante_detail.html' # Plantilla a utilizar
    context_object_name = 'postulante'
    permission_required = 'empleado.view_postulante'

# Vistas para empleado
class EmpleadoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = EmpleadoModel # Modelo a utilizar
    template_name = 'empleado_list.html' # Plantilla a utilizar
    context_object_name = 'empleados'
    permission_required = 'empleado.view_empleadomodel'


class EmpleadoWizardView(LoginRequiredMixin, PermissionRequiredMixin, SessionWizardView):
    permission_required = 'empleado.add_empleadomodel'
    template_name = 'empleado_wizard_form.html'
    form_list = [
        ('info', EmpleadoForm),
        ('puesto', EmpleadoPuestoForm),
        # He eliminado 'notas' para simplificar el ejemplo, pero puedes mantenerlo.
        ('notas', EmpleadoNotasForm),
    ]

    def get_form_initial(self, step):
        """
        Datos inciales para el formulario del paso actual.
        """
        # Primero, obtenemos el diccionario inicial del comportamiento por defecto del wizard.
        # Esto es crucial para evitar el bucle de recursión.
        initial = super().get_form_initial(step)

        # Solo si estamos en el paso 'puesto', intentamos obtener los datos del paso 'info'.
        if step == 'puesto':
            # Obtenemos los datos ya validados del paso anterior ('info')
            prev_data = self.get_cleaned_data_for_step('info')

            # Si existen datos y hay un 'postulante' en ellos...
            if prev_data and 'postulante' in prev_data:
                postulante = prev_data.get('postulante')
                if postulante:
                    # Actualizamos el diccionario 'initial' con los datos del postulante.
                    initial.update({
                        'puesto': postulante.puesto,
                        'contrato': postulante.contrato
                    })

        # Devolvemos el diccionario 'initial', ya sea el original o el modificado.
        return initial

    @transaction.atomic  # Usamos una transacción para garantizar la integridad de los datos
    def done(self, form_list, **kwargs):
        """
        Este método se ejecuta cuando todos los formularios son válidos.
        """
        form_data = {}
        for form in form_list:
            form_data.update(form.cleaned_data)

        # Obtenemos la instancia del postulante
        postulante = form_data.get('postulante')

        # Cambiamos el estado del postulante a 'Aceptado' y lo guardamos
        if postulante:
            postulante.estado = 'Aceptado'
            postulante.save()

        # Añadimos los campos de auditoría
        form_data['created_by'] = self.request.user
        form_data['updated_by'] = self.request.user

        # Creamos el nuevo empleado con todos los datos recopilados
        EmpleadoModel.objects.create(**form_data)

        # Redirigimos a la lista de empleados
        return HttpResponseRedirect(reverse_lazy('empleado_list'))

# Buscar empleado por Nombre
class EmpleadoSearchView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = EmpleadoModel
    template_name = 'buscar_empleado.html'
    context_object_name = 'empleados'
    permission_required = 'empleado.view_empleadomodel'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return EmpleadoModel.objects.filter(
                Q(postulante__usuario__first_name__unaccent__icontains=query) | Q(postulante__usuario__last_name__unaccent__icontains=query)
            )
        return EmpleadoModel.objects.none()
# Empleados por sucursal
class EmpleadoSucursalListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = EmpleadoModel
    template_name = 'sucursal_empleados.html'
    context_object_name = 'empleados'
    permission_required = 'empleado.view_empleadomodel'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener el usuario actual
        user = self.request.user
        # Obtener la sucursal del usuario
        empleado_login = get_object_or_404(EmpleadoModel, postulante__usuario=user)
        context['sucursal'] = empleado_login.sucursal
        return context

    def get_queryset(self):
        # Obtener el usuario actual
        user = self.request.user
        # Obtener la sucursal del usuario
        empleado_login = get_object_or_404(EmpleadoModel, postulante__usuario=user)
        sucursal = empleado_login.sucursal
        # Filtrar los empleados por la sucursal del usuario
        return EmpleadoModel.objects.filter(sucursal=sucursal)

# Detalle de empleado
class EmpleadoDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = EmpleadoModel # Modelo a utilizar
    template_name = 'empleado.html' # Plantilla a utilizar
    context_object_name = 'empleado'
    permission_required = 'empleado.view_empleadomodel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener el empleado actual
        empleado = self.get_object()
        # Obtener las incidencias del empleado
        context['incidencias'] = IncidenciasEmpleados.objects.filter(empleado=empleado, estado_incidencia='PENDIENTE').order_by('-fecha')
        # Obtener los tipos de incidencias
        context['tipos_incidencias'] = TipoIncidenciasModel.objects.all()
        # Obtener contratos
        context['contratos'] = ContratoModel.objects.filter(personalizado=False)
        return context
    def post(self, request, *args, **kwargs):
        # Recibir los datos del formulario
        # Procesar la solicitud POST
        tipo_incidencia_id = request.POST.get('tipo_incidencia')
        fecha = request.POST.get('fecha')
        observaciones = request.POST.get('observaciones')
        tipo_contrato = request.POST.get('tipo_contrato')
        dif_puesto = request.POST.get('dif_puesto', 'off') == 'on'  # Convertir a booleano
        print(f'El tipo de contrato es: {tipo_contrato} y se la dedicion es : {dif_puesto}')

        # Guardar la incidencia
        try:
            empleado = self.get_object()
            tipo_incidencia = get_object_or_404(TipoIncidenciasModel, id=tipo_incidencia_id)
            incidencia = IncidenciasEmpleados.objects.create(
                empleado=empleado,
                tipo_incidencia=tipo_incidencia,
                fecha=fecha,
                observaciones=observaciones,
                dif_puesto = dif_puesto,
                contrato_obj = get_object_or_404(ContratoModel, id=tipo_contrato) if tipo_contrato else None,
                created_by=self.request.user,
                updated_by=self.request.user
            )
            # Redirigir a la página de detalle del empleado
            return HttpResponseRedirect(reverse_lazy('empleado_detail', kwargs={'pk': empleado.pk}))
        except Exception as e:
            # Manejar el error, por ejemplo, mostrar un mensaje de error
            print(f"Error al crear la incidencia: {e}")
            # Aquí podrías redirigir a una página de error o mostrar un mensaje en la misma página
        return HttpResponseRedirect(reverse_lazy('empleado_detail', kwargs={'pk': self.get_object().pk}))

class EmpleadoUpdateWizardView(LoginRequiredMixin, PermissionRequiredMixin, SessionWizardView):
    permission_required = 'empleado.change_empleadomodel'
    template_name = 'empleado_wizard_form.html'
    form_list = [
        ('puesto', EmpleadoPuestoForm),
        ('notas', EmpleadoNotasForm),
    ]

    def get_form_instance(self, step):
        # Obtener el objeto desde la base de datos solo una vez
        if not hasattr(self, 'empleado'):
            self.empleado = EmpleadoModel.objects.get(pk=self.kwargs['pk'])
        return self.empleado

    def done(self, form_list, **kwargs):
        # Guardar el objeto editado
        empleado = self.get_form_instance(None)
        for form in form_list:
            for field, value in form.cleaned_data.items():
                setattr(empleado, field, value)
        empleado.save()
        return redirect('empleado_detail', pk=empleado.pk)