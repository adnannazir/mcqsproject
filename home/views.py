from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from dataclasses import dataclass

from django.views.decorators.http import require_GET
from django_htmx.middleware import HtmxDetails
from faker import Faker

from home.models import Question


# Create your views here.

class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


def index(request):
    context = {
        'parent': '',
        'segment': 'dashboard'
    }
    return render(request, 'index.html', context)


@dataclass
class Person:
    id: int
    name: str


faker = Faker()
people = [Person(id=i, name=faker.name()) for i in range(1, 235)]


@require_GET
def partial_rendering(request: HtmxHttpRequest) -> HttpResponse:
    # Retrieve questions from your database (example: getting all questions)
    questions = Question.objects.all()
    # Standard Django pagination
    page_num = request.GET.get("page", "1")
    page = Paginator(object_list=questions, per_page=10).get_page(page_num)

    # The htmx magic - use a different, minimal base template for htmx
    # requests, allowing us to skip rendering the unchanging parts of the
    # template.
    if request.htmx:
        base_template = "_partial.html"
    else:
        base_template = "layouts/base.html"

    return render(
        request,
        "partial-rendering.html",
        {
            "base_template": base_template,
            "page": page,
        },
    )
