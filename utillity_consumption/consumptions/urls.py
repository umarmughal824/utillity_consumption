from django.urls import path

from utillity_consumption.consumptions.views import (
    index,
    building_detail_view,
    meter_detail_view,
    line_chart_json,
)

app_name = "consumptions"
urlpatterns = [
    path("", index, name="index"),
    path("<int:id>/", view=building_detail_view, name="detail"),
    path("meter/<int:id>/", view=meter_detail_view, name="meter-detail"),
    path("chartJSON/<int:meter_id>", line_chart_json, name="line_chart_json"),
]
