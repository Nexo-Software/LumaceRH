from admin_interface.models import Theme

theme = Theme.objects.create(
    name="Dark Mode",
    active=True,
    css_header_background_color="#121212",
    css_header_text_color="#ffffff",
    css_module_background_color="#1e1e1e",
    css_module_text_color="#e0e0e0",
    css_module_link_color="#4fc3f7",
    css_save_button_background_color="#00695c",
    css_save_button_text_color="#ffffff",
    css_delete_button_background_color="#c62828",
    css_delete_button_text_color="#ffffff",
)
theme.save()