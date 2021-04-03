from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from utillity_consumption.consumptions.models import Building


def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    context = {
        'buildings': Building.objects.all()
    }
    return render(request, 'consumptions/index.html', context)


from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView


class BuildingDetailView(LoginRequiredMixin, DetailView):

    model = Building
    slug_field = "id"
    slug_url_kwarg = "id"


building_detail_view = BuildingDetailView.as_view()
