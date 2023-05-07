from django import forms


class UploadFile(forms.Form):
    file = forms.FileField()


class TasksForm(forms.Form):
    template_name = "forms/tasks_form.html"

    def __init__(self, form_data, *args, **kwargs):
        super().__init__(form_data, *args, **kwargs)
        for i, data in enumerate(form_data):
            self.sourceword_translation = data["source_word-translation"]
            self.fields[f"requisite_{i}"] = forms.ChoiceField(
                choices=((eng_ru[0],) for eng_ru in data["translation_variants"]),
                widget=forms.RadioSelect)
            self.fields[f"requisite_{i}"].initial = 0
