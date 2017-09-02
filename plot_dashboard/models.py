from django.conf import settings

if settings.APP_NAME == 'plot_dashboard':
    from .tests import models
