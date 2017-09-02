from django.db import models
from edc_base.model_mixins import BaseUuidModel
from django.db.models.deletion import PROTECT
from edc_base.utils import get_utcnow


class Plot(BaseUuidModel):

    plot_identifier = models.CharField(max_length=25)


class PlotLog(BaseUuidModel):

    plot = models.ForeignKey(Plot, on_delete=PROTECT)


class PlotLogEntry(BaseUuidModel):

    report_datetime = models.DateTimeField(default=get_utcnow)

    plot_log = models.ForeignKey(PlotLog, on_delete=PROTECT)
