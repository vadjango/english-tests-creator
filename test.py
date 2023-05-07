import pandas as pd

example = pd.DataFrame({"source": ["car", "six", "false"], "translation": ["машина", "шесть", "ложь"]})
a = pd.DataFrame({"source": ["hash", "code", "processor", "six", "false", "gang", "car"],
                  "translation": ["хеш", "код", "процессор", "шесть", "ложь", "удар", "машина"]})

for lol, kek in zip(example.values, a.values):
    print(lol, kek)

