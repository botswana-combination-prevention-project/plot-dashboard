from django.conf import settings
from django.test import TestCase, tag
from edc_model_wrapper.tests import ModelWrapperTestHelper

from ..model_wrappers import PlotModelWrapper, PlotLogEntryModelWrapper
from ..model_wrappers import PlotWithLogEntryModelWrapper
from .models import Plot, PlotLog


app_label = settings.APP_NAME


class MyModelWrapperTestHelper(ModelWrapperTestHelper):
    dashboard_url = '/listboard/111111-11'


class TestModelWrappers(TestCase):

    model_wrapper_helper_cls = MyModelWrapperTestHelper

    def setUp(self):
        self.plot_identifier = '111111-11'
        self.survey_schedule = 'bcpp-survey.bcpp-year-3.community'
        self.survey = 'bcpp-survey.bcpp-year-3.ess.community'
        self.plot = Plot.objects.create(plot_identifier=self.plot_identifier)
        self.plot_log = PlotLog.objects.create(
            plot=self.plot)

    @tag('1')
    def test_plot(self):
        helper = self.model_wrapper_helper_cls(
            model_wrapper=PlotModelWrapper,
            app_label='plot_dashboard',
            plot_identifier=self.plot_identifier)
        helper.test(self)

    @tag('1')
    def test_plot_log_entry(self):
        helper = self.model_wrapper_helper_cls(
            model_wrapper=PlotLogEntryModelWrapper,
            app_label='plot_dashboard',
            plot_log=self.plot_log)
        helper.test(self)

    @tag('1')
    def test_plot_with_log_entry(self):
        helper = self.model_wrapper_helper_cls(
            model_wrapper=PlotWithLogEntryModelWrapper,
            app_label='plot_dashboard',
            plot_identifier=self.plot_identifier)
        helper.test(self)
