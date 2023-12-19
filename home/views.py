from string import ascii_uppercase

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from dataclasses import dataclass

from django.views.decorators.http import require_GET
from django_htmx.middleware import HtmxDetails
from faker import Faker

from home.models import Question, Category


# from django.db.models import BooleanField, Case, When


# Create your views here.

class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


def index(request):
    # categories = Category.objects.all()

    # Retrieve and organize your categories
    # categories = Category.objects.annotate(
    #     has_children=Case(
    #         When(children__isnull=False, then=True),
    #         default=False,
    #         output_field=BooleanField()
    #     )
    # ).order_by('has_children', 'order', 'name')  # Order by has_children first, then other fields

    categories = Category.objects.order_by('order')
    context = {
        'parent': '',
        'segment': 'dashboard',
        'categories': categories,
    }
    return render(request, 'index.html', context)


@require_GET
def main_page(request: HtmxHttpRequest, category_id=None) -> HttpResponse:
    # Retrieve questions from your database (example: getting all questions)
    questions = Question.objects.all()
    categories = Category.objects.order_by('order')
    if category_id:
        # Filter questions by the provided category ID
        category = get_object_or_404(Category, id=category_id)
        questions = questions.filter(Q(categories=category))

    # Standard Django pagination
    page_num = request.GET.get("page", "1")
    page = Paginator(object_list=questions, per_page=10).get_page(page_num)

    letters = {index: chr(65 + index - 1) for index in range(1, 27)}  # Generating letters A-Z
    # The htmx magic - use a different, minimal base template for htmx
    # requests, allowing us to skip rendering the unchanging parts of the
    # template.
    if request.htmx:
        base_template = "_partial.html"
    else:
        base_template = "layouts/base.html"

    return render(
        request,
        "mcqs.html",
        {
            "base_template": base_template,
            "page": page,
            "categories": categories,
            'segment': 'questions',
        },
    )
