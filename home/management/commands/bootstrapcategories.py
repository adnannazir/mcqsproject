from django.core.management.base import BaseCommand
from home.models import Category


class Command(BaseCommand):
    help = 'Bootstrap categories'

    def handle(self, *args, **kwargs):
        categories = [
            # Main Categories
            ("Main Category", None),
            ("English Mcqs", "Main Category"),
            ("Maths Mcqs", "Main Category"),
            ("General Knowledge MCQs", "Main Category"),
            ("Pakistan Current Affairs MCQs", "Main Category"),
            ("World Current Affairs MCQs", "Main Category"),
            ("Pak Study Mcqs", "Main Category"),
            ("Islamic Studies Mcqs", "Main Category"),
            ("Computer Mcqs", "Main Category"),
            ("Everyday Science Mcqs", "Main Category"),
            ("Physics Mcqs", "Main Category"),
            ("Chemistry Mcqs", "Main Category"),
            ("Biology Mcqs", "Main Category"),
            ("Pedagogy Mcqs", "Main Category"),
            ("URDU Mcqs", "Main Category"),

            # Sub Categories
            ("Management Sciences", "Main Category"),
            ("Finance Mcqs", "Management Sciences"),
            ("HRM Mcqs", "Management Sciences"),
            ("Marketing Mcqs", "Management Sciences"),
            ("Accounting Mcqs", "Management Sciences"),
            ("Auditing Mcqs", "Management Sciences"),

            ("ENGINEERING MCQS", "Main Category"),
            ("Electrical Engineering Mcqs", "ENGINEERING MCQS"),
            ("Civil Engineering Mcqs", "ENGINEERING MCQS"),
            ("Mechanical Engineering Mcqs", "ENGINEERING MCQS"),
            ("Chemical Engineering Mcqs", "ENGINEERING MCQS"),
            ("Software Engineering Mcqs", "ENGINEERING MCQS"),

            ("MEDICAL SUBJECTS", "Main Category"),
            ("Medical Mcqs", "MEDICAL SUBJECTS"),
            ("Biochemistry", "MEDICAL SUBJECTS"),
            ("Dental Materials", "MEDICAL SUBJECTS"),
            ("General Anatomy Mcqs", "MEDICAL SUBJECTS"),
            ("Microbiology", "MEDICAL SUBJECTS"),
            ("Oral Anatomy", "MEDICAL SUBJECTS"),
            ("Oral Histology", "MEDICAL SUBJECTS"),
            ("Oral Pathology and Medicine", "MEDICAL SUBJECTS"),
            ("Physiology Mcqs", "MEDICAL SUBJECTS"),
            ("Pathology", "MEDICAL SUBJECTS"),
            ("Pharmacology", "MEDICAL SUBJECTS"),

            ("OTHER SUBJECTS", "Main Category"),
            ("Psychology Mcqs", "OTHER SUBJECTS"),
            ("Agriculture Mcqs", "OTHER SUBJECTS"),
            ("Economics Mcqs", "OTHER SUBJECTS"),
            ("Sociology Mcqs", "OTHER SUBJECTS"),
            ("Political Science Mcqs", "OTHER SUBJECTS"),
            ("Statistics Mcqs", "OTHER SUBJECTS"),
            ("English Literature Mcqs", "OTHER SUBJECTS"),
            ("Judiciary And Law Mcqs", "OTHER SUBJECTS"),
        ]

        parent_categories = {}

        for name, parent_name in categories:
            parent_category = None
            if parent_name:
                parent_category = parent_categories.get(parent_name)

            category = Category.objects.create(name=name, parent_wbs=parent_category)
            parent_categories[name] = category

        self.stdout.write(self.style.SUCCESS('Categories bootstrapped successfully.'))
