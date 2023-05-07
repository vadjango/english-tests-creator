import numpy as np
from django.test import TestCase
import pandas as pd
from checker.views import get_all_translations


# Create your tests here.
class GetAllTranslationsTestCase(TestCase):

    def test_different_values_in_dataframes(self):
        entire_df = pd.DataFrame(data=
                                 {"source":
                                      ["car", "to resolve", "running", "to cheat", "ghost",
                                       "pentagon", "two", "three", "four", "five", "six", "seven",
                                       "nine", "ten", "eleven"],
                                  "translation":
                                      ["машина", "решить", "выполнение", "обманывать",
                                       "привидение", "пятиугольник", "два", "три", "четыре", "пять", "шесть",
                                       "семь", "девять", "десять", "одиннадцать"]})

        variants_df = pd.DataFrame(data={
            "source": ["car", "eleven", "nine", "pentagon", "to resolve"],
            "translation": ["машина", "одиннадцать", "девять", "пятиугольник", "решить"]
        })
        all_trans = get_all_translations(entire_df, variants_df)
        for translation_pack in all_trans:
                # проверяем, есть ли слово в списке уникальных слов
            self.assertFalse(len(translation_pack[translation_pack.duplicated()]))
            # for translation in translation_pack:
            #     self.assertFalse(translation.isin(existed))

