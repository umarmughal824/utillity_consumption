from django.urls import path

from utillity_consumption.consumptions.views import (
    Buildings,
    building_detail_view,
)

app_name = "consumptions"
urlpatterns = [
    path("", Buildings.as_view(), name="index"),
    # path("~index/", view=index, name="index"),
    # path("~update/", view=user_update_view, name="update"),
    path("<int:id>/", view=building_detail_view, name="detail"),
]
