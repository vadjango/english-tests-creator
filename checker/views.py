from django.shortcuts import render
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.views.generic import View, TemplateView
from django.http import HttpResponseRedirect
from checker.forms import UploadFile, TasksForm
from docx import Document
import pandas as pd
import numpy as np
from django.views.decorators.csrf import csrf_exempt


def replace_str(txt: str) -> str:
    replacements = (("–", "-"), ("—", "-"))
    for char, replacement in replacements:
        if char in txt:
            txt = txt.replace(char, replacement)
    return txt


def get_all_translations(entire_dtf: pd.DataFrame, variants_dtf: pd.DataFrame) -> list[np.array]:
    all_translations = []
    for i in range(20):
        rand_variants = entire_dtf.sample(3, ignore_index=True)  # получаем 3 случайных варианта из всего датафрейма
        additional_variant: pd.DataFrame = variants_dtf.iloc[
            [i]]  # и доп. вариант, который правильный. Однако, он уже может быть в rand_variants
        print(list(rand_variants["translation"].array))
        print("Source truth matrix:\n", additional_variant["translation"].isin(rand_variants["translation"].array),
              end="\n\n")
        print("Non-truth matrix:\n", ~additional_variant["translation"].isin(rand_variants["translation"].array))
        print("Final matrix:\n", additional_variant["translation"][~additional_variant["translation"].
              isin(rand_variants["translation"].array)])
        if len(additional_variant["translation"][~additional_variant["translation"].
                isin(rand_variants["translation"].array)]):
            all_translations.append(pd.concat([rand_variants, additional_variant]).sample(4).values)
        else:
            all_translations.append(
                pd.concat([rand_variants, entire_dtf.sample(1, ignore_index=True)]).sample(4).values)
    return all_translations


def get_tasks_form_data(variants: pd.DataFrame, all_translations: list[np.array]):
    return [{
        "source_word-translation": (variants["source"][i], variants["translation"][i]),
        "translation_variants": [(all_translations[i][j][0], all_translations[i][j][1]) for j in
                                 range(len(all_translations[i]))]
    } for i in range(len(all_translations))]


# Create your views here.
def index(request):
    if request.method == "POST":
        form = UploadFile(request.POST, request.FILES)
        if form.is_valid():
            doc_ = Document(request.FILES["file"])
            pars = doc_.paragraphs
            # дальше получаем датафрейм со столбцами "исходное" и "переведенное", и доп. полем (там везде None)
            df = pd.DataFrame([replace_str(i.text).split(" - ") for i in pars],
                              columns=["source", "translation", "extra"])
            # удаляем поле с None
            df: pd.DataFrame = df.drop(columns=["extra"])
            # получаем 20 случайных вариантов пары исходное - переведенное. Это будет отображено на сайте, рандомчик
            source_translation_df = df.sample(20, ignore_index=True)
            translation_variants = get_all_translations(df, source_translation_df)
            variants = source_translation_df.values
            form_data = get_tasks_form_data(source_translation_df, translation_variants)
            f = TasksForm(form_data=form_data)
            return render(request, template_name="checker.html", context={"tasks": zip(variants, translation_variants)})
    else:
        form = UploadFile()
    return render(request, template_name="index.html", context={"form": form})


@csrf_exempt
def check_form(request):
    print(request.POST)
    return render(request, template_name="checker.html", context={})
