from django.apps import apps as django_apps
from django.db.models import Q
from django.test import TestCase, tag
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.views.generic.base import ContextMixin

from edc_device.constants import CLIENT, CENTRAL_SERVER, NODE_SERVER
from edc_device.tests import DeviceTestHelper
from edc_map.models import Container, InnerContainer
from edc_map.tests import MapTestHelper
from edc_map.site_mappers import site_mappers
from plot.constants import ANONYMOUS
from plot.tests import PlotTestHelper, TestPlotMapper
from survey.tests import SurveyTestHelper

from ..view_mixins import PlotQuerysetViewMixin


class ListBoardView:
    def get_queryset_exclude_options(self, request, *args, **kwargs):
        """Returns exclude options applied to every
        queryset.
        """
        return {}

    def get_queryset_filter_options(self, request, *args, **kwargs):
        """Returns filter options applied to every
        queryset.
        """
        return {}

    def extra_search_options(self, search_term):
        """Returns a search Q object that will be added to the
        search criteria (OR) for the search queryset.
        """
        return Q()


class TestView(PlotQuerysetViewMixin, ListBoardView, ContextMixin):

    plot_queryset_lookups = ['plot']
    navbar_name = None


@tag('1')
class TestViewMixin(TestCase):

    plot_helper = PlotTestHelper()
    survey_helper = SurveyTestHelper()
    device_helper = DeviceTestHelper()
    map_helper = MapTestHelper()

    def setUp(self):
        self.device_helper.override_device(
            device_id='99', device_role=CENTRAL_SERVER)

        self.survey_helper.load_test_surveys()
        django_apps.app_configs['edc_device'].device_id = '99'
        site_mappers.registry = {}
        site_mappers.loaded = False
        site_mappers.register(TestPlotMapper)

        self.subject_identifier = '12345'
        self.view = TestView()
        request = RequestFactory()

        self.view.request = request
        self.view.request.META = {'HTTP_CLIENT_IP': '1.1.1.1'}
        self.view.request.GET = request
        self.view.object_list = None
        self.view.kwargs = {}

        map_area = 'test_community'
        self.plot = self.plot_helper.make_plot(map_area=map_area)

    def test_plot_queryset_context(self):
        self.assertTrue(self.view.get_context_data())

    @override_settings(DEVICE_ROLE=NODE_SERVER, DEVICE_ID='98')
    def test_plot_queryset_view_plot_identifiers(self):
        self.device_helper.override_device(
            device_id='98', device_role=NODE_SERVER)
        self.map_helper.allocate_objects_to_device(
            object_list=[self.plot], device_id='98')
        self.assertIn(self.plot.plot_identifier, self.view.plot_identifiers)

    def test_plot_queryset_view_filter_by_map_area(self):
        options = self.view.add_map_area_filter_options(options={})
        self.assertEqual('test_community', options.get('plot__map_area'))

    @override_settings(DEVICE_ROLE=CLIENT, DEVICE_ID='10')
    def test_plot_queryset_view_filter_by_map_area1(self):
        self.device_helper.override_device(device_id='10', device_role=CLIENT)
        options = {}
        options = self.view.get_queryset_filter_options(
            request=self.view.request, **options)
        self.assertEqual('test_community', options.get('plot__map_area'))

    @override_settings(DEVICE_ROLE=CLIENT, DEVICE_ID='10')
    def test_plot_queryset_view_filter_by_map_area2(self):
        self.device_helper.override_device(device_id='10', device_role=CLIENT)
        self.view.plot_queryset_lookups = ['household', 'plot']
        options = {}
        options = self.view.get_queryset_filter_options(
            request=self.view.request, **options)
        self.assertEqual('test_community', options.get(
            'household__plot__map_area'))

    @override_settings(DEVICE_ROLE=CLIENT, DEVICE_ID='10')
    def test_plot_queryset_view_filter_by_allocated_plots(self):
        self.device_helper.override_device(device_id='10', device_role=CLIENT)
        self.map_helper.allocate_objects_to_device(
            object_list=[self.plot], device_id='10')
        self.view.plot_queryset_lookups = ['household', 'plot']
        options = {}
        options = self.view.get_queryset_filter_options(
            request=self.view.request, **options)
        self.assertIn(self.plot.plot_identifier, options.get(
            'household__plot__plot_identifier__in'))

    @override_settings(DEVICE_ROLE=CLIENT, DEVICE_ID='10')
    def test_plot_queryset_view_filter_by_plot_identifier(self):
        self.device_helper.override_device(device_id='10', device_role=CLIENT)
        self.map_helper.allocate_objects_to_device(
            object_list=[self.plot], device_id='10')
        self.view.plot_queryset_lookups = ['household', 'plot']
        options = {}
        options = self.view.get_queryset_filter_options(
            request=self.view.request, plot_identifier=self.plot.plot_identifier, **options)
        self.assertEqual(self.plot.plot_identifier, options.get(
            'household__plot__plot_identifier'))

    @override_settings(DEVICE_ROLE=CLIENT, DEVICE_ID='10')
    def test_excludes_anonymous_plot(self):
        app_config = django_apps.get_app_config('plot')
        self.device_helper.override_device(device_id='10', device_role=CLIENT)
        self.map_helper.allocate_objects_to_device(
            object_list=[self.plot], device_id='10')
        options = {}
        exclude_options = self.view.get_queryset_exclude_options(
            request=self.view.request, **options)
        self.assertIn('plot__plot_identifier__in', exclude_options)
        self.assertIn(app_config.anonymous_plot_identifier, exclude_options.get(
            'plot__plot_identifier__in'))

    @override_settings(DEVICE_ROLE=CLIENT, DEVICE_ID='10')
    def test_does_not_exclude_anonymous_plot(self):
        self.device_helper.override_device(device_id='10', device_role=CLIENT)
        self.map_helper.allocate_objects_to_device(
            object_list=[self.plot], device_id='10')
        self.view.navbar_name = ANONYMOUS
        options = {}
        exclude_options = self.view.get_queryset_exclude_options(
            request=self.view.request, **options)
        self.assertNotIn(
            'plot__plot_identifier__in', exclude_options)
