import csv
from datetime import datetime
import pytz
import time

from chartjs.views.lines import BaseLineChartView
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.timezone import make_aware
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, RedirectView, UpdateView

from utillity_consumption.consumptions.models import Building, Meter, Consumption
from utillity_consumption.consumptions.utils import check_for_validity_of_file

BUILDING_HEADER_FIELDS = [
    f"{f.name}_id" if f.is_relation else f.name for f in Building._meta.get_fields()
]
BUILDING_HEADER_FIELDS.remove("meter_id")
METER_HEADER_FIELDS = [
    f"{f.name}_id" if f.is_relation else f.name for f in Meter._meta.get_fields()
]
METER_HEADER_FIELDS.remove("consumption_id")
CONSUMPTION_HEADER_FIELDS = [
    f"{f.name}_id" if f.is_relation else f.name for f in Consumption._meta.get_fields()
]
CONSUMPTION_HEADER_FIELDS.remove("id")


class Buildings(LoginRequiredMixin, TemplateView):
    template_name = "consumptions/index.html"

    def get(self, request):
        context = {"buildings": Building.objects.all()}
        return render(request, self.template_name, context)

    def post(self, request):
        action = request.POST.get("type", "")
        file = request.FILES["myfile"]
        if not file._name.endswith(".csv"):
            raise Exception("Only csv file is supported")
        file = file.read().decode("UTF-8")
        file = file.splitlines()
        reader = csv.DictReader(file)
        header_row = reader.fieldnames

        if action == "buildings":
            check_for_validity_of_file(BUILDING_HEADER_FIELDS, header_row)
            for row in reader:
                row = {k: v for k, v in row.items() if v != ""}
                if row:
                    _, _ = Building.objects.get_or_create(
                        id=row["id"], name=row["name"]
                    )
        elif action == "meters":
            check_for_validity_of_file(METER_HEADER_FIELDS, header_row)
            for row in reader:
                row = {k: v for k, v in row.items() if v != ""}
                if row:
                    _, _ = Meter.objects.get_or_create(
                        id=row["id"],
                        building_id=row["building_id"],
                        fuel=row["fuel"],
                        unit=row["unit"],
                    )

        elif action == "consumptions":
            check_for_validity_of_file(CONSUMPTION_HEADER_FIELDS, header_row)
            counter = 0
            for row in reader:
                row = {k: v for k, v in row.items() if v != ""}
                entries = []
                if row:
                    reading_date_time = row["reading_date_time"].split(" ")[0]
                    reading_date_time = datetime.strptime(reading_date_time, "%Y-%m-%d")
                    reading_date_time = make_aware(reading_date_time, timezone=pytz.UTC)
                    # pdb.set_trace()
                    consumption = Consumption(
                        meter_id=row["meter_id"],
                        consumption=float(row["consumption"]),
                        reading_date_time=reading_date_time,
                    )
                    entries.append(consumption)

                if counter % 100 == 0:
                    Consumption.objects.bulk_create(entries)
                    entries = []
                counter += 1

        self.msg = "Data successfully imported"
        context = {
            "buildings": Building.objects.all(),
            "msg": self.msg,
        }

        return render(request, self.template_name, context)


index = Buildings.as_view()


class BuildingDetailView(LoginRequiredMixin, DetailView):

    model = Building
    slug_field = "id"
    slug_url_kwarg = "id"


building_detail_view = BuildingDetailView.as_view()


class MeterDetailView(LoginRequiredMixin, DetailView):

    model = Meter
    slug_field = "id"
    slug_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context = super(MeterDetailView, self).get_context_data(**kwargs)
        consumptions = Consumption.objects.filter(meter_id=self.object.id).values_list(
            "consumption"
        )
        data = [consumption[0] for consumption in consumptions]
        context["data"] = data
        return context


meter_detail_view = MeterDetailView.as_view()


class LineChartJSONView(LoginRequiredMixin, BaseLineChartView):
    meter_id = None

    def get_context_data(self, **kwargs):
        context = super(BaseLineChartView, self).get_context_data(**kwargs)
        context.update({"labels": self.get_labels(), "datasets": self.get_datasets()})
        print(self.kwargs)
        self.meter_id = self.kwargs["meter_id"]
        print(self.meter_id)
        consumptions = Consumption.objects.filter(meter_id=self.meter_id).values_list(
            "consumption"
        )
        data = [consumption[0] for consumption in consumptions]
        # context['datasets'][0]["data"] = data
        dataset = context["datasets"][0]
        dataset["data"] = data
        result = [dataset]
        context["datasets"] = result
        print(context)
        return context

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]

    def get_providers(self):
        """Return names of datasets."""
        return ["UK"]

    def get_data(self):
        """Return 3 datasets to plot."""
        return [[1, 2, 3]]


# line_chart = TemplateView.as_view(template_name='line_chart.html')
line_chart_json = LineChartJSONView.as_view()
