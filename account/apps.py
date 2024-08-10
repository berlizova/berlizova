from django.apps import AppConfig


class AccountConfig(AppConfig):
    """
    Configuration class for the 'account' app.
    This class sets the default auto field type and the name of the app.
    """

    # Specifies the type of auto-created primary key fields.
    default_auto_field = "django.db.models.BigAutoField"

    # Defines the name of the application.
    name = "account"
