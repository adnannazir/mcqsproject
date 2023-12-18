import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Category


class DateTimePickerWidget(forms.widgets.DateTimeInput):
    def __init__(self, attrs=None, format='%d-%m-%Y'):
        attrs = attrs or {}
        attrs['class'] = attrs.get('class', '') + 'datetimepicker-input'  # common-datetimepicker  form-control
        attrs['data-target'] = attrs.get('data-target', '')
        # Specify the input format within the widget
        self.input_formats = ['%d-%m-%Y']

        super().__init__(attrs=attrs, format=format)


class DatePickerWidget(forms.widgets.DateInput):
    def __init__(self, attrs=None, format='%d-%m-%Y'):
        attrs = attrs or {}
        attrs['class'] = attrs.get('class',
                                   '') + 'datetimepicker-input form-control activity'  # common-datetimepicker  form-control
        attrs['data-target'] = attrs.get('data-target', '')
        # Add a placeholder attribute to provide a hint to the user
        attrs['placeholder'] = 'DD-MM-YYYY'
        # Specify the input format within the widget
        self.input_formats = ['%d-%m-%Y']
        super().__init__(attrs=attrs, format=format)


class DateFormatConversionField(forms.DateField):
    def to_python(self, value):
        if not value:
            return None

        try:
            # Parse the date in the custom format 'DD-MM-YYYY'
            date_value = datetime.datetime.strptime(value, '%d-%m-%Y').date()
        except ValueError:
            raise forms.ValidationError(f'Enter a valid date in the format DD-MM-YYYY.')

        return date_value



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['id', 'order', 'name', 'parent_category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['parent_category'].widget.attrs['required'] = False

    def clean_parent_wbs(self):
        parent_category = self.cleaned_data.get('parent_category')
        # instance_id = self.instance.id if self.instance else None  # Get instance ID or None if it's a new object

        if parent_category and self.instance:
            # Check if the current Category is a descendant of the selected parent_category
            if not self.instance.is_valid_descendant(parent_category):
                raise ValidationError("A Category cannot be its own parent or a child of its children (! >4 Levels Deep)")

        return parent_category
