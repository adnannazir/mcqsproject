from datetime import datetime
from random import sample
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from home.models import Category, Question, Option
from faker import Faker

class Command(BaseCommand):
    help = 'Add 1000 Random Questions to Categories'

    def handle(self, *args, **kwargs):
        fake = Faker()
        date_value = datetime(year=2023, month=12, day=18)
        User = get_user_model()
        default_user, created = User.objects.get_or_create(email='adnannazir.cs@gmail.com')

        categories = list(Category.objects.all())

        for _ in range(1000):
            question_text = fake.sentence(nb_words=10, variable_nb_words=True)
            assigned_categories = sample(categories, k=min(3, len(categories)))

            # Create a question and assign 2-3 random categories
            question = Question.objects.create(
                question_text=question_text,
                created_by=default_user,
                created_on=date_value
            )
            question.categories.add(*assigned_categories)

            # Generate 4 options and mark one as correct
            option_texts = [fake.words(nb=fake.random_int(min=3, max=5)) for _ in range(4)]
            correct_option_text = fake.random_element(option_texts)
            for option_text in option_texts:
                is_correct = (option_text == correct_option_text)
                Option.objects.create(
                    question=question,
                    option_text=' '.join(option_text),
                    is_correct=is_correct
                )

        self.stdout.write(self.style.SUCCESS('1000 questions added successfully.'))
