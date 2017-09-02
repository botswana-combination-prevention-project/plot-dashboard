from django.apps import apps as django_apps
from django.db.models.constants import LOOKUP_SEP

from edc_constants.constants import ANONYMOUS
from edc_device.constants import CLIENT, SERVER, NODE_SERVER
from edc_map.models import InnerContainer
from edc_map.site_mappers import site_mappers


class PlotQuerysetViewMixin:

    plot_queryset_lookups = []

    @property
    def plot_lookup_prefix(self):
        plot_lookup_prefix = LOOKUP_SEP.join(self.plot_queryset_lookups)
        return f'{plot_lookup_prefix}__' if plot_lookup_prefix else ''

    @property
    def plot_identifiers(self):
        """Returns a list of plot identifiers allocated to this device.
        """
        edc_device_app_config = django_apps.get_app_config('edc_device')
        device_id = edc_device_app_config.device_id
        plot_identifiers = []
        try:
            plot_identifiers = InnerContainer.objects.get(
                device_id=device_id,
                map_area=site_mappers.current_map_area).identifier_labels
        except InnerContainer.DoesNotExist:
            pass
        return plot_identifiers

    def add_device_filter_options(self, options=None, plot_identifier=None, **kwargs):
        """Updates the filter options to limit the plots returned
        to those allocated to this client device_id.
        """
        if plot_identifier:
            options.update(
                {f'{self.plot_lookup_prefix}plot_identifier': plot_identifier})
        elif self.plot_identifiers:
            options.update(
                {f'{self.plot_lookup_prefix}plot_identifier__in': self.plot_identifiers})
        return options

    def add_map_area_filter_options(self, options=None, **kwargs):
        """Updates the filter options to limit the plots returned
        to those in the current map_area.
        """
        map_area = site_mappers.current_map_area
        options.update(
            {f'{self.plot_lookup_prefix}map_area': map_area})
        return options

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        edc_device_app_config = django_apps.get_app_config('edc_device')
        if edc_device_app_config.device_role in [SERVER, CLIENT, NODE_SERVER]:
            options = self.add_map_area_filter_options(
                options=options, **kwargs)
        if edc_device_app_config.device_role == CLIENT:
            options = self.add_device_filter_options(options=options, **kwargs)
        return options

    def get_queryset_exclude_options(self, request, *args, **kwargs):
        options = super().get_queryset_exclude_options(
            request, *args, **kwargs)
        app_config = django_apps.get_app_config('plot')
        if self.navbar_name != ANONYMOUS:
            options.update(
                {f'{self.plot_lookup_prefix}plot_identifier__in':
                 [app_config.anonymous_plot_identifier]})
        return options
