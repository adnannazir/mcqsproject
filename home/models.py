from django.db import models
from django.conf import settings


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)
    parent_wbs = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(blank=True, default=0)

    def is_valid_descendant(self, parent_category, max_depth=4):
        """
        Check if this category is a valid descendant (child or grandchild) of the provided category,
        and also ensure that the depth of the relationship is not greater than max_depth.
        """
        current_category = self
        depth = 1

        while parent_category:
            print(f"I am at depth: {depth}")
            if current_category == parent_category:
                return False
            parent_category = parent_category.parent_category
            depth += 1

        return depth <= max_depth

    def __str__(self):
        return self.name


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    categories = models.ManyToManyField(Category)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_created',
        verbose_name='Created by'
    )
    def __str__(self):
        return self.question_text


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text
