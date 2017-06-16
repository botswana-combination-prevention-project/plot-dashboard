# coding=utf-8

from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'plot_dashboard'
    listboard_template_name = 'plot_dashboard/listboard.html'
    listboard_url_name = 'plot_dashboard:listboard_url'
    base_template_name = 'edc_base/base.html'
    url_namespace = 'plot_dashboard'  # FIXME: is this still neeed??
    map_url_name = 'plot_dashboard:map_url'
