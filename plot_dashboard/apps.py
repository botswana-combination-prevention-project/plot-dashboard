# coding=utf-8

from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings


class AppConfig(DjangoAppConfig):
    name = 'plot_dashboard'
    listboard_template_name = 'plot_dashboard/listboard.html'
    listboard_url_name = 'plot_dashboard:listboard_url'
    base_template_name = 'edc_base/base.html'
    # url_namespace = 'plot_dashboard'  # FIXME: is this still neeed??
    map_url_name = 'plot_dashboard:map_url'
    admin_site_name = 'plot_admin'


if settings.APP_NAME == 'plot_dashboard':

    from edc_map.apps import AppConfig as BaseEdcMapAppConfig

    class EdcMapAppConfig(BaseEdcMapAppConfig):
        verbose_name = 'Test Mappers'
        mapper_model = 'plot.plot'
        landmark_model = []
        verify_point_on_save = False
        zoom_levels = ['14', '15', '16', '17', '18']
        identifier_field_attr = 'plot_identifier'
        # Extra filter boolean attribute name.
        extra_filter_field_attr = 'enrolled'
