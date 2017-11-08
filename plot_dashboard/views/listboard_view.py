from django.apps import apps as django_apps
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import AppConfigViewMixin
from edc_dashboard.view_mixins import ListboardFilterViewMixin
from edc_dashboard.views import ListboardView as BaseListboardView
from plot.constants import RESIDENTIAL_HABITABLE

from ..model_wrappers import PlotWithLogEntryModelWrapper
from ..view_mixins import PlotQuerysetViewMixin
from .listboard_filters import PlotListboardViewFilters


class ListBoardView(AppConfigViewMixin, EdcBaseViewMixin, ListboardFilterViewMixin,
                    PlotQuerysetViewMixin, BaseListboardView):

    app_config_name = 'plot_dashboard'

    navbar_name = settings.MAIN_NAVBAR_NAME
    navbar_selected_item = 'plot'

    ordering = '-modified'
    model = 'plot.plot'
    model_wrapper_cls = PlotWithLogEntryModelWrapper
    listboard_view_filters = PlotListboardViewFilters()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            RESIDENTIAL_HABITABLE=RESIDENTIAL_HABITABLE,
            map_url_name=django_apps.get_app_config('plot_dashboard').map_url_name)
        return context
