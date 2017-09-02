from django.contrib.admin import AdminSite as DjangoAdminSite

from .models import Plot, PlotLog, PlotLogEntry


class AdminSite(DjangoAdminSite):
    site_url = '/'


plot_admin = AdminSite(name='plot_admin')
plot_admin.register(Plot)
plot_admin.register(PlotLog)
plot_admin.register(PlotLogEntry)
