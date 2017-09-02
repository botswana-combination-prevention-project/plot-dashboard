# coding=utf-8

from django.conf.urls import url
from edc_constants.constants import UUID_PATTERN

from .views import ListBoardView, LocationView
from .patterns import plot_identifier
from django.conf import settings

app_name = 'plot_dashboard'

urlpatterns = [
    url(r'^listboard/'
        '(?P<plot_identifier>' + plot_identifier + ')/'
        '(?P<page>\d+)/',
        ListBoardView.as_view(), name='listboard_url'),
    url(r'^listboard/'
        '(?P<plot_identifier>' + plot_identifier + ')/',
        ListBoardView.as_view(), name='listboard_url'),
    url(r'^listboard/'
        '(?P<id>' + UUID_PATTERN.pattern + ')/'
        '(?P<page>\d+)/',
        ListBoardView.as_view(), name='listboard_url'),
    url(r'^listboard/'
        '(?P<id>' + UUID_PATTERN.pattern + ')/',
        ListBoardView.as_view(), name='listboard_url'),
    url(r'^listboard/(?P<page>\d+)/',
        ListBoardView.as_view(), name='listboard_url'),
    url(r'^listboard/',
        ListBoardView.as_view(), name='listboard_url'),
    url(r'^map/(?P<map_area>\w+)/(?P<plot_identifier>' + plot_identifier + ')/',
        LocationView.as_view(), name='map_url'),
]


if settings.APP_NAME == 'plot_dashboard':
    from .tests.admin import plot_admin
    urlpatterns = ([url(r'^admin/', plot_admin.urls)]
                   + urlpatterns)
