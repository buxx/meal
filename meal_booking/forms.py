from django import forms
from django.forms.utils import ErrorList


class ModelForm(forms.ModelForm):
    # Related fields to manage in forms.ModelMultipleChoiceField
    related = []

    def __init__(
            self,
            data=None,
            files=None,
            auto_id='id_%s',
            prefix=None,
            initial=None,
            error_class=ErrorList,
            label_suffix=None,
            empty_permitted=False,
            instance=None,
            use_required_attribute=None,
    ):

        if instance:
            if initial is None:
                initial = {}

            for related_name in self.related:
                related_query = getattr(instance, related_name)
                initial[related_name] = related_query.all()

        super().__init__(
            data=data,
            files=files,
            auto_id=auto_id,
            prefix=prefix,
            initial=initial,
            error_class=error_class,
            label_suffix=label_suffix,
            empty_permitted=empty_permitted,
            instance=instance,
            use_required_attribute=use_required_attribute,
        )

    def save(self, commit=True):
        for related_name in self.related:
            setattr(self.instance, related_name, self.cleaned_data[related_name])

        return super().save(commit=commit)


class RequiredFieldsMixin(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fields_required = getattr(self.Meta, 'fields_required', None)
        if fields_required:
            for key in self.fields:
                self.fields[key].required = key in fields_required
